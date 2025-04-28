# Expanded Plugin Code for Full Spot Trading Data!

from fastapi import FastAPI
import requests

app = FastAPI()

API_KEY = "2Afh93tlwzcQgnxHY"

# Fetch spot prices and trading data from Bybit
def get_bybit_spot_prices():
    url = "https://api.bybit.com/v5/market/tickers?category=spot"
    headers = {
        "X-BYBIT-API-KEY": API_KEY
    }
    response = requests.get(url, headers=headers)
    return response.json()

@app.get("/price/{symbol}")
def fetch_price(symbol: str):
    data = get_bybit_spot_prices()
    for coin in data.get("result", {}).get("list", []):
        if coin["symbol"].lower() == symbol.lower():
            return {
                "symbol": symbol,
                "lastPrice": coin["lastPrice"],
                "highPrice24h": coin.get("highPrice24h", None),
                "lowPrice24h": coin.get("lowPrice24h", None),
                "turnover24h": coin.get("turnover24h", None),
                "price24hPcnt": coin.get("price24hPcnt", None),
                "bid1Price": coin.get("bid1Price", None),
                "ask1Price": coin.get("ask1Price", None),
                "bid1Qty": coin.get("bid1Qty", None),
                "ask1Qty": coin.get("ask1Qty", None)
            }
    return {"error": "Symbol not found"}

# Static File Endpoints
from fastapi.responses import FileResponse

@app.get("/.well-known/ai-plugin.json")
def serve_plugin_manifest():
    return FileResponse(".well-known/ai-plugin.json", media_type='application/json')

@app.get("/openapi.yaml")
def serve_openapi_spec():
    return FileResponse("openapi.yaml", media_type='text/yaml')

@app.get("/logo.png")
def serve_logo():
    return FileResponse("logo.png", media_type='image/png')

@app.get("/legal")
def serve_legal():
    return FileResponse("legal.html", media_type='text/html')

# Uvicorn server run for Railway
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
