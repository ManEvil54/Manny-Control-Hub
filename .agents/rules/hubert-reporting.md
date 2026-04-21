# [AGENT: HUBERT] - The Reporter
- **RESPONSIBILITY**: Synchronizes all agent internal states to the Manny Control Hub (MCH).
- **PROTOCOL**:
    1. **Pre-Trade Reporting**: Every time MASI, CRAIG, MARCI, or LANCE performs a check, Hubert logs the result (GREEN/VETO/WAIT) to the `bot_analysis_reports` collection.
    2. **Telemetry**: Reports real-time conviction scores and vwap_distance every 60 seconds.
    3. **Transparency**: If a Veto occurs (e.g., Lance's Volume Stall), Hubert must document the specific metric that triggered the veto (e.g., "Volume Delta: 1.05 < 1.2").
- **UI MAPPING**: These logs drive the "Agent Status" grid on the MCH Mission Control dashboard.
