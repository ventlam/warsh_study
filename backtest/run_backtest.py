"""
Backtest Warsh framework vs 60/40 and SPY (2021-2024)
"""

import pandas as pd
import numpy as np

def define_allocations():
    """
    Define asset allocations for each scenario
    Based on Investment Framework v1
    """
    allocations = {
        'A1': {  # High inflation + Stable growth: Aggressive defense
            'SPY': 0.50,   # Reduced equity (vs 60/40's 60%)
            'TLT': -0.10,  # Short duration (simplified, vs 60/40's long)
            'IEF': 0.00,
            'HYG': 0.00,   # Avoid credit
            'GLD': 0.20,   # Inflation hedge
            'Cash': 0.40,  # High cash
        },
        'A1_cautious': {  # Early A1 (CPI 4-5%)
            'SPY': 0.55,
            'TLT': 0.00,
            'IEF': 0.05,
            'HYG': 0.00,
            'GLD': 0.15,
            'Cash': 0.25,
        },
        'A1_A2_transition': {  # Between A1 and A2
            'SPY': 0.45,
            'TLT': -0.05,
            'IEF': 0.00,
            'HYG': 0.00,
            'GLD': 0.20,
            'Cash': 0.40,
        },
        'A2': {  # Stagflation: Maximum defense
            'SPY': 0.40,
            'TLT': 0.00,
            'IEF': 0.10,
            'HYG': 0.00,
            'GLD': 0.30,
            'Cash': 0.20,
        },
        'B1': {  # Soft landing: Risk on but cautious
            'SPY': 0.70,
            'TLT': 0.05,
            'IEF': 0.10,
            'HYG': 0.05,
            'GLD': 0.00,
            'Cash': 0.10,
        },
        'B1_watch': {  # B1 with elevated risk
            'SPY': 0.65,
            'TLT': 0.05,
            'IEF': 0.10,
            'HYG': 0.00,
            'GLD': 0.05,
            'Cash': 0.15,
        },
        'B1_strong': {  # B1 strong
            'SPY': 0.70,
            'TLT': 0.10,
            'IEF': 0.10,
            'HYG': 0.00,
            'GLD': 0.00,
            'Cash': 0.10,
        },
        'B2': {  # Recession: Long duration, defensive equity
            'SPY': 0.50,
            'TLT': 0.20,
            'IEF': 0.20,
            'HYG': 0.00,
            'GLD': 0.00,
            'Cash': 0.10,
        },
    }

    # 60/40 benchmark
    allocations['60/40'] = {
        'SPY': 0.60,
        'TLT': 0.00,
        'IEF': 0.40,
        'HYG': 0.00,
        'GLD': 0.00,
        'Cash': 0.00,
    }

    # 100% SPY benchmark
    allocations['SPY_only'] = {
        'SPY': 1.00,
        'TLT': 0.00,
        'IEF': 0.00,
        'HYG': 0.00,
        'GLD': 0.00,
        'Cash': 0.00,
    }

    return allocations

def calculate_portfolio_returns(prices_df, scenarios_df, allocations):
    """
    Calculate monthly returns for Warsh framework and benchmarks
    """
    # Calculate monthly returns for each asset
    returns = prices_df.pct_change()

    # Initialize portfolio values
    results = []

    # For each month
    for i in range(1, len(returns)):
        date = returns.index[i]
        month_returns = returns.iloc[i]

        # Get scenario for this month
        scenario = scenarios_df.loc[date, 'Scenario']

        # Warsh framework allocation
        warsh_alloc = allocations.get(scenario, allocations['B1'])  # Default to B1 if unknown

        # Calculate portfolio returns
        warsh_return = sum(warsh_alloc.get(asset, 0) * month_returns.get(asset, 0)
                           for asset in ['SPY', 'TLT', 'IEF', 'HYG', 'GLD'])

        # 60/40 benchmark
        bench_60_40_return = (0.60 * month_returns['SPY'] +
                               0.40 * month_returns['IEF'])

        # SPY only
        spy_return = month_returns['SPY']

        results.append({
            'Date': date,
            'Scenario': scenario,
            'Warsh_Return': warsh_return,
            '60/40_Return': bench_60_40_return,
            'SPY_Return': spy_return,
            'CPI_YoY': scenarios_df.loc[date, 'CPI_YoY'],
        })

    return pd.DataFrame(results)

def calculate_performance_metrics(returns_df):
    """
    Calculate key performance metrics
    """
    strategies = ['Warsh_Return', '60/40_Return', 'SPY_Return']
    metrics = {}

    for strategy in strategies:
        returns = returns_df[strategy]

        # Cumulative return
        cum_return = (1 + returns).prod() - 1

        # CAGR (4 years)
        cagr = (1 + cum_return) ** (1/4) - 1

        # Volatility (annualized)
        volatility = returns.std() * np.sqrt(12)

        # Sharpe ratio (assume Rf=0)
        sharpe = cagr / volatility if volatility > 0 else 0

        # Max drawdown
        cum_returns = (1 + returns).cumprod()
        running_max = cum_returns.expanding().max()
        drawdown = (cum_returns - running_max) / running_max
        max_drawdown = drawdown.min()

        # Calmar ratio
        calmar = cagr / abs(max_drawdown) if max_drawdown != 0 else 0

        # Win rate vs 60/40
        if strategy != '60/40_Return':
            win_rate = (returns > returns_df['60/40_Return']).sum() / len(returns)
        else:
            win_rate = np.nan

        metrics[strategy] = {
            'Cumulative Return': cum_return,
            'CAGR': cagr,
            'Volatility': volatility,
            'Sharpe Ratio': sharpe,
            'Max Drawdown': max_drawdown,
            'Calmar Ratio': calmar,
            'Win Rate vs 60/40': win_rate,
        }

    return pd.DataFrame(metrics).T

def main():
    # Load data
    prices = pd.read_csv('backtest/market_data_monthly.csv', index_col='Date', parse_dates=True)
    scenarios = pd.read_csv('backtest/scenarios.csv', index_col='Date', parse_dates=True)

    # Align dates to month-end
    scenarios.index = scenarios.index.to_period('M').to_timestamp('M')
    prices.index = prices.index.to_period('M').to_timestamp('M')

    # Define allocations
    allocations = define_allocations()

    # Calculate returns
    returns_df = calculate_portfolio_returns(prices, scenarios, allocations)

    # Save detailed results
    returns_df.to_csv('backtest/monthly_returns.csv', index=False)

    # Calculate metrics
    metrics_df = calculate_performance_metrics(returns_df)

    # Save metrics
    metrics_df.to_csv('backtest/performance_metrics.csv')

    # Print results
    print("="*80)
    print("WARSH FRAMEWORK BACKTEST RESULTS (2021-2024)")
    print("="*80)

    print("\n" + "="*80)
    print("PERFORMANCE METRICS")
    print("="*80)
    print(metrics_df.to_string())

    # Calculate alpha
    warsh_cagr = metrics_df.loc['Warsh_Return', 'CAGR']
    bench_cagr = metrics_df.loc['60/40_Return', 'CAGR']
    alpha = warsh_cagr - bench_cagr

    print("\n" + "="*80)
    print("KEY FINDINGS")
    print("="*80)
    print(f"\n✓ Warsh Framework CAGR: {warsh_cagr*100:>6.2f}%")
    print(f"✓ 60/40 Benchmark CAGR: {bench_cagr*100:>6.2f}%")
    print(f"✓ Alpha (Warsh - 60/40): {alpha*100:>6.2f}%")

    warsh_sharpe = metrics_df.loc['Warsh_Return', 'Sharpe Ratio']
    bench_sharpe = metrics_df.loc['60/40_Return', 'Sharpe Ratio']
    print(f"\n✓ Warsh Sharpe Ratio: {warsh_sharpe:>6.2f}")
    print(f"✓ 60/40 Sharpe Ratio: {bench_sharpe:>6.2f}")

    warsh_dd = metrics_df.loc['Warsh_Return', 'Max Drawdown']
    bench_dd = metrics_df.loc['60/40_Return', 'Max Drawdown']
    print(f"\n✓ Warsh Max Drawdown: {warsh_dd*100:>6.2f}%")
    print(f"✓ 60/40 Max Drawdown: {bench_dd*100:>6.2f}%")

    # Critical year analysis (2022)
    print("\n" + "="*80)
    print("CRITICAL YEAR: 2022 (Inflation Peak)")
    print("="*80)

    returns_2022 = returns_df[returns_df['Date'].dt.year == 2022]
    warsh_2022 = (1 + returns_2022['Warsh_Return']).prod() - 1
    bench_2022 = (1 + returns_2022['60/40_Return']).prod() - 1
    spy_2022 = (1 + returns_2022['SPY_Return']).prod() - 1

    print(f"\n✓ Warsh Framework 2022: {warsh_2022*100:>6.2f}%")
    print(f"✓ 60/40 Benchmark 2022: {bench_2022*100:>6.2f}%")
    print(f"✓ SPY 2022: {spy_2022*100:>6.2f}%")
    print(f"✓ Outperformance: {(warsh_2022 - bench_2022)*100:>6.2f}%")

    # Success criteria evaluation
    print("\n" + "="*80)
    print("SUCCESS CRITERIA EVALUATION")
    print("="*80)

    criteria = [
        ("Alpha >3%", alpha > 0.03, f"{alpha*100:.2f}%"),
        ("Max DD <15%", warsh_dd > -0.15, f"{warsh_dd*100:.2f}%"),
        ("2022 return >-5%", warsh_2022 > -0.05, f"{warsh_2022*100:.2f}%"),
        ("Sharpe >0.7", warsh_sharpe > 0.7, f"{warsh_sharpe:.2f}"),
    ]

    passed = 0
    for criterion, result, value in criteria:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {criterion:<20} (Actual: {value})")
        if result:
            passed += 1

    print(f"\n{'='*80}")
    print(f"OVERALL: {passed}/{len(criteria)} criteria met")

    if passed >= 3:
        print("✓ FRAMEWORK VALIDATED - Proceed to implementation")
    elif passed >= 2:
        print("⚠ PARTIAL SUCCESS - Consider refinements")
    else:
        print("✗ FRAMEWORK NEEDS REVISION")

    print("="*80)

if __name__ == "__main__":
    main()
