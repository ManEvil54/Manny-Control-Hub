# Workflow: /deploy-sniper
This workflow initializes the MCH-Futures-Sniper environment.
1. **Initialize Firebase**: Set up Cloud Functions in `functions/` and Hosting for the dashboard.
2. **Configure API Keys**: Ensure Tradovate credentials and Firestore project IDs are correctly set.
3. **Deploy Webhook**: Deploy the `tradovate_webhook` function to Firebase.
4. **Sync Dashboard**: Deploy the React MCH Dashboard components to Firebase Hosting.
5. **Security Check**: Verify that the TradingView Webhook secret matches the `MANNY_SNIPER_2026` key.
