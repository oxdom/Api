import requests

def fetch_ticker_data(market_code):
    url = f'https://api.ox.fun/v3/tickers?marketCode={market_code}'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        print('Ticker Data:', response.json())
    except requests.exceptions.RequestException as error:
        print('Error fetching ticker data:', error)

# Example usage
fetch_ticker_data('BTC-USD-SWAP-LIN') 