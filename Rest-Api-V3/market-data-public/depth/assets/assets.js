const axios = require('axios');

async function fetchMarketData() {
  const asset = 'BTC';
  const url = `https://api.ox.fun/v3/assets?asset=${asset}`;

  try {
    const response = await axios.get(url);
    console.log('Market Data:', response.data);
  } catch (error) {
    console.error('Error fetching market data:', error.response ? error.response.data : error.message);
  }
}

fetchMarketData();