import yfinance as yf
from datetime import datetime
import pytz

def default(request):
    try:
        symbol = request.query.get("symbol", None)
        if not symbol:
            return {
                "statusCode": 400,
                "body": "Missing 'symbol' in query"
            }

        stock = yf.Ticker(symbol)
        info = stock.info

        if 'shortName' not in info:
            return {
                "statusCode": 404,
                "body": f"No data found for '{symbol.upper()}'"
            }

        dt = datetime.now(pytz.timezone("US/Pacific"))
        price = info['regularMarketPrice']
        change = info.get('regularMarketChange', 0)
        percent = info.get('regularMarketChangePercent', 0)
        result = {
            "datetime": dt.strftime("%a %b %d %H:%M:%S %Z %Y"),
            "company": f"{info['shortName']} ({symbol.upper()})",
            "price": f"{price:.2f} {'+' if change >= 0 else '-'}{abs(change):.2f} ({'+' if percent >= 0 else '-'}{abs(percent):.2f}%)"
        }

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": result
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }
