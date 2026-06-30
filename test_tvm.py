"""Unit tests สำหรับคลาส TimeValueOfMoney ด้วย pytest"""

import pytest

from tvm import TimeValueOfMoney


def test_future_value():
    # ฝาก 100 ที่ 5% สามปี → 100*1.05^3 = 115.7625
    calc = TimeValueOfMoney(0.05)
    assert calc.future_value(100, 3) == pytest.approx(115.7625)


def test_present_value():
    # ภาพกลับด้านของ future_value: 115.7625 ในอีก 3 ปี = 100 วันนี้
    calc = TimeValueOfMoney(0.05)
    assert calc.present_value(115.7625, 3) == pytest.approx(100.0)


def test_fv_pv_roundtrip():
    # เอาเงินไปอนาคตแล้วดึงกลับ ต้องได้เท่าเดิม (พิสูจน์ว่าสองสูตรสอดคล้องกัน)
    calc = TimeValueOfMoney(0.08)
    fv = calc.future_value(500, 10)
    assert calc.present_value(fv, 10) == pytest.approx(500.0)


def test_annuity_present_value():
    # จ่าย 100 ต่อปี 3 ปี ที่ 5% → 272.3248...
    calc = TimeValueOfMoney(0.05)
    assert calc.annuity_present_value(100, 3) == pytest.approx(272.324802, abs=1e-4)


def test_annuity_zero_rate():
    # ดอกเบี้ย 0% → จ่าย 100 สามงวด = 300 พอด (เช็คว่ากันหารศูนย์ทำงาน)
    calc = TimeValueOfMoney(0.0)
    assert calc.annuity_present_value(100, 3) == pytest.approx(300.0)


def test_npv():
    # ลงทุน -100 แล้วได้ 50, 70 ที่ 10% → NPV ≈ 3.3058
    calc = TimeValueOfMoney(0.10)
    assert calc.npv([-100, 50, 70]) == pytest.approx(3.305785, abs=1e-4)


def test_irr_matches_excel():
    # IRR ไม่สนใจ rate ที่ตั้งไว (ตั้ง 0 ก็ได้) มันแก้หาเอง
    # [-100, 50, 70] → IRR ≈ 0.123212 ตรงกบ Excel =IRR()
    calc = TimeValueOfMoney(0.0)
    assert calc.irr([-100, 50, 70]) == pytest.approx(0.123212, abs=1e-4)