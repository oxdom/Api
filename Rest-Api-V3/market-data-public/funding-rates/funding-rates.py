import requests
import time

def fetch_funding_rates(market_code, limit=100):
    # Calculate startTime as 24 hours ago
    start_time = int(time.time() * 1000) - 24 * 60 * 60 * 1000  # 24 hours in milliseconds

    # Calculate endTime as the current time
    end_time = int(time.time() * 1000)

    url = f'https://api.ox.fun/v3/funding/rates?marketCode={market_code}&limit={limit}&startTime={start_time}&endTime={end_time}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        print('Funding Rates Data:', response.json())
    except requests.exceptions.RequestException as error:
        print('Error fetching funding rates data:', error)

# Example usage
fetch_funding_rates('BTC-USD-SWAP-LIN', 100)