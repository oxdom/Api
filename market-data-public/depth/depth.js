const axios = require('axios');

async function fetchMarketDepth(marketCode, level) {
  const url = `https://api.ox.fun/v3/depth?marketCode=${marketCode}&level=${level}`;

  try {
    const response = await axios.get(url);
    console.log('Market Depth Data:', response.data);
  } catch (error) {
    console.error('Error fetching market depth data:', error.response ? error.response.data : error.message);
  }
}

// Example usage
fetchMarketDepth('BTC-USD-SWAP-LIN', 10);