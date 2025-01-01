import requests

def fetch_assets_data():
    asset = 'BTC'
    url = f'https://api.ox.fun/v3/assets?asset={asset}'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        print('Assets Data:', response.json())
    except requests.exceptions.RequestException as error:
        print('Error fetching assets data:', error)

fetch_assets_data()