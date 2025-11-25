import streamlit as st
import pandas as pd
import numpy as np
import datetime

# ---- REQUIRED FOR EMBEDDING (prevents redirect loops) ----
st.set_page_config(page_title="BN Pulse Board", layout="wide")

# Hides Streamlit default UI
hide_default_format = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stApp { background: linear-gradient(180deg, #071028 0%, #0d2338 100%); color: #E6F0FF; }
.card { background: rgba(255,255,255,0.05); padding: 18px; border-radius: 12px; }
.kpi { font-size: 28px; font-weight:700; }
.kpi-label { color:#9FB6D9; font-size:12px; }
.small { color:#9FB6D9; font-size:12px; }
</style>
"""
st.markdown(hide_default_format, unsafe_allow_html=True)

# ---- Title ----
st.markdown("<h2 style='color:#DDEAFF;'>BN Pulse Board — Trending Markets</h2>", unsafe_allow_html=True)
st.caption("Sectors: Technology & Energy — synthetic demo data for UI testing")

# ---- synthetic data generator ----
np.random.seed(42)

def random_walk(base, days=30, vol=0.03):
    changes = np.random.normal(loc=0.0, scale=vol, size=days)
    vals = [base]
    for c in changes:
        vals.append(max(vals[-1] * (1 + c), 0.01))
    return vals[1:]

def generate_sector_df(sector):
    days = 30
    dates = [datetime.date.today() - datetime.timedelta(days=(days - 1 - i)) for i in range(days)]
    if sector == "Technology":
        df = pd.DataFrame({
            "date": dates,
            "Funding_ZAR_M": np.round(random_walk(base=480, days=days, vol=0.06), 1),
            "Sentiment": np.round(random_walk(base=68, days=days, vol=0.02), 1),
            "Growth_YoY_%": np.round(random_walk(base=22, days=days, vol=0.015), 2),
            "Social_Mentions": np.round(random_walk(base=4200, days=days, vol=0.08), 0)
        })
    else:  # Energy
        df = pd.DataFrame({
            "date": dates,
            "Investment_ZAR_M": np.round(random_walk(base=640, days=days, vol=0.05), 1),
            "Adoption_%": np.round(random_walk(base=15, days=days, vol=0.012), 2),
            "Sentiment": np.round(random_walk(base=72, days=days, vol=0.018), 1),
            "Policy_Mentions": np.round(random_walk(base=900, days=days, vol=0.06), 0)
        })
    return df

# ---- UI Layout ----
left, mid, right = st.columns([1, 2.5, 1])

with left:
    sector = st.radio("Sector", ["Technology", "Energy"], index=0)
    freq = st.selectbox("Window", ["7 days", "14 days", "30 days"], index=2)
    st.caption("Demo synthetic KPIs")

df = generate_sector_df(sector)
window = int(freq.split()[0])
df_win = df.tail(window)

# ---- KPIs ----
with mid:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div style='display:flex; gap:42px; align-items:center;'>", unsafe_allow_html=True)

    if sector == "Technology":
        f_cur = df_win["Funding_ZAR_M"].iloc[-1]
        s_cur = df_win["Sentiment"].iloc[-1]
        g_cur = df_win["Growth_YoY_%"].iloc[-1]
        m_cur = int(df_win["Social_Mentions"].iloc[-1])
        st.markdown(f"""
            <div><div class='kpi'>R {f_cur:,.1f}M</div><div class='kpi-label'>Funding</div></div>
            <div><div class='kpi'>{s_cur}</div><div class='kpi-label'>Sentiment</div></div>
            <div><div class='kpi'>{g_cur}%</div><div class='kpi-label'>YoY Growth</div></div>
            <div><div class='kpi'>{m_cur:,}</div><div class='kpi-label'>Social Mentions</div></div>
        """, unsafe_allow_html=True)

    else:
        inv_cur = df_win["Investment_ZAR_M"].iloc[-1]
        ad_cur = df_win["Adoption_%"].iloc[-1]
        s_cur = df_win["Sentiment"].iloc[-1]
        p_cur = int(df_win["Policy_Mentions"].iloc[-1])
        st.markdown(f"""
            <div><div class='kpi'>R {inv_cur:,.1f}M</div><div class='kpi-label'>Investment</div></div>
            <div><div class='kpi'>{ad_cur}%</div><div class='kpi-label'>Adoption</div></div>
            <div><div class='kpi'>{s_cur}</div><div class='kpi-label'>Sentiment</div></div>
            <div><div class='kpi'>{p_cur:,}</div><div class='kpi-label'>Policy Mentions</div></div>
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

# ---- charts ----
with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Trend")
    if sector == "Technology":
        st.line_chart(df_win.set_index("date")[["Funding_ZAR_M", "Sentiment"]])
    else:
        st.line_chart(df_win.set_index("date")[["Investment_ZAR_M", "Sentiment"]])
    st.markdown("</div>", unsafe_allow_html=True)

# ---- table ----
st.subheader(f"{sector} — Data snapshot (last {window} days)")
st.dataframe(df_win.reset_index(drop=True).assign(date=df_win['date'].astype(str)))

# ---- footer ----
st.caption(f"Generated: {datetime.datetime.now().isoformat(timespec='seconds')} — Synthetic demo data only.")
