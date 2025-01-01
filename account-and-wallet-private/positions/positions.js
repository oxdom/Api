require('dotenv').config();
const axios = require('axios');
const CryptoJS = require("crypto-js");

async function fetchPositions(subAccounts, marketCode) {
  const apiKey = process.env.API_KEY;
  const secretKey = process.env.API_SECRET;
  const ts = new Date().toISOString();
  const nonce = Math.random().toString(36).substring(2);
  const method = "/v3/positions";
  const apiUrl = "api.ox.fun";

  const subAccParam = subAccounts ? `subAcc=${subAccounts.join(',')}` : "";
  const queryString = `${subAccParam}&marketCode=${marketCode}`.replace(/^&/, '');
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
    return response.data;
  } catch (error) {
    console.error('Error fetching positions:', error);
  }
}

// Example usage
const subAccounts = null;
const marketCode = 'BTC-USD-SWAP-LIN';
fetchPositions(subAccounts, marketCode).then(response => console.log(response));