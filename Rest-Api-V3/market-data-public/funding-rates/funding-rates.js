const axios = require('axios');

async function fetchFundingRates(marketCode, limit = 100) {
  // Calculate startTime as 24 hours ago
  const startTime = Date.now() - 24 * 60 * 60 * 1000; // 24 hours in milliseconds

  // Calculate endTime as the current time
  const endTime = Date.now();

  const url = `https://api.ox.fun/v3/funding/rates?marketCode=${marketCode}&limit=${limit}&startTime=${startTime}&endTime=${endTime}`;

  try {
    const response = await axios.get(url);
    console.log('Funding Rates Data:', response.data);
  } catch (error) {
    console.error('Error fetching funding rates data:', error.response ? error.response.data : error.message);
  }
}

// Example usage
fetchFundingRates('BTC-USD-SWAP-LIN', 100);