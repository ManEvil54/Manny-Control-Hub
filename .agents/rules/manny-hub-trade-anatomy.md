# Rule: Manny Hub Trade Anatomy (Little RZY)

This rule defines the "Little RZY" strategy, a three-leg geometry for scaling into futures trades and managing exits.

## 1. Strategy Legs (A-B-C-D)

- **Leg A-B (The Impulse)**: 
    - **Trigger**: 9:35 AM Sniper breakout.
    - **Action**: Fire **Scout** entry (1 Micro).
    - **Point A**: The session low identified between 9:30 AM and 9:35 AM.
    - **Point B**: The high reached during the initial impulse move.

- **Leg B-C (The "Rizzy" Pullback)**:
    - **Behavior**: The market "breathes" after the impulse.
    - **Oracle Action**: Draw a trendline across the highs of this pullback.
    - **Validation**: Only valid if `/MNQ` and `/MES` are in **VWAP Sync**.

- **Leg C-D (The Hammer)**:
    - **Trigger**: Price breaks the trendline drawn by the Oracle.
    - **Action**: Fire **Scale-in** (Add 2 Micros).
    - **Validation**: Veto if there is a **Volume Stall** at the break.

## 2. The "Measured Move" Exit Rule

Once the **Hammer** (Scale-in) is live, the bot must automatically manage the exit based on the "Little RZY" geometry:

### Profit Target (Leg C-D)
The distance of Leg C-D is mathematically expected to equal Leg A-B.
- **Formula**: `Target = BreakoutPrice + (ImpulseHigh - ImpulseLow)`
- **Action**: Set an automatic Limit Order at this price. This is the "Anti-Greed" tool to lock in profits.

### Dynamic Stop-Loss (The Rizzy Guard)
- **Action**: Immediately move the Stop-Loss to the **Point C** (the "Rizzy" pullback low) as soon as the Hammer is triggered.
- **Purpose**: Protect the Scout position and the new Hammer size by trailing the stop to the most recent structural low.

## 3. Validation Logic

- **Masi's Anchor**: Confirm VWAP Sync between /MNQ and /MES before recognizing the B-C pullback.
- **Lance's Fuse**: No Volume Stall allowed on the trendline break. If volume dies, cancel the Hammer scale-in.
