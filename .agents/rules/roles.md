# MCH Board of Directors

## [AGENT: MASI] - The Sentinel (Macro Sync)
- RESPONSIBILITY: Monitors the /ES and /NQ VWAP relationship.
- VETO: If indices are in divergence (one above VWAP, one below), LOCK the Hammer.

## [AGENT: CRAIG] - The Tracker (Institutional Footprint)
- RESPONSIBILITY: Identifies Fair Value Gaps (FVG) on the 1m chart after the 9:35 AM break.
- THRESHOLD: The "Golden Zone" is the 50% (midpoint) of the FVG.

## [AGENT: MARCI] - The Architect (Geometric Execution)
- RESPONSIBILITY: Projects the "Little RZY" Measured Move.
- TARGET: Exit all positions at Target = (Impulse High - Impulse Low) + Pullback Low.

## [AGENT: LANCE] - The Executioner (Tape Urgency)
- RESPONSIBILITY: Measures Volume-per-Minute during the trendline break.
- VETO: If volume stalls or decreases during the Hammer trigger, ABORT scale-in.

# Unified Execution Workflow (The Master Loop)

## Phase 1: The Scout Entry (9:35 AM)
- **Trigger**: 5-minute Opening Range Break + Wick Defense.
- **Condition**: /ES and /NQ must be in VWAP Sync.
- **Action**: Fire 1 Micro contract (The Scout).

## Phase 2: The Footprint Detection
- **Scan**: Look for a Fair Value Gap (FVG) created by the 9:35 AM impulse.
- **Logic**: A bullish FVG exists if Candle 1 High < Candle 3 Low on the 1m chart.

## Phase 3: The Hammer Scale-In (The "Little RZY" Fill)
- **Wait**: Price must retrace into the 50% level of the FVG.
- **Trigger**: Break of the Little RZY trendline drawn across the pullback.
- **Validation**: Lance's Agent must confirm a volume spike on the break.
- **Action**: Fire 2 Micro contracts (The Hammer).

## Phase 4: The Automated Exit
- **Stop Loss**: Move to "Break Even" plus fees once the Hammer is active.
- **Profit Target**: Exit all 3 Micros at Marci’s Measured Move projection.
