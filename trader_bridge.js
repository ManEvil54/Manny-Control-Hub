const fs = require('fs');
const axios = require('axios');
const path = require('path');

// Load environment from config
const configPath = path.join(__dirname, 'config', 'tradier_env.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
const current = config.environments[config.active_env];

const tradierClient = axios.create({
  baseURL: current.base_url,
  headers: {
    'Authorization': `Bearer ${current.token}`,
    'Accept': 'application/json'
  }
});

console.log(`[MCH] System Armed in ${current.mode_label} Mode.`);

/**
 * Executes the "Scout" or "Hammer" trade
 * @param {string} symbol - e.g., /MNQ
 * @param {number} qty - 1 for Scout, 2 for Hammer
 * @param {string} type - 'market' or 'limit'
 */
async function placeSniperOrder(symbol, qty, type = 'market') {
  try {
    const params = new URLSearchParams();
    params.append('class', 'equity');
    params.append('symbol', symbol);
    params.append('side', 'buy');
    params.append('quantity', qty);
    params.append('type', type);
    params.append('duration', 'day');

    const response = await tradierClient.post(`accounts/${current.brokerage_id}/orders`, params);
    
    if (response.data.order && response.data.order.id) {
        console.log(`[Order Success] ${qty}x ${symbol} filled in ${config.active_env}. Order ID: ${response.data.order.id}`);
        return response.data.order.id;
    } else {
        const errorMsg = response.data.errors ? JSON.stringify(response.data.errors) : "Unknown error";
        console.error(`[Order Failed] ${symbol} could not be filled: ${errorMsg}`);
        return null;
    }
  } catch (err) {
    const errorMsg = err.response ? JSON.stringify(err.response.data) : err.message;
    console.error(`[Order Failed] System Error in ${config.active_env}:`, errorMsg);
    throw err;
  }
}

module.exports = { place_sniper_order: placeSniperOrder, config: current };

// If run directly, fire a test Scout order if in Sandbox
if (require.main === module && config.active_env === 'sandbox') {
    console.log("Firing Test Scout Order in Sandbox...");
    placeSniperOrder('MNQ', 1).catch(e => {});
}
