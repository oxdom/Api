const axios = require('axios');

async function fetchOperationalMarketData(marketCode) {
  const url = `https://api.ox.fun/v3/markets/operational?marketCode=${marketCode}`;

  try {
    const response = await axios.get(url);
    console.log('Operational Market Data:', response.data);
  } catch (error) {
    console.error('Error fetching operational market data:', error.response ? error.response.data : error.message);
  }
}

// Example usage
fetchOperationalMarketData('BTC-USD-SWAP-LIN');