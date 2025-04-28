from fastapi import FastAPI
import requests
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

app = FastAPI()

# Bybit API Key (PUBLIC, no secret needed for market data)
API_KEY = "2Afh93tlwzcQgnxHY"

# Fetch spot prices from Bybit
def get_bybit_spot_prices():
    url = "https://api.bybit.com/v5/market/tickers?category=spot"
    headers = {
        "2Afh93tlwzcQgnxHY": API_KEY
    }
    response = requests.get(url, headers=headers)
    return response.json()

@app.get("/price/{symbol}")
def fetch_price(symbol: str):
    data = get_bybit_spot_prices()
    for coin in data.get("result", {}).get("list", []):
        if coin["symbol"].lower() == symbol.lower():
            return {"symbol": symbol, "price": coin["lastPrice"]}
    return {"error": "Symbol not found"}