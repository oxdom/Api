require('dotenv').config();
const axios = require('axios');
const crypto = require('crypto');

async function cancelAllOrders(marketCode) {
  const apiKey = process.env.API_KEY;
  const secretKey = process.env.API_SECRET;
  const ts = new Date().toISOString().split('.')[0] + 'Z';
  const nonce = Date.now().toString();
  const method = "/v3/orders/cancel-all";
  const apiUrl = "api.ox.fun";

  const postData = {
    marketCode: marketCode
  };

  const body = JSON.stringify(postData);
  const msgString = `${ts}\n${nonce}\nDELETE\n${apiUrl}\n${method}\n${body}`;

  const sign = crypto.createHmac('sha256', secretKey)
    .update(msgString)
    .digest('base64');

  const headers = {
    'Content-Type': 'application/json',
    'AccessKey': apiKey,
    'Timestamp': ts,
    'Signature': sign,
    'Nonce': nonce
  };

  try {
    const response = await axios.delete(`https://${apiUrl}${method}`, {
      data: body,
      headers: headers
    });
    console.log('Response:', response.data);
  } catch (error) {
    console.error('Error canceling all orders:', error.response ? error.response.data : error.message);
  }
}

// Example usage
cancelAllOrders("BTC-USD-SWAP-LIN");