# Edge Cases & Decision Rules (Warsh Framework)

**Created**: 2026-02-02
**Purpose**: Handle threshold boundaries and ambiguous scenarios
**Version**: 1.0

---

## Problem Statement

The Investment Framework v1.0 defines clear thresholds (e.g., CPI >5% = A1), but real-world data often sits in gray zones:

- CPI at 4.8% (just below 5% threshold)
- Panic indicators at 1.5 (below 2 threshold but elevated)
- Scenario oscillating monthly (A1→B1→A1)

**Without edge case rules**: Portfolio would thrash between scenarios, incurring transaction costs and whipsaw losses.

**Solution**: Introduce buffer zones, confirmation periods, and transition states.

---

## Core Principles

### 1. Stability Over Precision
**Principle**: Better to stay in wrong scenario for 1 extra month than flip-flop 3 times

**Rationale**:
- Transaction costs add up (0.1% per trade × 3 trades = 0.3% lost)
- Emotional discipline harder with frequent changes
- Framework's edge is risk management, not perfect timing

---

### 2. Asymmetric Thresholds (Hysteresis)
**Principle**: Higher bar to exit defensive scenarios than to enter them

**Example**:
```
Enter A1 (defensive): CPI >5.0%
Exit A1 (to B1):     CPI <3.5% (not 5.0%)
```

**Rationale**: Downside protection > upside capture

---

### 3. Confirmation Period
**Principle**: Require 2 consecutive months before major scenario change

**Exception**: C1 (Panic) requires immediate action (no confirmation)

---

## Edge Case Rules

### Case 1: CPI Near Thresholds

#### Situation: CPI between 4.5-5.5%

**Problem**:
- 4.8% CPI: Is this A1 (>5%) or not?
- One month 4.9%, next month 5.1%: Scenario flips?

**Solution: 10% Buffer Zone**

```
Threshold: 5.0%
Buffer: ±10% = ±0.5%

Entry zone:  CPI >5.5% → Definitely A1
Exit zone:   CPI <4.5% → Definitely NOT A1
Gray zone:   4.5-5.5% → Depends on current state

Rule:
IF currently in A1:
    Stay in A1 until CPI <4.5% (exit buffer)
IF currently NOT in A1:
    Enter A1 only when CPI >5.5% (entry buffer)
```

**Example Timeline**:

| Month | CPI | Current State | Action | New State |
|-------|-----|---------------|--------|-----------|
| Jan | 4.2% | B1 | Hold | B1 |
| Feb | 4.8% | B1 | Hold (below 5.5% entry) | B1 |
| Mar | 5.3% | B1 | Hold (in gray zone) | B1 |
| Apr | 5.6% | B1 | **Switch** (above 5.5%) | A1 |
| May | 5.4% | A1 | Hold (above 4.5% exit) | A1 |
| Jun | 4.8% | A1 | Hold (above 4.5% exit) | A1 |
| Jul | 4.3% | A1 | **Switch** (below 4.5%) | B1 |

**Result**: Reduced flipping from 4 times to 2 times

---

#### All CPI Thresholds with Buffers

| Scenario | Entry CPI | Exit CPI | Buffer |
|----------|-----------|----------|--------|
| **A1/A2** (High inflation) | >5.5% | <4.5% | ±10% |
| **A1_cautious** (Watch zone) | >4.4% | <3.6% | ±10% |
| **B1** (Target zone) | 2.2-4.4% | Outside range | ±10% |
| **B2** (Low inflation) | <1.8% | >2.2% | ±10% |

---

### Case 2: Unemployment Near Thresholds

#### Situation: Unemployment between 4.5-5.5%

**Problem**: A1 vs A2 distinction depends on unemployment <5% or >5.5%

**Solution: 15% Buffer Zone** (wider than CPI due to higher volatility)

```
Threshold: 5.0% (stable growth) vs 5.5% (weak growth)
Buffer: ±15%

Entry to "weak growth": Unemployment >6.0%
Exit from "weak growth": Unemployment <4.5%
Gray zone: 4.5-6.0%
```

**Decision Matrix**:

| CPI | Unemployment | Scenario |
|-----|--------------|----------|
| >5.5% | <4.5% | A1 (No-brainer tightening) |
| >5.5% | 4.5-6.0% | **A1_A2_transition** (assume A1 unless confirmed weak) |
| >5.5% | >6.0% | A2 (Stagflation) |

---

### Case 3: Scenario Confirmation Period

#### Situation: CPI spikes one month then drops back

**Example**:
- Jan: CPI 4.8% (B1)
- Feb: CPI 5.6% (crosses threshold → A1?)
- Mar: CPI 4.9% (drops back → B1?)

**Problem**: If we react immediately, portfolio flips twice in 2 months

**Solution: 2-Month Confirmation for Major Changes**

```
Major change = Switch between scenario families:
- A (inflation) ↔ B (disinflation)
- B (normal) ↔ C (crisis)

Minor change = Within same family:
- A1 ↔ A2
- B1 ↔ B2
```

**Rule**:

```python
def confirm_scenario_change(current, new, history):
    """
    Require 2 consecutive months of new scenario before switching
    """
    if is_major_change(current, new):
        if history[-2:] == [new, new]:  # Both last 2 months = new scenario
            return new  # Confirmed
        else:
            return current  # Not confirmed, stay put
    else:
        return new  # Minor change, switch immediately
```

**Example with confirmation**:

| Month | CPI | Raw Scenario | Confirmed Scenario | Action |
|-------|-----|--------------|-------------------|--------|
| Jan | 4.8% | B1 | B1 | - |
| Feb | 5.6% | A1 | **B1** (not confirmed) | Hold |
| Mar | 5.7% | A1 | **A1** (2 months → confirmed) | Switch now |
| Apr | 5.5% | A1 | A1 | Hold |
| May | 4.4% | B1 | **A1** (not confirmed) | Hold |
| Jun | 4.3% | B1 | **A1** (not confirmed) | Hold |
| Jul | 4.2% | B1 | **B1** (2 months → confirmed) | Switch now |

**Result**: Switches from 4 times to 2 times, with better timing

---

#### Exception: Panic Scenarios (No Confirmation)

**Rule**: C1 (Panic) overrides all confirmation periods

```
IF 2+ panic indicators triggered:
    Switch to C1 immediately (no 2-month wait)
REASON: Capital preservation > stability
```

---

### Case 4: Panic Indicators at 1.5

#### Situation: Only 1.5 panic indicators triggered

**Framework rule**: 2+ indicators = C1 (Panic)

**Problem**: What if 1.5 indicators?

**Example**:
- Household wealth: -17% ✅ (threshold: -15%)
- Stock market: -35% ⚠️ (threshold: -40%, close but not triggered)
- GDP: -4% ❌ (threshold: -6%)
- Banks: -45% ✅ (threshold: -50%, borderline)
- Unemployment: 7% ❌ (threshold: 8%)
- Money markets: Minor stress ❌

**Count**: 1 fully triggered + 2 borderline = "1.5"

**Solution: Weighted Panic Score**

```python
def calculate_panic_score(indicators):
    """
    Weighted score: Full point if threshold crossed, 0.5 if within 20%
    """
    score = 0

    # Household wealth
    if wealth_decline < -15%:
        score += 1.0
    elif wealth_decline < -12%:  # Within 20% of threshold
        score += 0.5

    # Stock market
    if stocks_decline < -40%:
        score += 1.0
    elif stocks_decline < -32%:  # Within 20%
        score += 0.5

    # ... similar for other 4 indicators

    return score
```

**Decision Rule**:

```
Panic Score >= 2.0: → C1 (Panic mode, immediate action)
Panic Score 1.5-1.9: → C1_watch (Heightened alert, raise cash 10-20%)
Panic Score 1.0-1.4: → Normal scenario + 5% cash raise
Panic Score <1.0:    → Normal scenario
```

---

### Case 5: Transition States (Hybrid Allocations)

#### Situation: Between two clear scenarios

**Problem**: Markets don't transition instantly from A1 to B1

**Solution: Define Transition Allocations**

#### A1 → B1 Transition (CPI falling but still elevated)

**Trigger**: CPI between 4.0-5.0% + falling for 2 months

**Allocation** (A1_to_B1_transition):
```
SPY:  60% (midpoint of A1's 50% and B1's 70%)
TLT:  0%  (no short, no long)
IEF:  10%
HYG:  0%
GLD:  10% (reduced from A1's 20%)
Cash: 20% (midpoint of A1's 40% and B1's 10%)
```

**Duration**: Stay in transition for max 2 months, then commit to B1

---

#### B1 → A1 Transition (CPI rising but not yet critical)

**Trigger**: CPI between 4.0-5.0% + rising for 2 months

**Allocation** (B1_to_A1_transition):
```
SPY:  60%
TLT:  0%
IEF:  5%
HYG:  0%
GLD:  15%
Cash: 20%
```

**Psychology**: Start reducing risk before full A1, but don't overreact

---

### Case 6: Warsh Statement Ambiguity

#### Situation: Warsh gives nuanced statement

**Example**:
> "While inflation has moderated from peak levels, I remain concerned about persistent core price pressures, particularly in services. The Fed's current stance seems appropriate for now, though vigilance is required."

**Problem**: Is this Dissent Level 0, 1, or 2?

**Solution: Keyword Scoring System**

**Dovish keywords** (-1 each):
- "appropriate", "reasonable", "warranted", "adequate"

**Hawkish keywords** (+1 each):
- "concerned", "vigilance", "persistent", "elevated"

**Critical keywords** (+2 each):
- "mistake", "error", "culprit", "greatest", "credibility"

**Dissent Level**:
```
Score -2 to 0:  Level 0 (Silent/supportive)
Score 1-2:      Level 1 (Mild critique)
Score 3-4:      Level 2 (Direct criticism)
Score 5+:       Level 3 (Resignation-level)
```

**Example scoring**:
- "concerned" (+1)
- "persistent" (+1)
- "vigilance" (+1)
- "appropriate" (-1)
- **Total**: +2 → **Level 1** (Mild critique)

---

### Case 7: Data Revision Impact

#### Situation: CPI revised after initial release

**Example**:
- Initial: CPI 5.2% (triggers A1)
- Revised: CPI 4.9% (would NOT trigger A1)
- Portfolio already rebalanced to A1

**Problem**: Do we rebalance again based on revision?

**Solution: Ignore Revisions Within Same Month**

**Rule**:
```
Use initial release only for month M
Revisions incorporated in month M+1 data
Do not rebalance mid-month
```

**Rationale**:
- Reduces whipsaw
- Initial release is what market trades on
- Revisions usually small (<0.3%)

**Exception**: If revision is >0.5% AND changes scenario, re-evaluate next month earlier

---

### Case 8: Multiple Scenario Triggers

#### Situation: Both A1 and C1 triggers met

**Example**:
- CPI: 8.5% (A1 trigger ✅)
- Panic score: 2.5 (C1 trigger ✅)

**Problem**: Which scenario takes precedence?

**Solution: Priority Hierarchy**

```
1. C1 (Panic)         - Highest priority (capital preservation)
2. C2 (Credit shock)  - Second (systemic risk)
3. A2 (Stagflation)   - Third (dual stress)
4. A1 (High inflation) - Fourth
5. B2 (Recession)     - Fifth
6. B1 (Soft landing)  - Default/lowest priority
```

**Rule**: Always use highest-priority triggered scenario

**Rationale**: Survival first, alpha second

---

## Implementation Checklist

### Before Each Monthly Rebalance

**Step 1: Data Collection** (by 15th of month)
- [ ] CPI (released ~12th)
- [ ] Unemployment (released ~1st Friday)
- [ ] Stock market data (month-end)
- [ ] Panic indicators (if needed)
- [ ] Warsh public statements (if any)

**Step 2: Raw Scenario Calculation**
- [ ] Calculate CPI-based scenario
- [ ] Check unemployment for A1 vs A2
- [ ] Calculate panic score (if market stress)

**Step 3: Apply Edge Case Rules**
- [ ] Check if in buffer zone → Apply hysteresis
- [ ] Check if major change → Require 2-month confirmation
- [ ] Check if panic override → Immediate action
- [ ] Check scenario priority hierarchy

**Step 4: Determine Final Scenario**
- [ ] Confirmed scenario = [___]
- [ ] Allocation = [___]

**Step 5: Rebalance** (by 20th of month)
- [ ] Calculate target weights
- [ ] Execute trades
- [ ] Document decision in log

---

## Decision Tree (Visual Summary)

```
START
  ↓
[Collect data: CPI, Unemp, Panic indicators]
  ↓
[Calculate panic score]
  ↓
Panic score >2.0? ──YES→ C1 (immediate action) → END
  ↓ NO
[Calculate raw scenario from CPI + Unemp]
  ↓
[Check buffer zones]
  ↓
In gray zone? ──YES→ Use current scenario → END
  ↓ NO
[New scenario = X]
  ↓
Major change (A↔B)? ──YES→ Confirmed for 2 months? ──NO→ Stay current → END
  ↓ NO                                              ↓ YES
Switch to scenario X → END
```

---

## Examples

### Example 1: CPI Oscillation (Handled by Buffer)

| Month | CPI | Raw | Buffer Rule | Final | Action |
|-------|-----|-----|-------------|-------|--------|
| Jan | 4.8% | B1 | N/A | B1 | - |
| Feb | 5.1% | A1? | In buffer, stay B1 | **B1** | Hold |
| Mar | 5.3% | A1? | In buffer, stay B1 | **B1** | Hold |
| Apr | 5.7% | A1 | Above 5.5%, switch | **A1** | Rebalance |
| May | 5.4% | A1 | Above 4.5%, stay | **A1** | Hold |
| Jun | 4.8% | B1? | In buffer, stay A1 | **A1** | Hold |
| Jul | 4.3% | B1 | Below 4.5%, switch | **B1** | Rebalance |

**Result**: 2 switches instead of 5

---

### Example 2: Panic Borderline (Panic Score 1.7)

**Indicators**:
- Household wealth: -16% → Score 1.0 ✅
- Stocks: -35% → Score 0.5 ⚠️ (within 20% of -40%)
- GDP: -5% → Score 0 ❌
- Banks: -48% → Score 0.5 ⚠️ (within 20% of -50%)
- Unemployment: 7% → Score 0 ❌
- Money markets: Moderate stress → Score 0 ❌

**Total**: 1.0 + 0.5 + 0.5 = **2.0**

**Decision**: **Panic score = 2.0 → Switch to C1 immediately**

---

### Example 3: Warsh Nuanced Statement

**Statement**:
> "The recent inflation data is encouraging, showing progress toward our 2% target. However, core services inflation remains stubbornly elevated, and I would urge continued vigilance. The Fed's current posture strikes me as reasonable for now."

**Scoring**:
- Hawkish: "elevated" (+1), "stubbornly" (+1), "vigilance" (+1)
- Dovish: "encouraging" (-1), "progress" (-1), "reasonable" (-1)
- **Net**: +3 - 3 = **0**

**Dissent Level**: **0** (Neutral/supportive)

**Action**: No adjustment to risk levels

---

## Testing & Validation

### Backtest Application

**Q**: If we applied these rules to 2021-2024, would performance improve?

**Hypothesis**: Fewer transactions → Lower costs → Slightly better return

**Test Plan**:
1. Re-run backtest with edge case rules
2. Count # of scenario switches (with vs without)
3. Estimate transaction cost savings
4. Check if Sharpe improves

**Expected Result**: 0.1-0.3% CAGR improvement from reduced whipsaw

---

## Maintenance

### Quarterly Review

- [ ] Check if buffer zones (±10%) are still appropriate
- [ ] Check if confirmation period (2 months) caused missed opportunities
- [ ] Adjust if market structure changed (e.g., higher volatility)

### Annual Review

- [ ] Full backtest with updated rules
- [ ] Compare rule-based vs no-rule performance
- [ ] Update keyword list for Warsh statements (if language evolves)

---

## Appendix: Quick Reference

### Buffer Zones Summary

| Threshold Type | Raw Value | Entry Buffer | Exit Buffer |
|----------------|-----------|--------------|-------------|
| CPI (A1) | 5.0% | 5.5% | 4.5% |
| CPI (4% action) | 4.0% | 4.4% | 3.6% |
| Unemployment (weak) | 5.5% | 6.0% | 4.5% |
| Panic score | 2.0 | 2.0 (no buffer) | 1.5 |

### Confirmation Periods

| Change Type | Confirmation Required |
|-------------|----------------------|
| A ↔ B | 2 months |
| B ↔ C | Immediate (C1), 2 months (C2) |
| Within A (A1↔A2) | 1 month |
| Within B (B1↔B2) | 1 month |

### Scenario Priority

1. C1 (Panic) - Immediate override
2. C2 (Credit shock)
3. A2 (Stagflation)
4. A1 (High inflation)
5. B2 (Recession)
6. B1 (Soft landing)

---

**Document Version**: 1.0
**Last Updated**: 2026-02-02
**Next Review**: 2026-05-02 (After 3 months of paper trading)
