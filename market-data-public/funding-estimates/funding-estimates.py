import requests

def fetch_funding_estimates(market_code):
    url = f'https://api.ox.fun/v3/funding/estimates?marketCode={market_code}'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        print('Funding Estimates:', response.json())
    except requests.exceptions.RequestException as error:
        print('Error fetching funding estimates:', error)

# Example usage
fetch_funding_estimates('BTC-USD-SWAP-LIN')