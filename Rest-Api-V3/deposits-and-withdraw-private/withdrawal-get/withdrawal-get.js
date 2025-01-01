require('dotenv').config();
const axios = require('axios');
const CryptoJS = require("crypto-js");

async function getWithdrawal(id, asset, limit, startTime, endTime) {
  const apiKey = process.env.API_KEY;
  const secretKey = process.env.API_SECRET;
  const timestamp = new Date().toISOString();
  const nonce = Math.random().toString(36).substring(2);
  const verb = 'GET';
  const path = 'api.ox.fun';
  const method = '/v3/withdrawal';
  const body = `id=${id}&asset=${asset}&limit=${limit}&startTime=${startTime}&endTime=${endTime}`;
  const msgString = `${timestamp}\n${nonce}\n${verb}\n${path}\n${method}\n${body}`;
  const sign = CryptoJS.enc.Base64.stringify(CryptoJS.HmacSHA256(msgString, secretKey));

  try {
    const response = await axios.get(`https://${path}${method}?${body}`, {
      headers: {
        'Content-Type': 'application/json',
        'AccessKey': apiKey,
        'Timestamp': timestamp,
        'Signature': sign,
        'Nonce': nonce
      }
    });

    if (response.data.success) {
      return response.data;
    } else {
      console.error('Failed to fetch withdrawal data', response.data);
    }
  } catch (error) {
    console.error('Error making API request:', error);
  }
}

// Example usage
const currentTime = Date.now();
const sevenDaysAgo = currentTime - (7 * 24 * 60 * 60 * 1000);

getWithdrawal('11111111111111111', 'OX', 100, sevenDaysAgo, currentTime)
  .then(response => console.log(response))
  .catch(error => console.error(error));