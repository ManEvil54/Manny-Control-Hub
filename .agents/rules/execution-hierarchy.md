# Execution Hierarchy

## Core Protocols

1. **Strategic Veto Power**
   - **MASI**: Can LOCK execution if /ES and /NQ diverge from VWAP.
   - **LANCE**: Can ABORT scale-in if volume stalls during a trendline break.

2. **Setup Priority**
   - **TSM Golden Setup**: Priority #1. Requires 9:35 AM ORB + FVG + Little RZY Trendline Break.

## Emergency Defense & News Catalyst

- **Immediate Market Exit Rule**:
  If a News Catalyst (via Context Agent) triggers a 1-minute drop > 0.5% of index value, the **Lance Agent** has the authority to bypass the Marci Target and execute an **IMMEDIATE Market Sell** of all positions.
