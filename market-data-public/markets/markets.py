import requests

def fetch_market_data():
    market_code = 'BTC-USD-SWAP-LIN'
    url = f'https://api.ox.fun/v3/markets?marketCode={market_code}'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        print('Market Data:', response.json())
    except requests.exceptions.RequestException as error:
        print('Error fetching market data:', error)

fetch_market_data()