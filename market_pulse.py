import streamlit as st
import pandas as pd
import numpy as np

##### ============================
##### PAGE CONFIG — CLEAN EMBEDDING
##### ============================

st.set_page_config(
    page_title="BN Pulse Board",
    layout="wide",
)

##### ============================
##### SYNTHETIC MARKET DATA
##### ============================

np.random.seed(42)

sectors = ["Technology", "Energy"]

synthetic_data = {}

for sec in sectors:
    synthetic_data[sec] = pd.DataFrame({
        "date": pd.date_range(start="2024-01-01", periods=20, freq="D"),
        "market_index": np.random.uniform(80, 120, size=20).round(2),
        "trade_volume": np.random.uniform(1000, 5000, size=20).round(),
        "sentiment": np.random.uniform(-1, 1, size=20).round(2)
    })


##### ============================
##### UI — NO TITLES, CLEAN MINIMAL
##### ============================

# Centered download report section
colA, colB, colC = st.columns([1, 2, 1])
with colB:
    st.download_button(
        label="📄 Download Sector Report",
        data="Report content demo…",
        file_name="BN_Market_Report.pdf",
        type="secondary",
        use_container_width=True
    )

st.markdown("""<style>
body { margin: 0; padding:0; }
div.block-container { padding-top: 0rem; }
</style>""", unsafe_allow_html=True)


##### ============================
##### KPI STRIP — HORIZONTAL
##### ============================

sector_choice = st.selectbox("Select Sector", sectors, label_visibility="collapsed")
df = synthetic_data[sector_choice]
latest = df.iloc[-1]

col1, col2, col3 = st.columns(3)

col1.metric("📊 Market Index", latest["market_index"])
col2.metric("📦 Trade Volume", latest["trade_volume"])
col3.metric("😊 Sentiment Score", latest["sentiment"])


##### ============================
##### MAIN FEATURE — TREND CHART
##### ============================

trend_cols = st.columns([0.05, 0.9, 0.05])
with trend_cols[1]:
    st.line_chart(
        df.set_index("date")[["market_index"]],
        height=250
    )
