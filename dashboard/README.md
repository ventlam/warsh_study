# Warsh 投资框架实时监控 Dashboard

## 功能概述

实时监控系统，基于 Warsh 投资框架自动追踪宏观经济指标并提供资产配置建议。

### 核心功能

1. **宏观经济指标监控**
   - CPI YoY% (来自 FRED)
   - 失业率 (来自 FRED)
   - SPY 市场价格 (来自 yfinance)

2. **Panic 指标追踪**（6个指标）
   - 家庭财富变化
   - 股市跌幅
   - 银行股跌幅
   - 失业率飙升
   - GDP 崩溃
   - 货币市场规模激增

3. **自动场景识别**
   - A1: 高通胀 + 稳定增长
   - A1_cautious: 进入高通胀
   - A2: 滞胀
   - B1: 软着陆
   - B2: 通缩性衰退
   - C1: Panic 模式

4. **资产配置建议**
   - 基于当前场景自动生成配置
   - 支持 SPY, TLT, IEF, HYG, GLD, Cash
   - 可视化展示（表格 + 饼图）

5. **历史趋势图表**
   - 24个月 CPI 趋势
   - 24个月失业率趋势
   - 2年 SPY 价格趋势

---

## 安装与使用

### 1. 安装依赖

```bash
cd dashboard
pip install -r requirements.txt
```

### 2. 获取 FRED API Key

1. 访问 https://fred.stlouisfed.org/
2. 注册免费账户
3. 进入 https://fred.stlouisfed.org/docs/api/api_key.html
4. 点击 "Request API Key"
5. 复制生成的 Key

### 3. 启动 Dashboard

```bash
streamlit run app.py
```

或者设置环境变量：

```bash
export FRED_API_KEY=your_api_key_here
streamlit run app.py
```

### 4. 访问 Dashboard

浏览器自动打开 http://localhost:8501

---

## 使用说明

### 首次使用

1. 启动后，在左侧边栏输入 FRED API Key
2. 点击 "刷新数据" 按钮
3. Dashboard 将自动加载最新数据

### 数据更新频率

- **CPI**: 每月12日左右发布（月度数据）
- **失业率**: 每月第一个周五发布（月度数据）
- **市场数据**: 实时更新（延迟15分钟）
- **Panic 指标**: 数据频率不一（季度/月度/周度）

**建议**: 每月15日左右（CPI发布后）刷新数据，进行场景识别。

### 场景切换逻辑

Dashboard 使用以下逻辑判断场景：

1. **Panic Score >= 2.0** → C1（Panic 模式）
2. **CPI > 5.5%**
   - 失业率 > 6% → A2（滞胀）
   - 失业率 <= 6% → A1（高通胀）
3. **CPI 4.4-5.5%** → A1_cautious（警惕）
4. **CPI 2.2-4.4%** → B1（软着陆）
5. **CPI < 2.2%**
   - 失业率 > 5.5% → B2（通缩性衰退）
   - 失业率 <= 5.5% → B1（低通胀稳定）

---

## 模块说明

### data_fetcher.py

数据获取模块，包含 `DataFetcher` 类：

- `get_cpi_data(months)`: 获取 CPI YoY% 数据
- `get_unemployment_data(months)`: 获取失业率数据
- `get_market_data(ticker, days)`: 获取市场价格数据
- `get_panic_indicators()`: 计算6个 Panic 指标
- `get_latest_data()`: 获取所有最新数据（Dashboard 入口）

**数据源**:
- FRED API: CPI, 失业率, GDP, 家庭财富, 货币市场基金
- yfinance: SPY, KBW 银行指数

### scenario_engine.py

场景识别引擎，包含 `ScenarioEngine` 类：

- `calculate_panic_score(indicators)`: 计算 Panic Score
- `identify_scenario(cpi, unemployment, panic_score)`: 识别当前场景
- 返回 `ScenarioResult`（场景、描述、配置、理由）

### app.py

Streamlit Dashboard 主程序：

- `render_macro_indicators()`: 渲染宏观指标卡片
- `render_panic_indicators()`: 渲染 Panic 指标表格
- `render_scenario_identification()`: 渲染场景识别和配置建议
- `render_historical_chart()`: 渲染历史趋势图表

---

## 测试

### 测试 data_fetcher.py

```bash
cd dashboard
python data_fetcher.py
```

预期输出：
- CPI 数据表格（最近6个月）
- 失业率数据表格
- SPY 价格数据
- 6个 Panic 指标状态

### 测试 scenario_engine.py

```bash
python scenario_engine.py
```

预期输出：
- 3个测试用例的场景识别结果
- 高通胀场景 (2022-06)
- 软着陆场景 (2023-12)
- Panic 场景 (2020-03)

---

## 常见问题

### Q: FRED API 请求失败？

A: 检查以下几点：
1. API Key 是否正确
2. 是否超过请求限额（免费版: 120 requests/minute）
3. 网络连接是否正常

### Q: yfinance 数据下载慢？

A: yfinance 依赖 Yahoo Finance，国内访问可能较慢。建议：
- 使用代理
- 减少历史数据长度（`days` 参数）

### Q: Panic 指标显示 Error？

A: 某些指标（如 Fed Z.1 家庭财富）是季度数据，发布频率低。如果最新数据不可用，会显示错误，不影响其他功能。

### Q: 场景识别与预期不符？

A: 场景识别基于当前最新数据。如果：
1. 数据尚未更新（如15日之前CPI未发布）
2. 数据源延迟
3. 缓冲区规则生效（CPI 4.4-5.5% 不会立即切换场景）

---

## 后续改进

### 待实现功能

- [ ] 邮件/SMS 告警（场景切换时通知）
- [ ] Warsh 声明监控（Google Alerts + RSS）
- [ ] 历史场景回溯（显示过去12个月的场景变化）
- [ ] 多账户支持（不同风险偏好的配置方案）
- [ ] 交易执行集成（自动下单）

### 技术改进

- [ ] 数据缓存（Redis）减少 API 请求
- [ ] 定时任务（每日自动更新）
- [ ] Docker 容器化部署
- [ ] 单元测试覆盖

---

## 许可证

MIT License

---

## 参考文档

- [Warsh 投资框架 v1.0](../frameworks/2026_02_02_investment_framework_v1.md)
- [边缘案例决策规则](../frameworks/edge_cases_decision_rules.md)
- [历史回测报告](../backtest/BACKTEST_REPORT.md)

---

**版本**: 1.0
**最后更新**: 2026-02-03
