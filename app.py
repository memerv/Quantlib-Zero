"""Quant Desk — Financial Analytics Dashboard (Streamlit)"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from tvm import TimeValueOfMoney
from loan import Loan
from bond import Bond
from analytics import ReturnsAnalyzer

st.set_page_config(page_title="Quant Desk", page_icon="📊", layout="wide")

# ---------- ธีม + ฟอนต์ ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"], .stApp { font-family:'Inter',-apple-system,sans-serif; }
.stApp { background:#f4f6fa; }
#MainMenu, footer, header { visibility:hidden; }
section[data-testid="stSidebar"] { background:#0f172a; }
section[data-testid="stSidebar"] * { color:#e2e8f0; }
section[data-testid="stSidebar"] h1 { color:#fff; font-weight:800; }
.block-container { padding:1.5rem 2.5rem; max-width:1300px; }
h1,h2,h3 { color:#0f172a; letter-spacing:-0.02em; font-weight:700; }
div[data-testid="stMetric"] { background:#fff; border:1px solid #e6e9f0;
    border-radius:16px; padding:18px 20px; box-shadow:0 1px 3px rgba(15,23,42,.05); }
div[data-testid="stMetricLabel"] { color:#64748b; font-weight:500; }
.stButton>button { background:#2563eb; color:#fff; border:none; border-radius:10px;
    padding:.5rem 1.5rem; font-weight:600; }
.stButton>button:hover { background:#1d4ed8; }
.card-title { font-size:1.05rem; font-weight:600; color:#0f172a; margin:.3rem 0 .1rem; }
.card-desc { font-size:.85rem; color:#64748b; margin-bottom:.5rem; }
</style>
""", unsafe_allow_html=True)

BLUE, GREEN, RED = "#2563eb", "#16a34a", "#dc2626"


def styled(fig, height=340):
    fig.update_layout(template="plotly_white", height=height,
        font=dict(family="Inter,sans-serif", color="#334155", size=12),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(orientation="h", y=-0.18))
    fig.update_xaxes(showgrid=False, linecolor="#e2e8f0")
    fig.update_yaxes(gridcolor="#eef1f6", zeroline=False)
    return fig


def panel(title, desc):
    st.markdown(f'<div class="card-title">{title}</div>'
                f'<div class="card-desc">{desc}</div>', unsafe_allow_html=True)


# ---------- เมนูซาย ----------
with st.sidebar:
    st.title("📊 Quant Desk")
    st.caption("Financial Analytics Suite")
    page = st.radio("menu", ["ภาพรวมการลงทุน", "สินเชื่อ / ผ่อนบ้าน",
                             "พันธบัตร", "วิเคราะห์หุ้น"],
                    label_visibility="collapsed")
    st.markdown("---")
    st.caption("Python · NumPy · Streamlit")


# ===== หน้า 1: การลงทุน =====
if page == "ภาพรวมการลงทุน":
    st.header("ภาพรวมการลงทุน")
    st.write("คำนวณการเติบโตของเงินตามเวลา และประเมินโครงการด้วย NPV / IRR")
    c = st.columns(3)
    rate = c[0].number_input("ดอกเบยต่อปี (%)", value=5.0, step=0.5) / 100
    pv = c[1].number_input("เงินต้น", value=100000.0, step=10000.0)
    n = int(c[2].number_input("จำนวนปี", value=10, step=1, min_value=1))
    calc = TimeValueOfMoney(rate)
    fv = calc.future_value(pv, n)
    interest = fv - pv

    m = st.columns(3)
    m[0].metric("มูลค่าอนาคต (FV)", f"{fv:,.0f}")
    m[1].metric("ดอกเบี้ยที่ได", f"{interest:,.0f}")
    m[2].metric("เติบโต", f"{(fv/pv-1)*100:,.1f}%")

    left, right = st.columns([3, 2])
    with left:
        panel("การเติบโตของเงิน", "เงินต้น (นเงิน) ทบกับดอกเบี้ยสะสม (เขียว) แต่ละปี")
        yrs = list(range(n + 1))
        fig = go.Figure()
        fig.add_bar(x=yrs, y=[pv]*(n+1), name="เงินต้น", marker_color=BLUE)
        fig.add_bar(x=yrs, y=[calc.future_value(pv, y)-pv for y in yrs],
                    name="ดอกเบี้ยสะสม", marker_color=GREEN)
        fig.update_layout(barmode="stack")
        st.plotly_chart(styled(fig), use_container_width=True)
    with right:
        panel("สัดสวนเมื่อครบกำหนด", "เงินต้นเทียบกับดอกเบี้ยที่งอกเงย")
        d = go.Figure(go.Pie(labels=["เงินต้น", "ดอกเบี้ย"], values=[pv, interest],
                             hole=0.6, marker_colors=[BLUE, GREEN]))
        st.plotly_chart(styled(d), use_container_width=True)

    st.markdown("---")
    panel("ประเมินโครงการ (NPV / IRR)", "กระแสเงินแต่ละงวด งวดแรกมักติดลบ เช่น -100000, 40000, 50000, 60000")
    cf_text = st.text_input("กระแสเงิน (คั่นด้วยจลภาค)", "-100000, 40000, 50000, 60000")
    try:
        flows = [float(x) for x in cf_text.split(",")]
        cc = st.columns(2)
        cc[0].metric("NPV", f"{calc.npv(flows):,.0f}")
        try:
            cc[1].metric("IRR", f"{calc.irr(flows)*100:,.2f}%")
        except ValueError:
            cc[1].metric("IRR", "หาไม่ได้")
        panel("กระแสเงินแต่ละงวด", "แดง = จ่ายออก, เขียว = รับเข้า")
        fig = go.Figure(go.Bar(x=[f"งวด {i}" for i in range(len(flows))], y=flows,
                               marker_color=[RED if v < 0 else GREEN for v in flows]))
        st.plotly_chart(styled(fig, 260), use_container_width=True)
    except ValueError:
        st.warning("กรอกเป็นตัวเลขคันด้วยจุลภาคเท่านั้น")


# ===== หน้า 2: สนเชื่อ =====
elif page == "สินเชื่อ / ผ่อนบ้าน":
    st.header("สินเชื่อ / ผ่อนบาน")
    st.write("คำนวณค่างวด ตารางผอน และสัดส่วนเงินต้น/ดอกเบี้ยตลอดสัญญา")
    c = st.columns(3)
    p = c[0].number_input("เงินกู้", value=3000000.0, step=100000.0)
    ar = c[1].number_input("ดอกเบี้ยต่อปี (%)", value=6.0, step=0.25) / 100
    yr = int(c[2].number_input("จำนวนปี", value=30, step=1, min_value=1))
    loan = Loan(p, ar, yr)
    sched = pd.DataFrame(loan.schedule())

    m = st.columns(3)
    m[0].metric("ค่างวด/เดือน", f"{loan.monthly_payment():,.0f}")
    m[1].metric("ดอกเบี้ยรวม", f"{loan.total_interest():,.0f}")
    m[2].metric("จ่ายทั้งหมด", f"{loan.monthly_payment()*loan.n_months:,.0f}")

    left, right = st.columns([3, 2])
    with left:
        panel("ยอดหนี้คงเหลือ", "หนี้ลดเร็วขึ้นเรือยๆ เมื่อดอกเบี้ยต่องวดน้อยลง")
        fig = go.Figure(go.Scatter(x=sched["month"], y=sched["balance"],
                        fill="tozeroy", line=dict(color=BLUE, width=2.5)))
        st.plotly_chart(styled(fig), use_container_width=True)
    with right:
        panel("เงินต้น vs ดอกเบี้ย", "ตลอดสัญญาคุณจ่ายดอกเบี้ยรวมเท่าไหร่")
        d = go.Figure(go.Pie(labels=["เงินต้น", "ดอกเบี้ย"],
                             values=[p, loan.total_interest()],
                             hole=0.6, marker_colors=[BLUE, RED]))
        st.plotly_chart(styled(d), use_container_width=True)

    sched["year"] = ((sched["month"] - 1) // 12) + 1
    yearly = sched.groupby("year")[["principal", "interest"]].sum().reset_index()
    panel("สัดส่วนการจ่ายแต่ละปี", "ช่วงแรกจ่ายดอกเบี้ยเยอะ (แดง) ปลายสัญญาตัดเงินต้นเยอะ (น้ำเงิน)")
    fig = go.Figure()
    fig.add_bar(x=yearly["year"], y=yearly["principal"], name="เงินต้น", marker_color=BLUE)
    fig.add_bar(x=yearly["year"], y=yearly["interest"], name="ดอกเบี้ย", marker_color=RED)
    fig.update_layout(barmode="stack")
    st.plotly_chart(styled(fig, 300), use_container_width=True)

    panel("ตารางผ่อน (12 เดือนแรก)", "ดูว่าแต่ละเดือนเงินไปเป็นเงินต้นหรือดอกเบี้ย")
    st.dataframe(sched.head(12).drop(columns="year"),
                 use_container_width=True, hide_index=True)


# ===== หน้า 3: พันธบัตร =====
elif page == "พันธบัตร":
    st.header("พันธบัตร")
    st.write("คำนวณราคา ความสัมพันธราคา–yield และกระแสเงินของพันธบัตร")
    c = st.columns(4)
    fvb = c[0].number_input("เงินต้น", value=1000.0, step=100.0)
    cr = c[1].number_input("คูปอง/ป (%)", value=5.0, step=0.25) / 100
    yb = int(c[2].number_input("อายุ (ปี)", value=10, step=1, min_value=1))
    ytm_in = c[3].number_input("yield (%)", value=6.0, step=0.25) / 100
    bond = Bond(fvb, cr, yb)

    m = st.columns(3)
    m[0].metric("ราคา", f"{bond.price(ytm_in):,.2f}")
    m[1].metric("YTM ที่กรอก", f"{ytm_in*100:,.2f}%")
    m[2].metric("Duration (ปี)", f"{bond.macaulay_duration(ytm_in):,.2f}")

    left, right = st.columns([3, 2])
    with left:
        panel("ราคา vs yield", "ผกผันกัน — yield ขึ้นราคาลง (เส้นประ = ราคา par)")
        ys = np.linspace(0.01, 0.15, 50)
        fig = go.Figure(go.Scatter(x=ys*100, y=[bond.price(y) for y in ys],
                        line=dict(color=BLUE, width=3)))
        fig.add_hline(y=fvb, line_dash="dash", line_color="#94a3b8")
        st.plotly_chart(styled(fig), use_container_width=True)
    with right:
        panel("ที่มาของผลตอบแทน", "คูปองรวมเทียบกับเงินตนที่ได้คืน")
        d = go.Figure(go.Pie(labels=["คูปองรวม", "เงนต้น"],
                             values=[bond.coupon*bond.n_periods, fvb],
                             hole=0.6, marker_colors=[GREEN, BLUE]))
        st.plotly_chart(styled(d), use_container_width=True)

    panel("กระแสเงินแต่ละงวด", "งวดสุดท้ายสูงเพราะได้คูปอง + เงินต้นคืน")
    flows = bond.cashflows()
    fig = go.Figure(go.Bar(x=list(range(1, len(flows)+1)), y=flows, marker_color=BLUE))
    st.plotly_chart(styled(fig, 280), use_container_width=True)
# ===== หน้า 4: หุ้น =====
elif page == "วิเคราะห์หุ้น":
    st.header("วิเคราะห์หุ้น")
    st.write("ดึงราคาจริงจากตลาด แล้ววัดผลตอบแทนและความเสี่ยง")
    c = st.columns([2, 1, 1])
    ticker = c[0].text_input("รหัสหุ้น", "AAPL")
    period = c[1].selectbox("ช่วงเวลา", ["6mo", "1y", "2y", "5y"], index=1)
    run = c[2].button("วิเคราะห์")

    if run:
        try:
            import yfinance as yf
            data = yf.download(ticker, period=period, progress=False)
            prices = data["Close"].squeeze().dropna().tolist()
            dates = list(data.index)
            if len(prices) < 2:
                raise ValueError("no data")
        except Exception:
            st.info("ดึงข้อมูลจริงไม่ได้ — ใช้ข้อมูลจำลองแทน")
            np.random.seed(0)
            prices = list(100*np.cumprod(1 + np.random.normal(0.0005, 0.02, 252)))
            dates = pd.date_range("2024-01-01", periods=len(prices))

        a = ReturnsAnalyzer(prices, risk_free_rate=0.02)
        m = st.columns(4)
        m[0].metric("ผลตอบแทน/ปี", f"{a.annualized_return()*100:,.1f}%")
        m[1].metric("ความผันผวน/ปี", f"{a.annualized_volatility()*100:,.1f}%")
        m[2].metric("Sharpe", f"{a.sharpe_ratio():,.2f}")
        m[3].metric("Max Drawdown", f"{a.max_drawdown()*100:,.1f}%")

        panel(f"ราคา {ticker}", "เส้นราคาปิดตามเวลา")
        fig = go.Figure(go.Scatter(x=dates, y=prices, fill="tozeroy",
                        line=dict(color=BLUE, width=2)))
        st.plotly_chart(styled(fig), use_container_width=True)

        rets = a.daily_returns()
        left, right = st.columns([3, 2])
        with left:
            panel("ผลตอบแทนรายวัน", "เขียว = วันบวก, แดง = วันลบ")
            fig = go.Figure(go.Bar(x=dates[1:], y=rets,
                marker_color=[GREEN if r >= 0 else RED for r in rets]))
            st.plotly_chart(styled(fig, 280), use_container_width=True)
        with right:
            panel("ราคาล่าสุด", "10 วันทำการล่าสุด")
            df = pd.DataFrame({"วันที่": [str(d)[:10] for d in dates[-10:]],
                               "ราคาปิด": [round(x, 2) for x in prices[-10:]]})
            st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("กรอกรหัสหุ้นแล้วกด 'วิเคราะห์'")