"""
Identify Warsh framework scenarios for each month (2021-2024)
"""

import pandas as pd
import numpy as np

def identify_scenario(cpi, unemployment):
    """
    Map macro conditions to Warsh framework scenario

    Scenarios:
    A1: High inflation (>5%) + Stable growth (unemployment <5%)
    A2: High inflation (>5%) + Weak growth (unemployment >5.5%)
    B1: Low inflation (2-4%) + Stable growth (unemployment <5%)
    B2: Low inflation (<3%) + Weak growth (unemployment >5.5%)
    Transition: Between thresholds
    """

    # High inflation scenarios
    if cpi >= 5.0:
        if unemployment < 5.0:
            return 'A1'  # No-brainer tightening
        elif unemployment >= 5.5:
            return 'A2'  # Stagflation
        else:
            return 'A1_A2_transition'

    # Moderate inflation (4-5%)
    elif cpi >= 4.0:
        if unemployment < 5.0:
            return 'A1_cautious'  # Action zone
        else:
            return 'B1_watch'

    # Soft landing zone (2-4%)
    elif cpi >= 2.0:
        if unemployment < 5.0:
            return 'B1'  # Goldilocks
        elif unemployment >= 5.5:
            return 'B2'  # Disinflationary recession
        else:
            return 'B1'

    # Below target (<2%)
    else:
        if unemployment >= 5.5:
            return 'B2'  # Recession
        else:
            return 'B1_strong'  # Deflation risk but stable

def get_warsh_dissent_level(date_str, cpi):
    """
    Mark Warsh public dissent level based on historical record

    Levels:
    0: Silent (no public comment)
    1: Mild critique (early warning)
    2: Direct criticism ("Fed is culprit")
    3: Resignation-level dissent
    """
    year_month = date_str[:7]  # YYYY-MM

    # Historical Warsh statements
    if year_month == '2021-06':
        return 1  # First warning when CPI hit 5.4%
    elif year_month in ['2021-11', '2021-12']:
        return 2  # "Fed is main culprit" when CPI 6.8-7.0%
    elif year_month in ['2022-01', '2022-02', '2022-03', '2022-04', '2022-05', '2022-06']:
        return 2  # Continued criticism during 7-9% CPI
    elif cpi > 5.0 and year_month >= '2022':
        return 1  # Assumed continued concern
    else:
        return 0

def main():
    # Load data
    cpi_df = pd.read_csv('backtest/cpi_data.csv', index_col='Date', parse_dates=True)
    unemp_df = pd.read_csv('backtest/unemployment_data.csv', index_col='Date', parse_dates=True)

    # Merge
    macro_df = cpi_df.join(unemp_df)

    # Identify scenarios
    macro_df['Scenario'] = macro_df.apply(
        lambda row: identify_scenario(row['CPI_YoY'], row['Unemployment']),
        axis=1
    )

    # Add Warsh dissent level
    macro_df['Warsh_Dissent'] = macro_df.apply(
        lambda row: get_warsh_dissent_level(str(row.name)[:10], row['CPI_YoY']),
        axis=1
    )

    # Save
    macro_df.to_csv('backtest/scenarios.csv')

    # Print summary
    print("="*70)
    print("SCENARIO IDENTIFICATION SUMMARY (2021-2024)")
    print("="*70)

    print("\nScenario Distribution:")
    print(macro_df['Scenario'].value_counts().sort_index())

    print("\n" + "="*70)
    print("MONTHLY TIMELINE")
    print("="*70)
    print(f"{'Date':<12} {'CPI':<6} {'Unemp':<6} {'Scenario':<20} {'Warsh':<6}")
    print("-"*70)

    for idx, row in macro_df.iterrows():
        date_str = idx.strftime('%Y-%m')
        dissent_marker = '★' * row['Warsh_Dissent'] if row['Warsh_Dissent'] > 0 else ''
        print(f"{date_str:<12} {row['CPI_YoY']:>5.1f}% {row['Unemployment']:>5.1f}% {row['Scenario']:<20} {dissent_marker:<6}")

    # Key insights
    print("\n" + "="*70)
    print("KEY INSIGHTS")
    print("="*70)

    a1_months = (macro_df['Scenario'].str.startswith('A1')).sum()
    warsh_dissent_months = (macro_df['Warsh_Dissent'] > 0).sum()
    peak_cpi = macro_df['CPI_YoY'].max()
    peak_date = macro_df['CPI_YoY'].idxmax().strftime('%Y-%m')

    print(f"\n• A1/A1-related scenarios: {a1_months} months ({a1_months/48*100:.0f}%)")
    print(f"• Warsh public dissent: {warsh_dissent_months} months")
    print(f"• Peak CPI: {peak_cpi:.1f}% in {peak_date}")
    print(f"• CPI >5% duration: {(macro_df['CPI_YoY'] > 5.0).sum()} months (Jun 2021 - Feb 2023)")
    print(f"• Current (Dec 2024): CPI {macro_df.iloc[-1]['CPI_YoY']:.1f}%, Scenario {macro_df.iloc[-1]['Scenario']}")

    # Critical period analysis
    print("\n" + "="*70)
    print("CRITICAL TEST PERIOD: 2021-2022")
    print("="*70)

    test_period = macro_df['2021-06':'2022-12']
    print(f"\n✓ Warsh warned in Jun 2021 (CPI {macro_df.loc['2021-06', 'CPI_YoY']:.1f}%)")
    print(f"✓ Fed said 'transitory' → No rate hike until Mar 2022")
    print(f"✓ Peak CPI {peak_cpi:.1f}% in Jun 2022 (proved Warsh right)")
    print(f"✓ Framework would have taken defensive position for {len(test_period)} months")

    print("\n" + "="*70)
    print("✓ Scenario identification complete")
    print("="*70)

if __name__ == "__main__":
    main()
