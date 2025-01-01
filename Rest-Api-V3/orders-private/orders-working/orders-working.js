const axios = require('axios');
const crypto = require('crypto');
require('dotenv').config();

async function fetchWorkingOrders(marketCode, orderId = null, clientOrderId = null) {
    const apiKey = process.env.API_KEY;
    const secretKey = process.env.API_SECRET;
    const ts = new Date().toISOString().split('.')[0] + 'Z';
    const nonce = Date.now().toString();
    const method = "/v3/orders/working";
    const apiUrl = "api.ox.fun";

    let queryString = `marketCode=${marketCode}`;
    if (orderId) {
        queryString += `&orderId=${orderId}`;
    }
    if (clientOrderId) {
        queryString += `&clientOrderId=${clientOrderId}`;
    }

    const msgString = `${ts}\n${nonce}\nGET\n${apiUrl}\n${method}\n${queryString}`;

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
        const response = await axios.get(`https://${apiUrl}${method}?${queryString}`, { headers });
        const data = response.data;
        if (data.success) {
            return data;
        } else {
            console.log('Failed to fetch working orders');
        }
    } catch (error) {
        console.log('Error fetching working orders:', error);
    }
}

// Example usage
fetchWorkingOrders("BTC-USD-SWAP-LIN").then(orders => console.log(orders));