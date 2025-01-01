import requests

def fetch_operational_market_data(market_code):
    url = f'https://api.ox.fun/v3/markets/operational?marketCode={market_code}'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        print('Operational Market Data:', response.json())
    except requests.exceptions.RequestException as error:
        print('Error fetching operational market data:', error)

# Example usage
fetch_operational_market_data('BTC-USD-SWAP-LIN')