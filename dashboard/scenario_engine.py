"""
场景识别引擎
基于 Warsh 框架自动识别当前经济场景
"""

from typing import Dict, Tuple
from dataclasses import dataclass


@dataclass
class ScenarioResult:
    """场景识别结果"""
    scenario: str
    scenario_name: str
    description: str
    allocation: Dict[str, float]
    rationale: str


class ScenarioEngine:
    """场景识别引擎"""

    # 场景配置
    SCENARIOS = {
        'A1': {
            'name': '高通胀 + 稳定增长',
            'description': '通胀>5.5%, 失业率<6%, 需要防御',
            'allocation': {
                'SPY': 0.50,
                'TLT': -0.10,
                'IEF': 0.00,
                'HYG': 0.00,
                'GLD': 0.20,
                'Cash': 0.40
            }
        },
        'A1_cautious': {
            'name': '进入高通胀',
            'description': 'CPI 4.4-5.5%, 保持警惕',
            'allocation': {
                'SPY': 0.55,
                'TLT': 0.00,
                'IEF': 0.05,
                'HYG': 0.00,
                'GLD': 0.15,
                'Cash': 0.25
            }
        },
        'A2': {
            'name': '滞胀',
            'description': '高通胀(>5.5%) + 高失业率(>6%)',
            'allocation': {
                'SPY': 0.40,
                'TLT': 0.00,
                'IEF': 0.10,
                'HYG': 0.00,
                'GLD': 0.30,
                'Cash': 0.20
            }
        },
        'B1': {
            'name': '软着陆',
            'description': 'CPI 2.2-4.4%, 增长稳定',
            'allocation': {
                'SPY': 0.70,
                'TLT': 0.05,
                'IEF': 0.10,
                'HYG': 0.05,
                'GLD': 0.00,
                'Cash': 0.10
            }
        },
        'B2': {
            'name': '通缩性衰退',
            'description': 'CPI<2.2%, 失业率>5.5%',
            'allocation': {
                'SPY': 0.50,
                'TLT': 0.20,
                'IEF': 0.20,
                'HYG': 0.00,
                'GLD': 0.00,
                'Cash': 0.10
            }
        },
        'C1': {
            'name': 'Panic模式',
            'description': 'Panic Score >= 2.0，资本保全',
            'allocation': {
                'SPY': 0.20,
                'TLT': 0.30,
                'IEF': 0.20,
                'HYG': 0.00,
                'GLD': 0.00,
                'Cash': 0.30
            }
        }
    }

    def __init__(self):
        """初始化引擎"""
        pass

    def calculate_panic_score(self, panic_indicators: Dict) -> float:
        """
        计算Panic Score

        Args:
            panic_indicators: Panic指标字典

        Returns:
            Panic Score (0-6)
        """
        score = 0.0

        for name, indicator in panic_indicators.items():
            if indicator['triggered']:
                score += 1.0

        return score

    def identify_scenario(self, cpi: float, unemployment: float, panic_score: float) -> ScenarioResult:
        """
        识别当前场景

        Args:
            cpi: CPI YoY% (例如: 5.4)
            unemployment: 失业率% (例如: 4.2)
            panic_score: Panic分数 (0-6)

        Returns:
            ScenarioResult对象
        """
        # 1. 检查Panic
        if panic_score >= 2.0:
            scenario = 'C1'
            rationale = f"Panic Score = {panic_score:.1f} >= 2.0，进入资本保全模式"
            return self._build_result(scenario, cpi, unemployment, panic_score, rationale)

        # 2. 检查高通胀
        if cpi > 5.5:
            if unemployment > 6.0:
                scenario = 'A2'
                rationale = f"滞胀：CPI {cpi:.1f}% > 5.5% 且 失业率 {unemployment:.1f}% > 6%"
            else:
                scenario = 'A1'
                rationale = f"高通胀：CPI {cpi:.1f}% > 5.5%，失业率 {unemployment:.1f}% 尚可"
            return self._build_result(scenario, cpi, unemployment, panic_score, rationale)

        # 3. 检查通胀缓冲区
        if 4.4 <= cpi <= 5.5:
            scenario = 'A1_cautious'
            rationale = f"CPI {cpi:.1f}% 在缓冲区 [4.4%, 5.5%]，保持警惕"
            return self._build_result(scenario, cpi, unemployment, panic_score, rationale)

        # 4. 检查软着陆
        if 2.2 <= cpi < 4.4:
            scenario = 'B1'
            rationale = f"软着陆：CPI {cpi:.1f}% 在目标范围 [2.2%, 4.4%]"
            return self._build_result(scenario, cpi, unemployment, panic_score, rationale)

        # 5. 检查低通胀/通缩
        if cpi < 2.2:
            if unemployment > 5.5:
                scenario = 'B2'
                rationale = f"通缩性衰退：CPI {cpi:.1f}% < 2.2% 且 失业率 {unemployment:.1f}% > 5.5%"
            else:
                scenario = 'B1'
                rationale = f"低通胀稳定：CPI {cpi:.1f}% < 2.2%，但失业率 {unemployment:.1f}% 健康"
            return self._build_result(scenario, cpi, unemployment, panic_score, rationale)

        # 默认
        scenario = 'B1'
        rationale = f"默认软着陆场景（CPI {cpi:.1f}%, 失业率 {unemployment:.1f}%）"
        return self._build_result(scenario, cpi, unemployment, panic_score, rationale)

    def _build_result(self, scenario: str, cpi: float, unemployment: float, panic_score: float, rationale: str) -> ScenarioResult:
        """构建场景结果对象"""
        config = self.SCENARIOS[scenario]

        return ScenarioResult(
            scenario=scenario,
            scenario_name=config['name'],
            description=config['description'],
            allocation=config['allocation'],
            rationale=rationale
        )


if __name__ == "__main__":
    # 测试代码
    engine = ScenarioEngine()

    # 测试用例 1: 高通胀场景 (2022年6月)
    print("=== Test Case 1: 高通胀 (2022-06) ===")
    result = engine.identify_scenario(cpi=9.1, unemployment=3.6, panic_score=0)
    print(f"场景: {result.scenario} - {result.scenario_name}")
    print(f"描述: {result.description}")
    print(f"理由: {result.rationale}")
    print(f"配置: {result.allocation}")

    # 测试用例 2: 软着陆 (2023年末)
    print("\n=== Test Case 2: 软着陆 (2023-12) ===")
    result = engine.identify_scenario(cpi=3.4, unemployment=3.7, panic_score=0)
    print(f"场景: {result.scenario} - {result.scenario_name}")
    print(f"理由: {result.rationale}")

    # 测试用例 3: Panic (2020年3月)
    print("\n=== Test Case 3: Panic (2020-03) ===")
    panic_indicators = {
        'household_wealth': {'triggered': True},
        'stock_market': {'triggered': True},
        'unemployment': {'triggered': True}
    }
    panic_score = 3.0
    result = engine.identify_scenario(cpi=1.5, unemployment=4.4, panic_score=panic_score)
    print(f"场景: {result.scenario} - {result.scenario_name}")
    print(f"理由: {result.rationale}")
