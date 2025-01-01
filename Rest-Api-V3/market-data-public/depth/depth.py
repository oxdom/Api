import requests

def fetch_market_depth(market_code, level):
    url = f'https://api.ox.fun/v3/depth?marketCode={market_code}&level={level}'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        print('Market Depth Data:', response.json())
    except requests.exceptions.RequestException as error:
        print('Error fetching market depth data:', error)

# Example usage
fetch_market_depth('BTC-USD-SWAP-LIN', 10)