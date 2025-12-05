import streamlit as st
import pandas as pd
import numpy as np

# =============================================
# PAGE CONFIG
# =============================================

st.set_page_config(page_title="BN Pulse Board", layout="wide")

# =============================================
# STYLE — CLEAN SIMPLIFIED
# =============================================

st.markdown("""
<style>
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
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =============================================
# SYNTHETIC DATA GENERATION FUNCTION
# =============================================

def generate_sector_data(seed=42):
    np.random.seed(seed)

    # Create multiple granular date levels
    dates_1h = pd.date_range(start="2026-01-01", periods=24*60, freq="H")  # 60 days hourly
    dates_1d = pd.date_range(start="2025-01-01", periods=400, freq="D")
    
    # Base metrics for all sectors
    def build_df(dates):
        return pd.DataFrame({
            "date": dates,
            "Funding_ZAR_M": np.random.uniform(10, 300, len(dates)).round(2),
            "Sentiment": np.random.uniform(5, 95, len(dates)).round(1),
            "Growth_YoY_%": np.random.uniform(-5, 20, len(dates)).round(1),
            "Mentions": np.random.uniform(100, 5000, len(dates)).round()
        })

    df_hourly = build_df(dates_1h)
    df_daily = build_df(dates_1d)

    return {
        "hourly": df_hourly,
        "daily": df_daily
    }

# =============================================
# CREATE DATA FOR ALL SECTORS
# =============================================

sector_data = {
    "ICT": generate_sector_data(1),
    "FinTech": generate_sector_data(2),
    "AgriTech": generate_sector_data(3),
    "Health & Wellness": generate_sector_data(4),
    "Tourism & Hospitality": generate_sector_data(5),
}

# =============================================
# TIMEFRAME AGGREGATION FUNCTION
# =============================================

def get_timeframe_df(df_hourly, df_daily, timeframe):

    df = pd.concat([df_hourly, df_daily]).drop_duplicates("date").sort_values("date")
    df = df.set_index("date")

    if timeframe == "1H":
        return df.resample("H").mean().dropna().reset_index()

    elif timeframe == "4H":
        return df.resample("4H").mean().dropna().reset_index()

    elif timeframe == "1D":
        return df.resample("D").mean().dropna().reset_index()

    elif timeframe == "1W":
        return df.resample("W").mean().dropna().reset_index()

    elif timeframe == "1M":
        return df.resample("M").mean().dropna().reset_index()

    elif timeframe == "3M":
        return df.resample("Q").mean().dropna().reset_index()

    elif timeframe == "6M":
        return df.resample("2Q").mean().dropna().reset_index()

    elif timeframe == "1Y":
        return df.resample("A").mean().dropna().reset_index()

    return df.reset_index()

# =============================================
# REPORT DOWNLOAD (CENTER)
# =============================================

colA, colB, colC = st.columns([1, 2, 1])
with colB:
    st.download_button(
        label="📄 Download Sector Report",
        data="Preview of auto-generated report...",
        file_name="BN_Market_Report.pdf",
        type="secondary",
        use_container_width=True
    )

# =============================================
# SELECTOR — SECTOR & TIMEFRAME
# =============================================

sector = st.selectbox("Sector", list(sector_data.keys()), label_visibility="collapsed")

timeframe = st.selectbox(
    "Timeframe",
    ["1D", "1W", "1M", "3M", "6M", "1Y"],
    label_visibility="collapsed"
)

# =============================================
# LOAD DATA FOR SELECTED SECTOR + TIMEFRAME
# =============================================

df_daily = sector_data[sector]["daily"]

df_win = get_timeframe_df(df_daily, timeframe)

# =============================================
# KPIs — ALWAYS LAST VALUE OF FILTERED DATA
# =============================================

latest = df_win.iloc[-1]

kpi1 = latest["Funding_ZAR_M"]
kpi2 = latest["Sentiment"]
kpi3 = latest["Growth_YoY_%"]
kpi4 = int(latest["Mentions"])

st.markdown("<div class='card'>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div>
          <div class='kpi'>R {kpi1:,.1f}M</div>
          <div class='kpi-label'>Funding</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div>
          <div class='kpi'>{kpi2}</div>
          <div class='kpi-label'>Market Sentiment</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div>
          <div class='kpi'>{kpi3}%</div>
          <div class='kpi-label'>YoY Growth</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div>
          <div class='kpi'>{kpi4:,}</div>
          <div class='kpi-label'>Mentions</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# =============================================
# TREND CHART
# =============================================

chart_cols = st.columns([0.05, 0.9, 0.05])
with chart_cols[1]:
    st.line_chart(
        df_win.set_index("date")[["Funding_ZAR_M", "Sentiment", "Growth_YoY_%"]],
        height=260
    )



