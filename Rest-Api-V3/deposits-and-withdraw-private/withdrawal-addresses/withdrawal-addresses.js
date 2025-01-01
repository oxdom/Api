require('dotenv').config();
const axios = require('axios');
const CryptoJS = require("crypto-js");

async function getWithdrawalAddress(asset, network) {
  const apiKey = process.env.API_KEY;
  const secretKey = process.env.API_SECRET;
  const timestamp = new Date().toISOString();
  const nonce = Math.random().toString(36).substring(2);
  const verb = 'GET';
  const path = 'api.ox.fun';
  const method = '/v3/withdrawal-addresses';
  const body = `asset=${asset}&network=${network}`;

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
      console.log('Withdrawal Address:', response.data.data);
    } else {
      console.error('Failed to fetch withdrawal address');
    }
  } catch (error) {
    console.error('Error making API request:', error.response ? error.response.data : error.message);
  }
}

// Example usage
getWithdrawalAddress('OX', 'Solana');
