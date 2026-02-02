# Monthly Rebalancing Checklist

**Purpose**: Operational guide for monthly portfolio rebalancing
**Time Required**: 30-60 minutes
**Schedule**: Around 15th of each month (after CPI release)

---

## Quick Start

**3-Step Process**:
1. Collect data (15 min)
2. Identify scenario (10 min)
3. Rebalance portfolio (30 min)

---

## Step 1: Data Collection (Due: ~15th of month)

### Required Data Points

| Data | Source | Typical Release | Value |
|------|--------|-----------------|-------|
| **CPI YoY%** | [FRED CPIAUCSL](https://fred.stlouisfed.org/series/CPIAUCSL) | ~12th | ____% |
| **Unemployment Rate** | [FRED UNRATE](https://fred.stlouisfed.org/series/UNRATE) | 1st Friday | ____% |
| **SPY Price** (month-end) | Yahoo Finance | End of month | $____ |
| **Warsh Statement?** | Google News / WSJ | Varies | Yes/No |

### Optional (Only if market stress)

| Panic Indicator | Data Source | Threshold | Actual | Triggered? |
|-----------------|-------------|-----------|--------|------------|
| Household wealth | Fed Z.1 Report | <-15% | ____% | ☐ |
| Stock market decline | SPY YoY | <-40% | ____% | ☐ |
| Bank stocks | KBW Index | <-50% | ____% | ☐ |
| Unemployment spike | FRED | >8% rapid | ____% | ☐ |

---

## Step 2: Scenario Identification (10 min)

### 2a. Calculate Raw Scenario

Use this decision tree:

```
Is Panic Score >2.0? ──YES→ C1 (Panic) → STOP
  ↓ NO
Is CPI >5.5%?
  ↓ YES
  Is Unemployment >6.0%? ──YES→ A2 (Stagflation)
  ↓ NO
  A1 (High inflation)

↓ (CPI ≤5.5%)
Is CPI 4.4-5.5%?
  ↓ YES → A1_cautious OR B1_watch (depends on trend)

Is CPI 2.2-4.4%? ──YES→ B1 (Soft landing)

Is CPI <2.2%?
  ↓ YES
  Is Unemployment >5.5%? ──YES→ B2 (Recession)
  ↓ NO
  B1 (Low inflation, stable)
```

**Raw Scenario**: ________

---

### 2b. Apply Edge Case Rules

#### Buffer Zone Check

**Current scenario** (from last month): ________

| Check | Rule | Result |
|-------|------|--------|
| Is CPI in buffer zone (4.5-5.5%)? | If yes, stay in current scenario | ☐ Stay / ☐ Switch |
| Is Unemployment in buffer (4.5-6.0%)? | Use midpoint assumption | ☐ Stable / ☐ Weak |

**After buffer check**: ________

---

#### Confirmation Check (Only if scenario changed)

| Check | Answer |
|-------|--------|
| Did scenario change from last month? | ☐ Yes ☐ No |
| Is it a major change (A↔B or B↔C)? | ☐ Yes ☐ No |
| Has new scenario persisted for 2+ months? | ☐ Yes ☐ No |

**Confirmation rule**:
```
IF major change AND not confirmed (2+ months)
THEN Stay in current scenario
ELSE Proceed to new scenario
```

**Final Scenario**: ________

---

### 2c. Warsh Statement Adjustment (If applicable)

**Did Warsh make public statement this month?**
- ☐ No → Skip this section
- ☐ Yes → Analyze below

**Statement keywords**:
- Hawkish (+): ______________________________
- Dovish (-): ________________________________
- Critical (++): _____________________________

**Dissent Level**: 0 / 1 / 2 / 3

**Adjustment**:
- Level 0-1: No change
- Level 2: Reduce risk by 10-20%
- Level 3: Reduce risk by 30-50%

---

## Step 3: Portfolio Allocation (30 min)

### 3a. Lookup Target Allocation

**Scenario**: ________ → Go to allocation table below

### Allocation Tables

#### A1: High Inflation + Stable Growth (Defensive)
```
SPY:  50%
TLT: -10% (or 0% if short not feasible)
IEF:   0%
HYG:   0%
GLD:  20%
Cash: 40%
```

#### A1_cautious: Entering High Inflation
```
SPY:  55%
TLT:   0%
IEF:   5%
HYG:   0%
GLD:  15%
Cash: 25%
```

#### A2: Stagflation (Maximum Defense)
```
SPY:  40%
TLT:   0%
IEF:  10%
HYG:   0%
GLD:  30%
Cash: 20%
```

#### B1: Soft Landing (Risk On)
```
SPY:  70%
TLT:   5%
IEF:  10%
HYG:   5%
GLD:   0%
Cash: 10%
```

#### B2: Disinflationary Recession
```
SPY:  50%
TLT:  20%
IEF:  20%
HYG:   0%
GLD:   0%
Cash: 10%
```

#### C1: Panic (Capital Preservation)
```
Phase 1 (Panic ongoing):
SPY:  20%
TLT:  30% (flight to safety)
IEF:  20%
HYG:   0%
GLD:   0%
Cash: 30%

Phase 2 (Fed intervening):
SPY:  40%
TLT:  20%
IEF:  20%
HYG:  10%
GLD:   0%
Cash: 10%
```

---

### 3b. Calculate Target Shares

**Portfolio Value**: $________

**Target Weights** (from scenario above):
- SPY:  ____% × $______ = $______
- TLT:  ____% × $______ = $______
- IEF:  ____% × $______ = $______
- HYG:  ____% × $______ = $______
- GLD:  ____% × $______ = $______
- Cash: ____% × $______ = $______

**Current Positions**:
- SPY:  $______
- TLT:  $______
- IEF:  $______
- HYG:  $______
- GLD:  $______
- Cash: $______

**Trades Needed**:
- SPY:  ☐ Buy $______ ☐ Sell $______
- TLT:  ☐ Buy $______ ☐ Sell $______
- IEF:  ☐ Buy $______ ☐ Sell $______
- HYG:  ☐ Buy $______ ☐ Sell $______
- GLD:  ☐ Buy $______ ☐ Sell $______

---

### 3c. Execute Trades

**Execution Date**: ________ (Around 20th of month)

**Order of Execution**:
1. Sell positions (if any) → Raise cash
2. Buy new positions (in order of priority)

**Transaction Costs**:
- Estimated: ______ × 0.1% = $______

---

## Step 4: Documentation

### Monthly Log Entry

**Date**: ________
**Month**: ________

**Data**:
- CPI: _____%
- Unemployment: _____%
- SPY (month-end): $______

**Scenario**:
- Raw: ________
- Confirmed: ________
- Warsh Dissent Level: ____

**Allocation**:
- SPY: ____%
- TLT: ____%
- IEF: ____%
- HYG: ____%
- GLD: ____%
- Cash: ____%

**Trades Executed**:
- [List trades]

**Rationale** (1-2 sentences):
- [Why this scenario? Any edge cases applied?]

---

## Emergency Override

### Panic Checklist (If market crash)

**☐ Step 1**: Calculate panic score immediately (don't wait for month-end)

**☐ Step 2**: If panic score >2.0:
- Switch to C1 Phase 1 allocation immediately
- Raise cash to 30%+
- Buy long-duration Treasuries (TLT)

**☐ Step 3**: Monitor daily until panic score drops below 1.5

**☐ Step 4**: When Fed announces intervention (QE, emergency cuts):
- Shift to C1 Phase 2 allocation
- Start buying risk assets gradually

---

## Monthly Timeline

| Date | Task | Time |
|------|------|------|
| **~5th** | Check unemployment data (1st Friday release) | 5 min |
| **~12th** | Check CPI data | 5 min |
| **~15th** | Complete Steps 1-2 (Data + Scenario) | 25 min |
| **~18th-20th** | Execute Step 3 (Rebalancing) | 30 min |
| **~22nd** | Document in log | 5 min |

**Total time per month**: ~70 minutes

---

## Tips & Best Practices

### 1. Set Calendar Alerts
- 5th: Check unemployment
- 12th: Check CPI
- 15th: Run full checklist

### 2. Stick to the Process
- Don't second-guess scenarios
- Edge cases are there for a reason
- Trust the framework (it backtested well)

### 3. Document Everything
- Keeps you honest
- Allows performance attribution
- Helps refine rules over time

### 4. Don't Overtrade
- Monthly rebalancing is enough
- Avoid reacting to daily noise
- Confirmation periods prevent whipsaw

### 5. Risk Management
- Never skip panic indicator check
- When in doubt, raise cash
- Warsh dissent Level 2+ = serious warning

---

## Troubleshooting

### "CPI is exactly 5.0%" (On threshold)
→ Use buffer rule: Stay in current scenario unless already been 2+ months

### "Scenario says A1 but market rallying hard"
→ Framework prioritizes downside protection, not upside capture. Stay disciplined.

### "Panic score is 1.9" (Just below 2.0)
→ Raise cash by 10-20% as precaution, but don't full C1 until 2.0+

### "Warsh statement is ambiguous"
→ Use keyword scoring. If unclear, default to Level 0-1 (no adjustment)

### "Forgot to rebalance on 20th"
→ Do it ASAP. Don't wait another month.

---

## Contact & Support

**Questions?**
- Review: `frameworks/edge_cases_decision_rules.md`
- Review: `frameworks/2026_02_02_investment_framework_v1.md`
- Review: `backtest/BACKTEST_REPORT.md`

**Framework not working?**
- Check if market structure changed
- Review last 3 months of decisions
- Consider quarterly framework review

---

**Checklist Version**: 1.0
**Last Updated**: 2026-02-02
**Next Review**: After 3 months of usage
