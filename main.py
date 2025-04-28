from fastapi import FastAPI
from fastapi.responses import FileResponse
import requests
import os
import uvicorn

app = FastAPI()

API_KEY = "2Afh93tlwzcQgnxHY"

@app.get("/price/{symbol}")
def fetch_price(symbol: str):
    url = "https://api.bybit.com/v5/market/tickers?category=spot"
    headers = {"X-BYBIT-API-KEY": API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    for coin in data.get("result", {}).get("list", []):
        if coin["symbol"].lower() == symbol.lower():
            return {"symbol": symbol, "price": coin["lastPrice"]}
    return {"error": "Symbol not found"}

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

# 🛠 ADD THIS at the bottom:
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)