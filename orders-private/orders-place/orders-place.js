const axios = require('axios');
const crypto = require('crypto');
require('dotenv').config();

async function placeOrders(orders) {
    const apiKey = process.env.API_KEY;
    const secretKey = process.env.API_SECRET;
    const ts = new Date().toISOString();
    const nonce = Math.random().toString(36).substring(2);
    const method = "/v3/orders/place";
    const apiUrl = "api.ox.fun";

    const postData = {
        recvWindow: 20000,
        responseType: "FULL",
        timestamp: Date.now(),
        orders: orders
    };

    const body = JSON.stringify(postData);
    const msgString = `${ts}\n${nonce}\nPOST\n${apiUrl}\n${method}\n${body}`;

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
        const response = await axios.post(`https://${apiUrl}${method}`, body, { headers });
        console.log('Response:', response.data);
    } catch (error) {
        console.error('Error placing orders:', error.response ? error.response.data : error.message);
    }
}

// Example usage
const orders = [
    {
        clientOrderId: 1612249737724,
        marketCode: "BTC-USD-SWAP-LIN",
        side: "SELL",
        quantity: "0.001",
        timeInForce: "GTC",
        orderType: "LIMIT",
        price: "50007"
    },
    {
        clientOrderId: 1612249737724,
        marketCode: "BTC-USD-SWAP-LIN",
        side: "BUY",
        quantity: "0.002",
        timeInForce: "GTC",
        orderType: "LIMIT",
        price: "54900"
    }
];

placeOrders(orders);