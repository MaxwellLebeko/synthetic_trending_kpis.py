import streamlit as st
import pandas as pd
import numpy as np

##### ============================
##### PAGE CONFIG — CLEAN EMBEDDING
##### ============================

st.set_page_config(page_title="BN Pulse Board", layout="wide")

# Remove padding
st.markdown("""
<style>
body { margin:0; padding:0; }
div.block-container { padding-top: 0rem; }
.card {
  background-color: rgba(255,255,255,0.04);
  border-radius: 8px;
  padding: 10px 14px;
}
.kpi {
  font-size: 1.25rem;
  font-weight: 600;
}
.kpi-label {
  font-size: 0.75rem;
  color: #ccc;
}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True

##### ============================
##### SYNTHETIC MARKET DATA
##### ============================

np.random.seed(42)

dates = pd.date_range(start="2024-01-01", periods=30, freq="D")

tech = pd.DataFrame({
    "date": dates,
    "Funding_ZAR_M": np.random.uniform(20, 200, size=len(dates)).round(2),
    "Sentiment": np.random.uniform(10, 90, size=len(dates)).round(1),
    "Growth_YoY_%": np.random.uniform(-3, 15, size=len(dates)).round(1),
    "Social_Mentions": np.random.uniform(200, 3000, size=len(dates)).round()
})

energy = pd.DataFrame({
    "date": dates,
    "Investment_ZAR_M": np.random.uniform(10, 120, size=len(dates)).round(2),
    "Sentiment": np.random.uniform(10, 90, size=len(dates)).round(1),
    "Adoption_%": np.random.uniform(2, 38, size=len(dates)).round(1),
    "Policy_Mentions": np.random.uniform(100, 1300, size=len(dates)).round()
})

synthetic_data = {"Technology": tech, "Energy": energy}



##### ============================
##### UI — NO TITLES, CLEAN MINIMAL
##### ============================

# small padding removal
st.markdown("""<style>
body { margin: 0; padding:0; }
div.block-container { padding-top: 0rem; }
.card {
  background-color: rgba(255,255,255,0.04);
  border-radius: 8px;
  padding: 10px 14px;
}
.kpi {
  font-size: 1.25rem;
  font-weight: 600;
}
.kpi-label {
  font-size: 0.75rem;
  color: #ccc;
}
</style>""", unsafe_allow_html=True)


##### ============================
##### REPORT DOWNLOAD (CENTER)
##### ============================

colA, colB, colC = st.columns([1, 2, 1])
with colB:
    st.download_button(
        label="📄 Download Sector Report",
        data="Preview report content...",
        file_name="BN_Market_Report.pdf",
        type="secondary",
        use_container_width=True
    )


##### ============================
##### SECTOR SELECTOR
##### ============================

sector = st.selectbox("Select Sector", ["Technology", "Energy"], label_visibility="collapsed")
df_win = synthetic_data[sector]




##### ============================
##### KPIs — FULL ORIGINAL METRICS ABOVE CHART
##### ============================

# KPI row centered
kpi_cols = st.columns([0.05, 0.9, 0.05])
with kpi_cols[1]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div style='display:flex; justify-content:space-between; gap:32px;'>", unsafe_allow_html=True)

    if sector == "Technology":
        f_cur = df_win["Funding_ZAR_M"].iloc[-1]
        s_cur = df_win["Sentiment"].iloc[-1]
        g_cur = df_win["Growth_YoY_%"].iloc[-1]
        m_cur = int(df_win["Social_Mentions"].iloc[-1])

        st.markdown(f"""
            <div>
              <div class='kpi'>R {f_cur:,.1f}M</div>
              <div class='kpi-label'>Funding</div>
            </div>
            <div>
              <div class='kpi'>{s_cur}</div>
              <div class='kpi-label'>Sentiment</div>
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
              <div class='kpi-label'>Investment</div>
            </div>
            <div>
              <div class='kpi'>{ad_cur}%</div>
              <div class='kpi-label'>Adoption</div>
            </div>
            <div>
              <div class='kpi'>{s_cur}</div>
              <div class='kpi-label'>Sentiment</div>
            </div>
            <div>
              <div class='kpi'>{p_cur:,}</div>
              <div class='kpi-label'>Policy Mentions</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


##### ============================
##### TREND CHART BELOW KPIs
##### ============================

chart_row = st.columns([0.05, 0.9, 0.05])
with chart_row[1]:
    if sector == "Technology":
        st.line_chart(df_win.set_index("date")[["Funding_ZAR_M", "Sentiment", "Growth_YoY_%"]], height=260)
    else:
        st.line_chart(df_win.set_index("date")[["Investment_ZAR_M", "Adoption_%", "Sentiment"]], height=260)

