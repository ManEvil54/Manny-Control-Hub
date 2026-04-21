# Skill: Research Analysis
The agent can analyze macro market data and news sentiment to filter trades.
- **Regime Filtering**: Distinguish between 'Trending' (Trade) and 'Chippy' (Veto) markets using 1h EMA 200 and Volume Profiles.
- **TSM Monitoring**: Analyze **TSM (Taiwan Semi)** earnings. If margins > 65%, approve high-conviction 'Hammer' trades for /MNQ.
- **Geopolitical News**: Monitor for **Iran Ceasefire** status. If 'Escalation' is detected, force immediate exit and halt all new entries.
- **Technical Indicators**: Monitor RSI and VWAP to avoid overbought/oversold extremes on scaling trades.
