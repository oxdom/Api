require('dotenv').config();
const axios = require('axios');
const CryptoJS = require("crypto-js");

async function getAccountInfo(subAccounts = []) {
  const apiKey = process.env.API_KEY;
  const secretKey = process.env.API_SECRET;
  const timestamp = new Date().toISOString();
  const nonce = Math.random().toString(36).substring(2);
  const verb = 'GET';
  const path = 'api.ox.fun';
  const method = '/v3/account';
  const subAccParam = subAccounts.length ? `subAcc=${subAccounts.join(',')}` : '';
  const body = subAccParam;

  const msgString = `${timestamp}\n${nonce}\n${verb}\n${path}\n${method}\n${body}`;
  const sign = CryptoJS.enc.Base64.stringify(CryptoJS.HmacSHA256(msgString, secretKey));

  try {
    let url = `https://${path}${method}`;
    if (subAccParam) {
      url += `?${subAccParam}`;
    }

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
      return response.data.data;
    } else {
      console.error('Failed to fetch account data');
    }
  } catch (error) {
    console.error('Error making API request:', error.response ? error.response.data : error.message);
  }
}

// Example usage
response = getAccountInfo();
console.log(response);