import requests

BASE_URL = "https://api.india.delta.exchange"  # Replace with the actual base URL of the API

def get_historical_candles(
    symbol: str,
    resolution: str,
    start: int,
    end: int,  
):
    """
    Fetch historical candle data for a given symbol and resolution.

    Args:
        symbol (str): The trading symbol (e.g., "BTCUSD").
        resolution (str): The resolution of the candles (e.g., "1m", "5m", "1h", "1d").
        start (int): The start timestamp in milliseconds.
        end (int): The end timestamp in milliseconds.
    """
    url = f"{BASE_URL}/v2/history/candles"
    params = {
        "symbol": symbol,
        "resolution": resolution,
        "start": start,
        "end": end
    }

    headers = {
        "Accept": "application/json"
    }   
    response = requests.get(
        url, 
        params=params,
        headers=headers,
        timeout=30
        )
    response.raise_for_status()  # Raise an exception for HTTP errors

    return response.json()

def get_latest_candles(
        symbol: str,
        resolution: str = "1h",
        lookback_hours: int = 10
):
    """
    Fetch the latest candles from Delta Exchange.
    
    Args:
        symbol (str): Trading symbol, e.g. "BTCUSD".
        resolution (str): Candle resolution, e.g. "1h".
        lookback_hours (int): Number of hours of historical candles to request.
        
    Returns:
        list: List of candle dictionaries.
    """
    import time

    end = int(time.time())
    start = end - (lookback_hours * 60 * 60)

    response = get_historical_candles(
        symbol=symbol,
        resolution=resolution,
        start=start,
        end=end
    )

    if not response.get("success"):
        raise RuntimeError(
            f"Delta API request failed: {response}"
        )

    return response["result"]