require('dotenv').config();
const axios = require('axios');
const crypto = require('crypto');

async function getDepositData(asset, limit, startTime, endTime) {
  const apiKey = process.env.API_KEY;
  const secretKey = process.env.API_SECRET;
  const timestamp = new Date().toISOString();
  const nonce = Math.random().toString(36).substring(2);
  const method = 'GET';
  const path = 'api.ox.fun';
  const endpoint = '/v3/deposit';
  const query = `asset=${asset}&limit=${limit}&startTime=${startTime}&endTime=${endTime}`;
  const msgString = `${timestamp}\n${nonce}\n${method}\n${path}\n${endpoint}\n${query}`;

  const sign = crypto.createHmac('sha256', secretKey).update(msgString).digest('base64');

  try {
    const response = await axios.get(`https://${path}${endpoint}?${query}`, {
      headers: {
        'Content-Type': 'application/json',
        'AccessKey': apiKey,
        'Timestamp': timestamp,
        'Signature': sign,
        'Nonce': nonce
      }
    });

    if (response.data.success) {
      return response.data.data;
    } else {
      console.error('Failed to fetch deposit data');
    }
  } catch (error) {
    console.error('Error making API request:', error.response ? error.response.data : error.message);
  }
}

// Example usage
async function main() {
const startTime = Date.now() - 24 * 60 * 60 * 1000; // 24 hours ago in milliseconds
const endTime = Date.now(); // current time in milliseconds
data = await getDepositData('OX', 100, startTime, endTime);
console.log(data);
}

main();
