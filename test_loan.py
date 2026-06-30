"""Unit tests สำหรับคลาส Loan"""

import pytest

from loan import Loan


def test_monthly_payment():
    # กู้ 100,000 ที่ 6%/ปี 30 ปี → ค่างวด ≈ 599.55 (ค่ามาตรฐานที่รู้กันทั่วไป)
    loan = Loan(100_000, 0.06, 30)
    assert loan.monthly_payment() == pytest.approx(599.55, abs=0.1)


def test_zero_rate_payment():
    # ดอกเบี้ย 0%: กู้ 1,200,000 ผ่อน 10 ปี → 1,200,000/120 = 10,000 พอดี
    loan = Loan(1_200_000, 0.0, 10)
    assert loan.monthly_payment() == pytest.approx(10_000)


def test_schedule_length():
    # ตารางต้องมีจำนวนแถว = จำนวนเดือนทั้งหมด
    loan = Loan(100_000, 0.06, 30)
    assert len(loan.schedule()) == 360


def test_loan_paid_off():
    # ผ่อนครบแล้วยอดคงเหลือต้องเป็น 0 (พิสูจน์ว่าตารางถูกต้อง)
    loan = Loan(100_000, 0.06, 30)
    assert loan.schedule()[-1]["balance"] == pytest.approx(0, abs=0.01)


def test_first_payment_mostly_interest():
    # เดือนแรก: ดอกเบี้ย = เงินต้น × อัตราต่อเดือน = 100,000 × 0.005 = 500
    loan = Loan(100_000, 0.06, 30)
    assert loan.schedule()[0]["interest"] == pytest.approx(500.0, abs=0.01)