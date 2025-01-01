require('dotenv').config();
const CryptoJS = require("crypto-js");
const axios = require('axios');

async function fetchTransfers(asset, limit, startTime, endTime) {
  const apiKey = process.env.API_KEY;
  const secretKey = process.env.API_SECRET;
  const ts = new Date().toISOString();
  const nonce = Math.random().toString(36).substring(2);
  const method = "/v3/transfer";
  const apiUrl = "api.ox.fun";

  const queryString = `asset=${asset}&limit=${limit}&startTime=${startTime}&endTime=${endTime}`;
  const msgString = `${ts}\n${nonce}\nGET\n${apiUrl}\n${method}\n${queryString}`;

  const sign = CryptoJS.enc.Base64.stringify(CryptoJS.HmacSHA256(msgString, secretKey));

  const headers = {
    'Content-Type': 'application/json',
    'AccessKey': apiKey,
    'Timestamp': ts,
    'Signature': sign,
    'Nonce': nonce
  };

  try {
    const response = await axios.get(`https://${apiUrl}${method}?${queryString}`, { headers });
    if (response.data.success) {
      return response.data.data;
    } else {
      console.error('Failed to fetch transfer data');
    }
  } catch (error) {
    console.error('Error fetching transfer data:', error.response ? error.response.data : error.message);
  }
}

// Example usage
const asset = 'OX';
const limit = 100;
const startTime = Date.now() - 24 * 60 * 60 * 1000;
const endTime = Date.now();
fetchTransfers(asset, limit, startTime, endTime).then(data => {
  console.log(data);
});