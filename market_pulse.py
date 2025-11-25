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

# KPIs
with mid:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div style='display:flex; gap:32px; align-items:center;'>", unsafe_allow_html=True)
    if sector == "Technology":
        f_cur = df_win["Funding_ZAR_M"].iloc[-1]
        f_prev = df_win["Funding_ZAR_M"].iloc[-2]
        s_cur = df_win["Sentiment"].iloc[-1]
        g_cur = df_win["Growth_YoY_%"].iloc[-1]
        m_cur = int(df_win["Social_Mentions"].iloc[-1])
        st.markdown(f"""
            <div>
              <div class='kpi'>R {f_cur:,.1f}M</div>
              <div class='kpi-label'>Funding (window)</div>
            </div>
            <div>
              <div class='kpi'>{s_cur}</div>
              <div class='kpi-label'>Market Sentiment (0-100)</div>
            </div>
            <div>
              <div class='kpi'>{g_cur}%</div>
              <div class='kpi-label'>YoY Growth</div>
            </div>
            <div>
              <div class='kpi'>{m_cur:,}</div>
              <div class='kpi-label'>Social Mentions</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        inv_cur = df_win["Investment_ZAR_M"].iloc[-1]
        ad_cur = df_win["Adoption_%"].iloc[-1]
        s_cur = df_win["Sentiment"].iloc[-1]
        p_cur = int(df_win["Policy_Mentions"].iloc[-1])
        st.markdown(f"""
            <div>
              <div class='kpi'>R {inv_cur:,.1f}M</div>
              <div class='kpi-label'>Investment (window)</div>
            </div>
            <div>
              <div class='kpi'>{ad_cur}%</div>
              <div class='kpi-label'>Adoption Rate</div>
            </div>
            <div>
              <div class='kpi'>{s_cur}</div>
              <div class='kpi-label'>Market Sentiment (0-100)</div>
            </div>
            <div>
              <div class='kpi'>{p_cur:,}</div>
              <div class='kpi-label'>Policy Mentions</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# charts & history
with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Trend (window)")
    if sector == "Technology":
        st.line_chart(df_win.set_index("date")[["Funding_ZAR_M", "Sentiment", "Growth_YoY_%"]])
    else:
        st.line_chart(df_win.set_index("date")[["Investment_ZAR_M", "Adoption_%", "Sentiment"]])
    st.markdown("</div>", unsafe_allow_html=True)
