"""Time Value of Money calculations"""
import numpy as np

class TimeValueOfMoney:
    def __init__(self, rate: float) -> None:
        self.rate = rate
    def future_value(self, present_value: float, periods: int) -> float:
        return present_value * (1 + self.rate) ** periods
    def present_value(self, future_value: float, periods: int) -> float:
        return future_value / (1 + self.rate) ** periods
    def annuity_present_value(self, payment: float, periods: int) -> float:
        if self.rate == 0:
            return payment * periods
        return payment * (1 - (1 + self.rate) ** -periods) / self.rate
    def npv(self, cashflows: list[float]) -> float:
        return sum(cf / (1 + self.rate) ** t for t, cf in enumerate(cashflows))
    def irr(self, cashflows: list[float], guess: float = 0.1) -> float:
        roots = np.roots(cashflows)
        real_roots = roots[np.abs(roots.imag) < 1e-9].real
        rates = real_roots - 1.0
        valid = rates[rates > -1.0]
        if valid.size == 0:
            raise ValueError("No real IRR found for this cash flow")
        return float(valid[np.argmin(np.abs(valid - guess))])
