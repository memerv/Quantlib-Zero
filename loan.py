"""เครื่องคำนวณสินเชื่อ: ค่างวด ดอกเบี้ยรวม และตารางผ่อน (amortization)"""


class Loan:
    """สินเชื่อผ่อนเท่ากันทุกเดือน

    Attributes:
        principal: เงินกู้ตั้งต้น
        annual_rate: ดอกเบี้ยต่อปี เป็นทศนิยม เช่น 0.06 = 6%
        years: จำนวนปีที่ผ่อน
    """

    def __init__(self, principal: float, annual_rate: float, years: int) -> None:
        self.principal = principal
        self.annual_rate = annual_rate
        self.years = years
        self.monthly_rate = annual_rate / 12   # ดอกเบี้ยต่อเดือน
        self.n_months = years * 12             # จำนวนงวดทั้งหมด

    def monthly_payment(self) -> float:
        """ค่างวดต่อเดือน (เท่ากันทุกงวด)"""
        r, n = self.monthly_rate, self.n_months
        if r == 0:                             # กันหารศูนย์ กรณีดอกเบี้ย 0%
            return self.principal / n
        return self.principal * r / (1 - (1 + r) ** -n)

    def total_interest(self) -> float:
        """ดอกเบี้ยรวมที่จ่ายตลอดสัญญา = ค่างวดรวม − เงินต้น"""
        return self.monthly_payment() * self.n_months - self.principal

    def schedule(self) -> list[dict]:
        """ตารางผ่อนรายเดือน: แต่ละแถวบอกดอกเบี้ย เงินต้น และยอดคงเหลือ"""
        balance = self.principal
        payment = self.monthly_payment()
        rows = []
        for month in range(1, self.n_months + 1):
            interest = balance * self.monthly_rate     # ดอกเบี้ยเดือนนี้
            principal_paid = payment - interest        # ส่วนที่ตัดเงินต้น
            balance -= principal_paid                  # ยอดคงเหลือลดลง
            rows.append({
                "month": month,
                "payment": round(payment, 2),
                "interest": round(interest, 2),
                "principal": round(principal_paid, 2),
                "balance": round(max(balance, 0), 2),  # กันค่าติดลบจิ๋วๆ จากทศนิยม
            })
        return rows