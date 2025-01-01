const axios = require('axios');

async function fetchLeverageTiers(marketCode) {
  const url = `https://api.ox.fun/v3/leverage/tiers?marketCode=${marketCode}`;

  try {
    const response = await axios.get(url);
    console.log('Leverage Tiers Data:', response.data);
  } catch (error) {
    console.error('Error fetching leverage tiers data:', error.response ? error.response.data : error.message);
  }
}

// Example usage
fetchLeverageTiers('BTC-USD-SWAP-LIN');