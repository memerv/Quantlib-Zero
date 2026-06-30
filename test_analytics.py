"""Unit tests สำหรับ ReturnsAnalyzer"""

import pytest

from analytics import ReturnsAnalyzer


def test_daily_returns():
    # 100→110 = +10%, 110→99 = −10%
    a = ReturnsAnalyzer([100, 110, 99])
    assert a.daily_returns() == pytest.approx([0.10, -0.10])


def test_returns_length():
    # n ราคา → n−1 ผลตอบแทน
    a = ReturnsAnalyzer([100, 101, 102, 103])
    assert len(a.daily_returns()) == 3


def test_constant_prices_zero_volatility():
    # ราคานิ่ง → ความผันผวน = 0
    a = ReturnsAnalyzer([50, 50, 50, 50])
    assert a.daily_volatility() == pytest.approx(0.0)


def test_daily_volatility():
    # ผลตอบแทน [0.1, -0.1] → sample std ≈ 0.14142
    a = ReturnsAnalyzer([100, 110, 99])
    assert a.daily_volatility() == pytest.approx(0.14142, abs=1e-4)


def test_max_drawdown():
    # จุดสูงสุด 120 → ตกไป 90 = ตก 25%
    a = ReturnsAnalyzer([100, 120, 90, 110])
    assert a.max_drawdown() == pytest.approx(0.25)


def test_sharpe_zero_when_flat():
    # ไม่มีความผันผวน → Sharpe = 0 (เช็คว่ากันหารศูนย์ทำงาน)
    a = ReturnsAnalyzer([100, 100, 100])
    assert a.sharpe_ratio() == pytest.approx(0.0)