const axios = require('axios');

async function fetchFundingEstimates(marketCode) {
  const url = `https://api.ox.fun/v3/funding/estimates?marketCode=${marketCode}`;

  try {
    const response = await axios.get(url);
    console.log('Funding Estimates:', response.data);
  } catch (error) {
    console.error('Error fetching funding estimates:', error.response ? error.response.data : error.message);
  }
}

// Example usage
fetchFundingEstimates('BTC-USD-SWAP-LIN'); 