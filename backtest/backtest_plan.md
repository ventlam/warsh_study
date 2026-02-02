# Warsh Framework Historical Backtest Plan

**Created**: 2026-02-02
**Period**: 2021-01 to 2024-12 (4 years)
**Goal**: Validate framework effectiveness with real market data

---

## Objective

Quantify whether the Warsh investment framework would have generated +5-7% annual alpha vs 60/40 benchmark during 2021-2024, particularly during the 2021-2022 inflation cycle.

---

## Test Period Rationale

**2021-2024 chosen because**:
- ✅ Includes critical 2021-22 inflation cycle (Warsh warned, Fed delayed)
- ✅ Multiple scenario transitions (A1 → A2 → B1)
- ✅ Real stress test (9.1% peak CPI, -18% SPY in 2022)
- ✅ Recent data = most relevant to current regime

---

## Data Requirements

### Macro Signals (Monthly)
- **CPI**: FRED CPIAUCSL (headline, YoY%)
- **Core CPI**: FRED CPILFESL
- **GDP**: FRED GDP (quarterly, interpolate monthly)
- **Unemployment**: FRED UNRATE
- **Fed Balance Sheet**: FRED WALCL (weekly → monthly avg)

### Asset Prices (Daily → Monthly)
- **SPY**: S&P 500 ETF (equity benchmark)
- **TLT**: 20Y+ Treasury ETF (long duration)
- **IEF**: 7-10Y Treasury ETF (intermediate duration)
- **TBT**: 2x Short 20Y Treasury (short duration tool)
- **DXY**: US Dollar Index
- **HYG**: High Yield Corporate Bond ETF (credit)
- **GLD**: Gold ETF
- **Cash**: 0% (assume money market = 0 for simplicity, or FRED DFF/12)

---

## Methodology

### Phase 1: Scenario Identification (Monthly)

For each month (2021-01 to 2024-12):

**Step 1: Calculate indicators**
```
CPI YoY = (CPI_t / CPI_t-12) - 1
Unemployment = UNRATE
GDP growth (trailing 4Q) = estimated
Panic indicators = check 6 metrics
```

**Step 2: Map to scenario**
```
IF CPI >5% AND Unemployment <5% → A1 (High inflation + Stable growth)
IF CPI >5% AND Unemployment >5.5% → A2 (High inflation + Weak growth)
IF CPI 2-4% AND Unemployment <5% → B1 (Soft landing)
IF CPI <3% AND Unemployment >5.5% → B2 (Disinflationary recession)
IF 2+ panic indicators → C1 (Liquidity shock)
IF Credit spreads >300bp (no panic) → C2 (Credit shock)
```

**Step 3: Check for Warsh public statements**
- 2021-06: WSJ op-ed warning
- 2021-12: "Fed is culprit"
- Mark these months with "Warsh dissent" flag

---

### Phase 2: Portfolio Construction (Monthly Rebalance)

**Scenario A1 allocation** (High inflation + Stable growth):
```
SPY:   50% (vs 60/40's 60%)
TLT:  -20% (short duration via TBT or futures)
IEF:    0%
Cash:  40%
DXY:  +10% (long USD)
HYG:    0% (avoid credit)
GLD:   20%
```

**Scenario B1 allocation** (Soft landing):
```
SPY:   70%
TLT:   10%
IEF:   10%
Cash:   10%
DXY:    0%
HYG:    0%
GLD:    0%
```

(Define all 6 scenarios)

**Rebalancing rules**:
- Rebalance at month-end
- Transaction costs = 0.1% per trade (assume)
- Slippage = 0 (simplification)

---

### Phase 3: Benchmark Portfolios

**60/40 Traditional**:
- 60% SPY, 40% IEF
- Rebalance quarterly

**100% SPY**:
- Buy and hold

**Warsh Framework (Dynamic)**:
- Scenario-based allocation
- Monthly rebalance

---

### Phase 4: Performance Metrics

Calculate monthly returns, then compute:

1. **Annual Returns** (CAGR)
2. **Volatility** (annualized std dev)
3. **Sharpe Ratio** (return / volatility, assume Rf=0)
4. **Max Drawdown** (peak to trough)
5. **Calmar Ratio** (return / max drawdown)
6. **Alpha** (Warsh - 60/40)
7. **Win Rate** (% months beating 60/40)

**Critical Year Analysis**:
- 2022 return (the test year where Warsh warned early)

---

## Expected Outcomes

### Hypothesis
- **2021**: Warsh framework raises cash early (~Jun when CPI >5%)
  - Expected: Underperform in H1 (stocks still rising)
  - Expected: Outperform in H2 (start of selloff)

- **2022**: Warsh framework short duration + underweight equity
  - Expected: Significantly outperform (60/40 down ~18%, SPY down ~18%)
  - Target: Warsh down only 0-5%

- **2023-2024**: Warsh framework gradually re-risk
  - Expected: Underperform rally (cautious positioning)
  - But lower volatility

**Overall (2021-2024)**:
- Warsh CAGR: 5-8%
- 60/40 CAGR: 2-4%
- Alpha: +3-4%
- Sharpe: Warsh 0.7-0.9 vs 60/40 0.3-0.5

---

## Success Criteria

**Must achieve**:
- ✅ Alpha >3% annually (vs 60/40)
- ✅ Max drawdown <15% (vs 60/40's ~20%)
- ✅ 2022 return >-5% (vs 60/40's ~-18%)

**Nice to have**:
- ✅ Sharpe ratio >0.7
- ✅ Win rate >55% (months beating 60/40)
- ✅ Positive skew (avoid fat tails)

**Failure conditions**:
- ❌ Alpha <1%
- ❌ Max drawdown >60/40
- ❌ 2022 worse than 60/40

---

## Risk Factors

**Things that could invalidate the test**:
1. **Look-ahead bias**: Using CPI data before public release
   - Mitigation: Use release dates (CPI for Jan published ~Feb 10)

2. **Overfitting**: Designing allocation to fit historical data
   - Mitigation: Allocations based on pre-defined framework, not optimized

3. **Execution impossibility**: Can't actually short TLT in size
   - Mitigation: Note this in limitations

4. **Transaction costs**: Frequent rebalancing expensive
   - Mitigation: Include 0.1% cost estimate

---

## Timeline

**Phase 1**: Data collection (30 min)
**Phase 2**: Scenario mapping (1 hour)
**Phase 3**: Portfolio simulation (1 hour)
**Phase 4**: Performance analysis (30 min)

**Total**: 3 hours

---

## Deliverables

1. **backtest_data.csv**: Monthly data (CPI, prices, scenarios)
2. **backtest_results.csv**: Monthly returns by strategy
3. **backtest_report.md**: Full analysis with charts
4. **backtest_critique.md**: Honest assessment of limitations

---

## Next Steps After Backtest

**If successful (Alpha >3%)**:
- ✅ Proceed to Task #2 (Dashboard)
- ✅ Begin paper trading (2026-02 onwards)
- ✅ Refine edge case rules

**If marginal (Alpha 1-3%)**:
- ⚠️ Adjust thresholds
- ⚠️ Try different rebalancing frequencies
- ⚠️ Re-run backtest

**If failed (Alpha <1%)**:
- ❌ Deep dive into failure months
- ❌ Re-examine core assumptions
- ❌ Consider framework revision or pause

---

**Status**: Planning complete, ready to execute
