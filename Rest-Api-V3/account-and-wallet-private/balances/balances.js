const axios = require('axios');
const crypto = require('crypto');
require('dotenv').config();

async function getBalances(subAccounts = [], asset = '') {
    const apiKey = process.env.API_KEY;
    const secretKey = process.env.API_SECRET;
    const ts = new Date().toISOString();
    const nonce = Math.random().toString(36).substring(2);
    const apiUrl = "api.ox.fun";
    const method = "/v3/balances";
    
    // Construct query parameters
    const subAccParam = subAccounts.length > 0 ? `subAcc=${subAccounts.join(',')}` : '';
    const assetParam = asset ? `asset=${asset}` : '';
    const queryString = [subAccParam, assetParam].filter(Boolean).join('&');
    
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
        console.log('Response:', response.data);

        // Display each account's balances
        response.data.data.forEach(account => {
            console.log(`Account Name: ${account.name}`);
            account.balances.forEach(balance => {
                console.log(`Asset: ${balance.asset}, Total: ${balance.total}, Available: ${balance.available}, Reserved: ${balance.reserved}`);
            });
        });
    } catch (error) {
        console.error('Error fetching balances:', error.response ? error.response.data : error.message);
    }
}

// Example usage
const subAccounts = ['subaccount1'];
const asset = 'OX';
getBalances(subAccounts, asset);