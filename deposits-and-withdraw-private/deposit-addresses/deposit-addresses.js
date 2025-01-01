require('dotenv').config();
const axios = require('axios');
const CryptoJS = require("crypto-js");

async function getDepositAddress(asset, network) {
  const apiKey = process.env.API_KEY;
  const secretKey = process.env.API_SECRET;
  const timestamp = new Date().toISOString();
  const nonce = Math.random().toString(36).substring(2);
  const method = 'GET';
  const path = 'api.ox.fun';
  const endpoint = '/v3/deposit-addresses';
  const query = `asset=${asset}&network=${network}`;
  const msgString = `${timestamp}\n${nonce}\n${method}\n${path}\n${endpoint}\n${query}`;

  const sign = CryptoJS.enc.Base64.stringify(CryptoJS.HmacSHA256(msgString, secretKey));

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
    //console.log(response.data);
    if (response.data.success) {
      return response.data.data.address;
    } else {
      console.error('Failed to fetch deposit address');
    }
  } catch (error) {
    console.error('Error making API request:', error.response ? error.response.data : error.message);
  }
}

async function main() {
  const address = await getDepositAddress('OX', 'Solana');
  console.log(address);
}

main();
