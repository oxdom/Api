const axios = require('axios');

async function fetchCandleData(marketCode, timeframe = '3600s', limit) {
  // Validate the timeframe
  const validTimeframes = ['60s', '300s', '900s', '1800s', '3600s', '7200s', '14400s', '86400s'];
  if (!validTimeframes.includes(timeframe)) {
    console.error('Invalid timeframe. Please use one of the following:', validTimeframes.join(', '));
    return;
  }

  // Calculate startTime as 24 hours ago
  const startTime = Date.now() - 24 * 60 * 60 * 1000; // 24 hours in milliseconds

  // Calculate endTime as the current time
  const endTime = Date.now();

  const url = `https://api.ox.fun/v3/candles?marketCode=${marketCode}&timeframe=${timeframe}&limit=${limit}&startTime=${startTime}&endTime=${endTime}`;

  try {
    const response = await axios.get(url);
    console.log('Candle Data:', response.data);
  } catch (error) {
    console.error('Error fetching candle data:', error.response ? error.response.data : error.message);
  }
}

// Example usage
fetchCandleData('BTC-USD-SWAP-LIN', '3600s', 100); 