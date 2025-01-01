const axios = require('axios');

async function fetchTickerData(marketCode) {
  const url = `https://api.ox.fun/v3/tickers?marketCode=${marketCode}`;

  try {
    const response = await axios.get(url);
    console.log('Ticker Data:', response.data);
  } catch (error) {
    console.error('Error fetching ticker data:', error.response ? error.response.data : error.message);
  }
}

// Example usage
fetchTickerData('BTC-USD-SWAP-LIN'); 