# Skill: Tradovate Execution
The agent can handle futures orders via the Tradovate REST API.
- **Order Placement**: Uses `POST /order/placeorder` with OAuth2 authentication.
- **Hybrid Logic**:
    - Manage trade tiers (Scout, Scaling, Max Conviction).
    - Apply dynamic wick defense and position sizing.
- **Firestore Sync**: Update `bot_status/futures_sniper` document after every execution.
- **Connection**: Uses `https://live.tradovateapi.com/v1` (or simulation environment for testing).
