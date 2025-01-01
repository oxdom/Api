import requests
import time

def fetch_candle_data(market_code, timeframe='3600s', limit=100):
    # Validate the timeframe
    valid_timeframes = ['60s', '300s', '900s', '1800s', '3600s', '7200s', '14400s', '86400s']
    if timeframe not in valid_timeframes:
        print('Invalid timeframe. Please use one of the following:', ', '.join(valid_timeframes))
        return

    # Calculate startTime as 24 hours ago
    start_time = int(time.time() * 1000) - 24 * 60 * 60 * 1000  # 24 hours in milliseconds

    # Calculate endTime as the current time
    end_time = int(time.time() * 1000)

    url = f'https://api.ox.fun/v3/candles?marketCode={market_code}&timeframe={timeframe}&limit={limit}&startTime={start_time}&endTime={end_time}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        print('Candle Data:', response.json())
    except requests.exceptions.RequestException as error:
        print('Error fetching candle data:', error)

# Example usage
fetch_candle_data('BTC-USD-SWAP-LIN', '3600s', 100)