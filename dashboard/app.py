"""
Warsh 投资框架实时监控 Dashboard
使用 Streamlit 构建
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from data_fetcher import DataFetcher
from scenario_engine import ScenarioEngine


# 页面配置
st.set_page_config(
    page_title="Warsh Framework Monitor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_data(fred_api_key: str):
    """加载数据"""
    try:
        fetcher = DataFetcher(fred_api_key)
        data = fetcher.get_latest_data()
        return data, fetcher
    except Exception as e:
        st.error(f"数据加载失败: {str(e)}")
        return None, None


def render_header():
    """渲染页面头部"""
    st.title("📊 Warsh 投资框架实时监控")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("更新时间", datetime.now().strftime("%Y-%m-%d %H:%M"))


def render_macro_indicators(data):
    """渲染宏观指标"""
    st.subheader("📈 宏观经济指标")

    col1, col2, col3 = st.columns(3)

    with col1:
        cpi_value = data['cpi_latest']['value']
        cpi_color = "🔴" if cpi_value > 5.5 else "🟡" if cpi_value > 4.4 else "🟢"
        st.metric(
            label=f"{cpi_color} CPI YoY%",
            value=f"{cpi_value:.2f}%",
            delta=f"截至 {data['cpi_latest']['date']}"
        )

    with col2:
        unemp_value = data['unemployment_latest']['value']
        unemp_color = "🔴" if unemp_value > 6.0 else "🟡" if unemp_value > 5.5 else "🟢"
        st.metric(
            label=f"{unemp_color} 失业率",
            value=f"{unemp_value:.1f}%",
            delta=f"截至 {data['unemployment_latest']['date']}"
        )

    with col3:
        spy_value = data['spy_latest']['value']
        st.metric(
            label="📊 SPY 价格",
            value=f"${spy_value:.2f}",
            delta=f"截至 {data['spy_latest']['date']}"
        )


def render_panic_indicators(data):
    """渲染 Panic 指标"""
    st.subheader("⚠️ Panic 指标监控")

    panic_indicators = data['panic_indicators']
    engine = ScenarioEngine()
    panic_score = engine.calculate_panic_score(panic_indicators)

    # Panic Score 显示
    st.metric(
        label="Panic Score",
        value=f"{panic_score:.1f} / 6.0",
        delta="🚨 HIGH RISK" if panic_score >= 2.0 else "✅ Normal"
    )

    # 详细指标表格
    indicators_data = []
    for name, indicator in panic_indicators.items():
        indicators_data.append({
            '指标': name.replace('_', ' ').title(),
            '当前值': indicator['description'],
            '阈值': f"{'<' if name in ['household_wealth', 'stock_market', 'bank_stocks', 'gdp'] else '>'} {indicator['threshold']}",
            '状态': '🔴 触发' if indicator['triggered'] else '🟢 正常'
        })

    df = pd.DataFrame(indicators_data)
    st.dataframe(df, use_container_width=True)


def render_scenario_identification(data):
    """渲染场景识别"""
    st.subheader("🎯 场景识别 & 仓位建议")

    # 获取当前数据
    cpi = data['cpi_latest']['value']
    unemployment = data['unemployment_latest']['value']
    panic_indicators = data['panic_indicators']

    # 场景识别
    engine = ScenarioEngine()
    panic_score = engine.calculate_panic_score(panic_indicators)
    scenario = engine.identify_scenario(cpi, unemployment, panic_score)

    # 显示场景信息
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(f"### 当前场景: **{scenario.scenario}**")
        st.markdown(f"**{scenario.scenario_name}**")
        st.info(scenario.description)
        st.success(f"**识别理由:**\n{scenario.rationale}")

    with col2:
        st.markdown("### 建议资产配置")

        # 配置表格
        allocation_data = []
        for asset, weight in scenario.allocation.items():
            allocation_data.append({
                '资产': asset,
                '权重': f"{weight*100:.0f}%",
                '方向': '做空' if weight < 0 else '做多' if weight > 0 else '无仓位'
            })

        df_allocation = pd.DataFrame(allocation_data)
        st.dataframe(df_allocation, use_container_width=True)

        # 饼图展示（仅展示正权重）
        positive_allocation = {k: v for k, v in scenario.allocation.items() if v > 0}
        if positive_allocation:
            fig = go.Figure(data=[go.Pie(
                labels=list(positive_allocation.keys()),
                values=list(positive_allocation.values()),
                hole=0.3
            )])
            fig.update_layout(
                title="资产配置分布",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)


def render_historical_chart(fetcher):
    """渲染历史图表"""
    st.subheader("📉 历史数据趋势")

    # 获取历史数据
    cpi_df = fetcher.get_cpi_data(months=24)
    unemp_df = fetcher.get_unemployment_data(months=24)
    spy_df = fetcher.get_market_data('SPY', days=730)

    # 创建子图
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=('CPI YoY%', '失业率 %', 'SPY 价格 $'),
        vertical_spacing=0.1
    )

    # CPI 图表
    fig.add_trace(
        go.Scatter(x=cpi_df['date'], y=cpi_df['cpi_yoy'], name='CPI YoY%', line=dict(color='red')),
        row=1, col=1
    )
    fig.add_hline(y=5.5, line_dash="dash", line_color="orange", row=1, col=1, annotation_text="High Inflation (5.5%)")
    fig.add_hline(y=2.2, line_dash="dash", line_color="green", row=1, col=1, annotation_text="Target (2.2%)")

    # 失业率图表
    fig.add_trace(
        go.Scatter(x=unemp_df['date'], y=unemp_df['unemployment_rate'], name='Unemployment %', line=dict(color='blue')),
        row=2, col=1
    )
    fig.add_hline(y=6.0, line_dash="dash", line_color="orange", row=2, col=1, annotation_text="Stagflation (6.0%)")

    # SPY 图表
    fig.add_trace(
        go.Scatter(x=spy_df['date'], y=spy_df['close'], name='SPY Price', line=dict(color='green')),
        row=3, col=1
    )

    fig.update_layout(height=900, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def main():
    """主函数"""
    # 侧边栏配置
    st.sidebar.title("⚙️ 配置")
    fred_api_key = st.sidebar.text_input(
        "FRED API Key",
        type="password",
        help="从 https://fred.stlouisfed.org/docs/api/api_key.html 获取"
    )

    refresh_button = st.sidebar.button("🔄 刷新数据")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 关于")
    st.sidebar.info(
        "Warsh 投资框架实时监控 Dashboard\n\n"
        "基于 Kevin Warsh 的政策反应函数，"
        "自动识别经济场景并给出资产配置建议。"
    )

    # 主页面
    render_header()

    if not fred_api_key:
        st.warning("⚠️ 请在左侧输入 FRED API Key 以开始监控")
        st.markdown(
            "### 如何获取 FRED API Key？\n"
            "1. 访问 https://fred.stlouisfed.org/\n"
            "2. 注册账户（免费）\n"
            "3. 进入 https://fred.stlouisfed.org/docs/api/api_key.html\n"
            "4. 点击 \"Request API Key\"\n"
            "5. 复制生成的 Key 并粘贴到左侧输入框"
        )
        return

    # 加载数据
    with st.spinner("正在加载数据..."):
        data, fetcher = load_data(fred_api_key)

    if data is None or fetcher is None:
        st.error("数据加载失败，请检查 API Key 是否正确")
        return

    # 渲染各个模块
    render_macro_indicators(data)
    st.markdown("---")

    render_panic_indicators(data)
    st.markdown("---")

    render_scenario_identification(data)
    st.markdown("---")

    render_historical_chart(fetcher)

    # 页脚
    st.markdown("---")
    st.caption(f"最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Powered by Streamlit + FRED API + yfinance")


if __name__ == "__main__":
    main()
