"""Unit tests สำหรับคลาส Bond"""

import pytest

from bond import Bond


def test_price_at_par():
    # yield = coupon → ราคา = เงินต้นพอดี (กฎพื้นฐานที่สุดของพันธบัตร)
    bond = Bond(1000, 0.05, 10)
    assert bond.price(0.05) == pytest.approx(1000.0)


def test_price_below_par():
    # yield (6%) สูงกว่า coupon (5%) → ราคาต่ำกว่า par
    bond = Bond(1000, 0.05, 10)
    assert bond.price(0.06) < 1000.0


def test_zero_coupon_price():
    # พันธบัตรไร้คูปอง = present value ก้อนเดียว: 1000/1.05^5 ≈ 783.53
    bond = Bond(1000, 0.0, 5)
    assert bond.price(0.05) == pytest.approx(783.53, abs=0.01)


def test_ytm_roundtrip():
    # คดราคาจาก yield 6% แล้วถอด yield กลับ ต้องได้ 6% คืน (price ↔ ytm สอดคล้องกัน)
    bond = Bond(1000, 0.05, 10)
    price = bond.price(0.06)
    assert bond.ytm(price) == pytest.approx(0.06, abs=1e-4)


def test_zero_coupon_duration():
    # พันธบัตรไร้คูปอง: เงินมาก้อนเดียวตอนครบกำหนด → duration = อายุพอดี
    bond = Bond(1000, 0.0, 5)
    assert bond.macaulay_duration(0.05) == pytest.approx(5.0)


def test_coupon_bond_duration_less_than_maturity():
    # พันธบัตรมีคูปอง: ได้เงินบางส่วนก่อนครบกำหนด → duration < อายุ
    bond = Bond(1000, 0.05, 10)
    assert bond.macaulay_duration(0.05) < 10