"""วิเคราะห์ผลตอบแทนและความเสี่ยงจากชุดราคา"""

import numpy as np


class ReturnsAnalyzer:
    """คำนวณผลตอบแทน ความผันผวน Sharpe และ drawdown จากราคาหุ้น

    Attributes:
        prices: ชุดราคาปิดเรียงตามเวลา
        risk_free_rate: อัตราปลอดความเสี่ยงต่อปี ใช้คิด Sharpe
    """

    TRADING_DAYS = 252   # จำนวนวันทำการต่อปี มาตรฐานวงการ

    def __init__(self, prices: list[float], risk_free_rate: float = 0.0) -> None:
        self.prices = np.array(prices, dtype=float)
        self.risk_free_rate = risk_free_rate

    def daily_returns(self) -> list[float]:
        """ผลตอบแทนรายวัน: (ราคาวันนี้ / เมื่อวาน) − 1"""
        p = self.prices
        return list(p[1:] / p[:-1] - 1)

    def daily_volatility(self) -> float:
        """ความผันผวนรายวัน = ส่วนเบี่ยงเบนมาตรฐานของผลตอบแทน"""
        return float(np.std(self.daily_returns(), ddof=1))

    def annualized_return(self) -> float:
        """ผลตอบแทนเฉลี่ยต่อปี"""
        return float(np.mean(self.daily_returns()) * self.TRADING_DAYS)

    def annualized_volatility(self) -> float:
        """ความผันผวนต่อปี = ผันผวนรายวัน × √252"""
        return self.daily_volatility() * np.sqrt(self.TRADING_DAYS)

    def sharpe_ratio(self) -> float:
        """ผลตอบแทนส่วนเกินต่อหน่วยความเสี่ยง"""
        vol = self.annualized_volatility()
        if vol == 0:
            return 0.0
        return (self.annualized_return() - self.risk_free_rate) / vol

    def max_drawdown(self) -> float:
        """การตกหนักสุดจากจุดสูงสุด (เป็นค่าบวก เช่น 0.25 = ตก 25%)"""
        running_max = np.maximum.accumulate(self.prices)
        drawdowns = (self.prices - running_max) / running_max
        return float(-drawdowns.min())