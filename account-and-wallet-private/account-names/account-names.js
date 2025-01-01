require('dotenv').config();
const axios = require('axios');
const CryptoJS = require("crypto-js");

async function getAccountNames() {
  const apiKey = process.env.API_KEY;
  const secretKey = process.env.API_SECRET;
  const timestamp = new Date().toISOString();
  const nonce = Math.random().toString(36).substring(2);
  const verb = 'GET';
  const path = 'api.ox.fun';
  const method = '/v3/account/names';
  const body = '';

  const msgString = `${timestamp}\n${nonce}\n${verb}\n${path}\n${method}\n${body}`;
  const sign = CryptoJS.enc.Base64.stringify(CryptoJS.HmacSHA256(msgString, secretKey));

  try {
    const url = `https://${path}${method}`;

    const response = await axios.get(url, {
      headers: {
        'Content-Type': 'application/json',
        'AccessKey': apiKey,
        'Timestamp': timestamp,
        'Signature': sign,
        'Nonce': nonce
      }
    });

    console.log("Raw Response Content:", response.data);

    if (response.data.success) {
      console.log("Account Names:", response.data.data);
      return response.data.data;
    } else {
      console.error('Failed to fetch account names');
    }
  } catch (error) {
    console.error('Error making API request:', error.response ? error.response.data : error.message);
  }
}

// Example usage
getAccountNames();