# Project Style Guide
- **Backend**: Python (Firebase Cloud Functions Gen 2).
- **Frontend**: React (Manny Control Hub style).
- **State Management**: Firestore for real-time synchronization.
- **Naming Conventions**:
    - Python: `snake_case` for functions and variables.
    - React: `PascalCase` for components, `camelCase` for hooks and props.
- **Communication**: Use Webhooks for TradingView integration to minimize latency and cost.
- **Security**: Use secret keys (e.g., `MANNY_SNIPER_2026`) for all webhook endpoints.
