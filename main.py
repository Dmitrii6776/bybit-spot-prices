from fastapi import FastAPI
from fastapi.responses import FileResponse
import requests
import uvicorn

app = FastAPI()

API_KEY = "2Afh93tlwzcQgnxHY"

# Fetch spot prices and trading data from Bybit
def get_bybit_spot_prices():
    url = "https://api.bybit.com/v5/market/tickers?category=spot"
    headers = {"X-BYBIT-API-KEY": API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

# Single coin full data
@app.get("/price/{symbol}")
def fetch_price(symbol: str):
    data = get_bybit_spot_prices()
    for coin in data.get("result", {}).get("list", []):
        if coin["symbol"].lower() == symbol.lower():
            return {
                "symbol": symbol,
                "lastPrice": coin["lastPrice"],
                "highPrice24h": coin.get("highPrice24h"),
                "lowPrice24h": coin.get("lowPrice24h"),
                "turnover24h": coin.get("turnover24h"),
                "price24hPcnt": coin.get("price24hPcnt"),
                "bid1Price": coin.get("bid1Price"),
                "ask1Price": coin.get("ask1Price"),
                "bid1Qty": coin.get("bid1Qty"),
                "ask1Qty": coin.get("ask1Qty")
            }
    return {"error": "Symbol not found"}

# Market scanner: only high-volume coins
@app.get("/market-scan")
def market_scan():
    data = get_bybit_spot_prices()
    high_volume_symbols = []
    for coin in data.get("result", {}).get("list", []):
        turnover = float(coin.get("turnover24h", 0))
        if turnover > 10000000:  # $10M turnover filter
            high_volume_symbols.append({
                "symbol": coin["symbol"],
                "lastPrice": coin["lastPrice"],
                "turnover24h": coin["turnover24h"],
                "price24hPcnt": coin["price24hPcnt"]
            })
    return high_volume_symbols

# Static serving for plugin system
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

# Uvicorn server runner
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)