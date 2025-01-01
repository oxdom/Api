const axios = require('axios');

async function fetchExchangeTrades(marketCode, limit = 100) {
  // Calculate startTime as 24 hours ago
  const startTime = Date.now() - 24 * 60 * 60 * 1000; // 24 hours in milliseconds

  // Calculate endTime as the current time
  const endTime = Date.now();

  const url = `https://api.ox.fun/v3/exchange-trades?marketCode=${marketCode}&limit=${limit}&startTime=${startTime}&endTime=${endTime}`;

  try {
    const response = await axios.get(url);
    console.log('Exchange Trades Data:', response.data);
  } catch (error) {
    console.error('Error fetching exchange trades data:', error.response ? error.response.data : error.message);
  }
}

// Example usage
fetchExchangeTrades('BTC-USD-SWAP-LIN', 100);