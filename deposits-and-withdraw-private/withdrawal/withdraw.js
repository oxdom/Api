require('dotenv').config();
const axios = require('axios');
const CryptoJS = require("crypto-js");

async function makeWithdrawal() {
  const apiKey = process.env.API_KEY;
  const secretKey = process.env.API_SECRET;
  const withdrawAddress = process.env.WITHDRAW_ADDRESS;
  const ts = new Date().toISOString();
  const nonce = Math.random().toString(36).substring(2);
  const method = "/v3/withdrawal";
  const timestamp = Math.floor(Date.now() / 1000);
  const postData = {
    asset: "OX",
    network: "Solana",
    address: withdrawAddress,
    quantity: "100",
    externalFee: true,
    recvWindow: 3000,
    timestamp: timestamp,
    responseType: "FULL"
  };
  const body = JSON.stringify(postData);

  const msgString = `${ts}\n${nonce}\nPOST\napi.ox.fun\n${method}\n${body}`;
  const sign = CryptoJS.enc.Base64.stringify(CryptoJS.HmacSHA256(msgString, secretKey));

  try {
    const response = await axios.post(`https://api.ox.fun${method}`, body, {
      headers: {
        'Content-Type': 'application/json',
        'AccessKey': apiKey,
        'Timestamp': ts,
        'Signature': sign,
        'Nonce': nonce
      }
    });

    if (response.data.success) {
      console.log('Withdrawal Successful:', response.data.data);
    } else {
      console.error('Failed to initiate withdrawal');
    }
  } catch (error) {
    console.error('Error making withdrawal request:', error);
  }
}

makeWithdrawal();
