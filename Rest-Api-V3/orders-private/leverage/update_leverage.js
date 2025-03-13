const axios = require('axios');
const crypto = require('crypto');
const dotenv = require('dotenv');

dotenv.config();

function adjustLeverage(marketCode, leverage) {
    const apiKey = process.env.API_KEY;
    const secretKey = Buffer.from(process.env.API_SECRET, 'utf-8');
    const ts = new Date().toISOString().slice(0, 19).replace('T', ' ');
    const nonce = Date.now().toString();
    const method = "/v3/leverage";
    const apiUrl = "api.ox.fun";

    const payload = {
        marketCode: marketCode,
        leverage: leverage
    };

    const payloadStr = JSON.stringify(payload);
    const msgString = `${ts}\n${nonce}\nPOST\n${apiUrl}\n${method}\n${payloadStr}`;

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

    const url = `https://${apiUrl}${method}`;

    axios.post(url, payload, { headers })
        .then(response => {
            const data = response.data;
            if (data.success) {
                console.log('Leverage Adjustment Successful:', data.data);
            } else {
                console.log('Failed to adjust leverage:', data);
            }
        })
        .catch(error => {
            console.error('Error adjusting leverage:', error.message);
        });
}

// Example usage
const marketCode = 'BTC-USD-SWAP-LIN';
const leverage = 1; // Example leverage value
adjustLeverage(marketCode, leverage);
