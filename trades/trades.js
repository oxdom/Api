const axios = require('axios');
const crypto = require('crypto');
require('dotenv').config();

async function fetchTrades(marketCode, limit, startTime, endTime) {
  const apiKey = process.env.API_KEY;
  const secretKey = process.env.API_SECRET;
  const ts = new Date().toISOString().split('.')[0] + 'Z';
  const nonce = Date.now().toString();
  const method = "/v3/trades";
  const apiUrl = "api.ox.fun";

  const queryString = `marketCode=${marketCode}&limit=${limit}&startTime=${startTime}&endTime=${endTime}`;
  const msgString = `${ts}\n${nonce}\nGET\n${apiUrl}\n${method}\n${queryString}`;

  const sign = crypto.createHmac('sha256', secretKey)
    .update(msgString)
    .digest('base64');

  const headers = {
    'Content-Type': 'application/json',
    'AccessKey': apiKey,
    'Timestamp': ts,
    'Signature': sign,
    'Nonce': nonce
  };

  const url = `https://${apiUrl}${method}?${queryString}`;

  try {
    const response = await axios.get(url, { headers });
    if (response.data.success) {
      console.log('Trades Data:', response.data.data);
    } else {
      console.error('Failed to fetch trades');
    }
  } catch (error) {
    console.error('Error fetching trades:', error.response ? error.response.data : error.message);
  }
}

// Example usage
const market_code = 'BTC-USD-SWAP-LIN';
const limit = 100;
const start_time = Date.now() - 24 * 60 * 60 * 1000; // 24 hours ago
const end_time = Date.now();
fetchTrades(market_code, limit, start_time, end_time);