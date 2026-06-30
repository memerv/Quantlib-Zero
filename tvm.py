"""Time Value of Money calculations.

โมดูลนี้มีคลาส TimeValueOfMoney สำหรับการคำนวณการเงินพื้นฐาน เช่น
future value, present value, annuity, NPV และ IRR
"""

import numpy as np


class TimeValueOfMoney:
    """เครื่องคำนวณ time-value-of-money ที่ผูกกับอัตราดอกเบี้ยค่าเดียว

    Attributes:
        rate: อัตราดอกเบี้ย/อัตราคิดลดต่องวด เป็นทศนิยม เช่น 0.05 = 5%
    """

    def __init__(self, rate: float) -> None:
        """ตั้งค่าเครื่องคำนวณด้วยอัตราดอกเบี้ยต่องวด"""
        self.rate = rate

    def future_value(self, present_value: float, periods: int) -> float:
        """มูลค่าอนาคตของเงินก้อนเดียว ด้วยดอกเบี้ยทบต้น: PV*(1+r)^n"""
        return present_value * (1 + self.rate) ** periods

    def present_value(self, future_value: float, periods: int) -> float:
        """มูลค่าปัจจุบันของเงินก้อนเดียวในอนาคต: FV/(1+r)^n"""
        return future_value / (1 + self.rate) ** periods

    def annuity_present_value(self, payment: float, periods: int) -> float:
        """มูลค่าปัจจุบันของเงินจ่ายเท่ากันทุกงวด (ordinary annuity)"""
        if self.rate == 0:
            return payment * periods
        return payment * (1 - (1 + self.rate) ** -periods) / self.rate

    def npv(self, cashflows: list[float]) -> float:
        """มูลค่าปัจจุบันสุทธิของกระแสเงินหลายงวด (งวดแรกอยู่ที่ t=0)"""
        return sum(cf / (1 + self.rate) ** t for t, cf in enumerate(cashflows))

    def irr(self, cashflows: list[float], guess: float = 0.1) -> float:
        """อัตราผลตอบแทนภายใน: อัตรา r ที่ทำให้ NPV = 0

        ใช้ np.roots หารากพหุนามใน y=(1+r) แล้วแปลงกลับเป็น r
        """
        roots = np.roots(cashflows)
        real_roots = roots[np.abs(roots.imag) < 1e-9].real
        rates = real_roots - 1.0
        valid = rates[rates > -1.0]
        if valid.size == 0:
            raise ValueError("ไม่พบ IRR ที่เป็นจำนวนจริงสำหรับกระแสเงินนี้")
        return float(valid[np.argmin(np.abs(valid - guess))])