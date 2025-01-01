require('dotenv').config();
const axios = require('axios');
const CryptoJS = require("crypto-js");

async function fetchFundingData(marketCode, limit = 100, startTime, endTime) {
  const apiKey = process.env.API_KEY;
  const secretKey = process.env.API_SECRET;
  const ts = new Date().toISOString();
  const nonce = Math.random().toString(36).substring(2);
  const method = "/v3/funding";
  const queryString = `marketCode=${marketCode}&limit=${limit}&startTime=${startTime}&endTime=${endTime}`;
  const msgString = `${ts}\n${nonce}\nGET\napi.ox.fun\n${method}\n${queryString}`;
  const sign = CryptoJS.enc.Base64.stringify(CryptoJS.HmacSHA256(msgString, secretKey));

  try {
    const response = await axios.get(`https://api.ox.fun${method}?${queryString}`, {
      headers: {
        'Content-Type': 'application/json',
        'AccessKey': apiKey,
        'Timestamp': ts,
        'Signature': sign,
        'Nonce': nonce
      }
    });

    if (response.data.success) {
      return response;
    } else {
      console.error('Failed to fetch funding data');
    }
  } catch (error) {
    console.error('Error fetching funding data:', error.response ? error.response.data : error.message);
  }
}

// Example usage
// start time and end time are in milliseconds and must be within 7 days of each other
(async () => {
  const startTime = Date.now() - 24 * 60 * 60 * 1000; // 24 hours in milliseconds
  const endTime = Date.now();
  const response = await fetchFundingData('BTC-USD-SWAP-LIN', 100, startTime, endTime);
  console.log(response);
})();