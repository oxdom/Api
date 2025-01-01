import requests

def fetch_leverage_tiers(market_code):
    url = f'https://api.ox.fun/v3/leverage/tiers?marketCode={market_code}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        print('Leverage Tiers Data:', response.json())
    except requests.exceptions.RequestException as error:
        print('Error fetching leverage tiers data:', error)

# Example usage
fetch_leverage_tiers('BTC-USD-SWAP-LIN')