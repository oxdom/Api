require('dotenv').config();
const CryptoJS = require("crypto-js");
const axios = require('axios');

async function createTransfer(asset, quantity, fromAccount, toAccount) {
  const apiKey = process.env.API_KEY;
  const secretKey = process.env.API_SECRET;
  const ts = new Date().toISOString();
  const nonce = Math.random().toString(36).substring(2);
  const method = "/v3/transfer";
  const apiUrl = "api.ox.fun";

  const body = {
    asset,
    quantity,
    fromAccount,
    toAccount
  };

  // For POST requests, we use the JSON stringified body instead of query params
  const bodyString = JSON.stringify(body);
  const msgString = `${ts}\n${nonce}\nPOST\n${apiUrl}\n${method}\n${bodyString}`;

  const sign = CryptoJS.enc.Base64.stringify(CryptoJS.HmacSHA256(msgString, secretKey));

  const headers = {
    'Content-Type': 'application/json',
    'AccessKey': apiKey,
    'Timestamp': ts,
    'Signature': sign,
    'Nonce': nonce
  };

  try {
    const response = await axios.post(`https://${apiUrl}${method}`, body, { headers });
    if (response.data.success) {
      return response.data.data;
    } else {
      console.error('Failed to create transfer');
    }
  } catch (error) {
    console.error('Error creating transfer:', error.response ? error.response.data : error.message);
  }
}

// Example usage
const asset = 'USDT';
const quantity = '1000';
const fromAccount = '14320';
const toAccount = '15343';

createTransfer(asset, quantity, fromAccount, toAccount).then(data => {
  console.log(data);
});
