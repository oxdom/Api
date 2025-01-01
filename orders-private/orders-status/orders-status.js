const axios = require('axios');
const crypto = require('crypto');
require('dotenv').config();

async function fetchOrderStatus(orderId = null, clientOrderId = null) {
    if (!orderId && !clientOrderId) {
        throw new Error("Either orderId or clientOrderId must be provided.");
    }

    const apiKey = process.env.API_KEY;
    const secretKey = process.env.API_SECRET;
    const ts = new Date().toISOString().split('.')[0] + 'Z';
    const nonce = Date.now().toString();
    const method = "/v3/orders/status";
    const apiUrl = "api.ox.fun";

    const queryString = orderId ? `orderId=${orderId}` : `clientOrderId=${clientOrderId}`;
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
            console.log('Failed to fetch order status');
        }
    } catch (error) {
        console.error('Error fetching order status:', error.response ? error.response.data : error.message);
    }
}

// Example usage
fetchOrderStatus(orderId="111111111111111111").then(status => console.log(status));