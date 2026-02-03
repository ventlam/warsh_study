"""
数据获取模块
自动从 FRED API 和 yfinance 获取宏观数据和市场数据
"""

import os
from datetime import datetime, timedelta
from typing import Dict, Optional
import pandas as pd
import yfinance as yf
from fredapi import Fred


class DataFetcher:
    """数据获取器"""

    def __init__(self, fred_api_key: Optional[str] = None):
        """
        初始化数据获取器

        Args:
            fred_api_key: FRED API密钥（从环境变量获取）
        """
        self.fred_api_key = fred_api_key or os.getenv('FRED_API_KEY')
        if not self.fred_api_key:
            raise ValueError("FRED_API_KEY not found. Please set it in environment or pass as parameter.")

        self.fred = Fred(api_key=self.fred_api_key)

    def get_cpi_data(self, months: int = 12) -> pd.DataFrame:
        """
        获取CPI数据（YoY%）

        Args:
            months: 获取最近N个月的数据

        Returns:
            DataFrame with columns: date, cpi_yoy
        """
        # CPIAUCSL: Consumer Price Index for All Urban Consumers
        series = self.fred.get_series('CPIAUCSL', observation_start=datetime.now() - timedelta(days=months*30))

        # 计算同比增长率
        cpi_yoy = series.pct_change(periods=12) * 100

        df = pd.DataFrame({
            'date': cpi_yoy.index,
            'cpi_yoy': cpi_yoy.values
        })

        return df.dropna()

    def get_unemployment_data(self, months: int = 12) -> pd.DataFrame:
        """
        获取失业率数据

        Args:
            months: 获取最近N个月的数据

        Returns:
            DataFrame with columns: date, unemployment_rate
        """
        # UNRATE: Unemployment Rate
        series = self.fred.get_series('UNRATE', observation_start=datetime.now() - timedelta(days=months*30))

        df = pd.DataFrame({
            'date': series.index,
            'unemployment_rate': series.values
        })

        return df.dropna()

    def get_market_data(self, ticker: str = 'SPY', days: int = 365) -> pd.DataFrame:
        """
        获取市场数据（股票价格）

        Args:
            ticker: 股票代码（默认SPY）
            days: 获取最近N天的数据

        Returns:
            DataFrame with OHLCV data
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        data = yf.download(ticker, start=start_date, end=end_date, progress=False)

        # Handle MultiIndex columns
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        data = data.reset_index()
        data.columns = [col.lower() for col in data.columns]

        return data

    def get_panic_indicators(self) -> Dict[str, float]:
        """
        获取6个Panic指标的最新值

        Returns:
            字典，包含6个指标的当前值和触发状态
        """
        indicators = {}

        # 1. 家庭财富 (来自 Fed Z.1 报告，季度数据)
        # BOGZ1FL192090005Q: Households and Nonprofit Organizations; Total Financial Assets
        try:
            wealth_series = self.fred.get_series('BOGZ1FL192090005Q')
            current_wealth = wealth_series.iloc[-1]
            year_ago_wealth = wealth_series.iloc[-5]  # 4 quarters ago
            wealth_change = ((current_wealth - year_ago_wealth) / year_ago_wealth) * 100

            indicators['household_wealth'] = {
                'value': wealth_change,
                'threshold': -15.0,
                'triggered': wealth_change < -15.0,
                'description': f'{wealth_change:.1f}% YoY'
            }
        except Exception as e:
            indicators['household_wealth'] = {
                'value': None,
                'threshold': -15.0,
                'triggered': False,
                'description': f'Error: {str(e)}'
            }

        # 2. 股市下跌 (SPY YoY)
        try:
            spy_data = self.get_market_data('SPY', days=400)
            current_price = spy_data['close'].iloc[-1]
            year_ago_price = spy_data['close'].iloc[-252]  # ~252 trading days
            spy_yoy = ((current_price - year_ago_price) / year_ago_price) * 100

            indicators['stock_market'] = {
                'value': spy_yoy,
                'threshold': -40.0,
                'triggered': spy_yoy < -40.0,
                'description': f'{spy_yoy:.1f}% YoY'
            }
        except Exception as e:
            indicators['stock_market'] = {
                'value': None,
                'threshold': -40.0,
                'triggered': False,
                'description': f'Error: {str(e)}'
            }

        # 3. 银行股下跌 (KBW Bank Index - ^BKX)
        try:
            kbw_data = self.get_market_data('^BKX', days=400)
            current_kbw = kbw_data['close'].iloc[-1]
            year_ago_kbw = kbw_data['close'].iloc[-252]
            kbw_yoy = ((current_kbw - year_ago_kbw) / year_ago_kbw) * 100

            indicators['bank_stocks'] = {
                'value': kbw_yoy,
                'threshold': -50.0,
                'triggered': kbw_yoy < -50.0,
                'description': f'{kbw_yoy:.1f}% YoY'
            }
        except Exception as e:
            indicators['bank_stocks'] = {
                'value': None,
                'threshold': -50.0,
                'triggered': False,
                'description': f'Error: {str(e)}'
            }

        # 4. 失业率飙升
        try:
            unemp_data = self.get_unemployment_data(months=12)
            current_unemp = unemp_data['unemployment_rate'].iloc[-1]

            indicators['unemployment'] = {
                'value': current_unemp,
                'threshold': 8.0,
                'triggered': current_unemp > 8.0,
                'description': f'{current_unemp:.1f}%'
            }
        except Exception as e:
            indicators['unemployment'] = {
                'value': None,
                'threshold': 8.0,
                'triggered': False,
                'description': f'Error: {str(e)}'
            }

        # 5. GDP崩溃 (GDPC1: Real Gross Domestic Product)
        try:
            gdp_series = self.fred.get_series('GDPC1')
            current_gdp = gdp_series.iloc[-1]
            peak_gdp = gdp_series.rolling(window=4).max().iloc[-1]  # 过去1年的峰值
            gdp_change = ((current_gdp - peak_gdp) / peak_gdp) * 100

            indicators['gdp'] = {
                'value': gdp_change,
                'threshold': -5.0,
                'triggered': gdp_change < -5.0,
                'description': f'{gdp_change:.1f}% from peak'
            }
        except Exception as e:
            indicators['gdp'] = {
                'value': None,
                'threshold': -5.0,
                'triggered': False,
                'description': f'Error: {str(e)}'
            }

        # 6. 货币市场规模激增 (MMMFFAQ027S: Money Market Funds Total Financial Assets)
        try:
            mmf_series = self.fred.get_series('MMMFFAQ027S')
            current_mmf = mmf_series.iloc[-1]
            year_ago_mmf = mmf_series.iloc[-53]  # ~1 year ago (weekly data)
            mmf_change = ((current_mmf - year_ago_mmf) / year_ago_mmf) * 100

            indicators['money_market'] = {
                'value': mmf_change,
                'threshold': 50.0,  # 增长超过50%
                'triggered': mmf_change > 50.0,
                'description': f'{mmf_change:.1f}% YoY'
            }
        except Exception as e:
            indicators['money_market'] = {
                'value': None,
                'threshold': 50.0,
                'triggered': False,
                'description': f'Error: {str(e)}'
            }

        return indicators

    def get_latest_data(self) -> Dict:
        """
        获取所有最新数据（Dashboard使用）

        Returns:
            包含CPI、失业率、市场数据、Panic指标的字典
        """
        data = {}

        # CPI
        cpi_df = self.get_cpi_data(months=12)
        data['cpi_latest'] = {
            'value': cpi_df['cpi_yoy'].iloc[-1],
            'date': cpi_df['date'].iloc[-1].strftime('%Y-%m-%d')
        }

        # 失业率
        unemp_df = self.get_unemployment_data(months=12)
        data['unemployment_latest'] = {
            'value': unemp_df['unemployment_rate'].iloc[-1],
            'date': unemp_df['date'].iloc[-1].strftime('%Y-%m-%d')
        }

        # SPY价格
        spy_df = self.get_market_data('SPY', days=30)
        data['spy_latest'] = {
            'value': spy_df['close'].iloc[-1],
            'date': spy_df['date'].iloc[-1].strftime('%Y-%m-%d')
        }

        # Panic指标
        data['panic_indicators'] = self.get_panic_indicators()

        return data


if __name__ == "__main__":
    # 测试代码
    fetcher = DataFetcher()

    print("=== CPI Data ===")
    cpi = fetcher.get_cpi_data(months=6)
    print(cpi.tail())

    print("\n=== Unemployment Data ===")
    unemp = fetcher.get_unemployment_data(months=6)
    print(unemp.tail())

    print("\n=== SPY Data ===")
    spy = fetcher.get_market_data('SPY', days=30)
    print(spy.tail())

    print("\n=== Panic Indicators ===")
    panic = fetcher.get_panic_indicators()
    for name, indicator in panic.items():
        print(f"{name}: {indicator['description']} (Triggered: {indicator['triggered']})")
