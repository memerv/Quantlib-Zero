"""เครื่องคิดราคาพันธบัตร: price, yield-to-maturity และ duration"""

from tvm import TimeValueOfMoney


class Bond:
    """พันธบัตรจายคูปองคงที่ คนเงินต้นตอนครบกำหนด

    Attributes:
        face_value: เงินต้นที่คนตอนครบกำหนด (par)
        coupon_rate: อัตราคูปองตอปี เป็นทศนิยม เช่น 0.05 = 5%
        years: จำนวนปีถึงครบกำหนด
        frequency: จำนวนงวดจ่ายตอปี (1 = รายปี, 2 = ทุกครึ่งปี)
    """

    def __init__(self, face_value: float, coupon_rate: float,
                 years: int, frequency: int = 1) -> None:
        self.face_value = face_value
        self.coupon_rate = coupon_rate
        self.years = years
        self.frequency = frequency
        self.n_periods = years * frequency
        self.coupon = face_value * coupon_rate / frequency   # คูปองต่องวด

    def cashflows(self) -> list[float]:
        """กระแสเงินทุกงวด (t=1..n) งวดสุดท้ายรวมเงินต้นคืนด้วย"""
        flows = [self.coupon] * self.n_periods
        flows[-1] += self.face_value
        return flows

    def price(self, ytm: float) -> float:
        """ราคาพันธบัตร = NPV ของกระแสเงินทังหมด คิดลดด้วย ytm

        Args:
            ytm: yield ต่อปี เป็นทศนิยม
        """
        r = ytm / self.frequency   # อัตราต่องวด
        return sum(cf / (1 + r) ** t
                   for t, cf in enumerate(self.cashflows(), start=1))

    def ytm(self, market_price: float) -> float:
        """หา yield-to-maturity จากราคาตลาด — คือ IRR ของ [-ราคา, กระแสเงิน...]

        Args:
            market_price: ราคาที่ซื้อขายจริงในตลาด
        """
        flows = [-market_price] + self.cashflows()
        calc = TimeValueOfMoney(0.0)          # rate ถูกละเลยใน irr อยู่แล้ว
        periodic = calc.irr(flows)            # ได้ yield ต่องวด
        return periodic * self.frequency      # แปลงเป็นตอปี

    def macaulay_duration(self, ytm: float) -> float:
        """อายุเฉลี่ยถ่วงน้ำหนก (ปี) — ยิ่งมาก ราคายิงไวต่อดอกเบี้ย"""
        r = ytm / self.frequency
        flows = self.cashflows()
        price = self.price(ytm)
        weighted = sum(t * cf / (1 + r) ** t
                       for t, cf in enumerate(flows, start=1))
        return weighted / price / self.frequency   # หาร frequency ให้เป็นปี