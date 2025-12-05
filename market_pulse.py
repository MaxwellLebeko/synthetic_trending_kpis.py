import streamlit as st
import pandas as pd
import numpy as np
import datetime

# ============================
# PAGE CONFIG
# ============================

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
""", unsafe_allow_html=True)


# ============================
# SYNTHETIC DAILY-LIVE DATA
# ============================

def generate_live_timeseries(days=150):
    """Generate realistic rolling market data over time."""
    today = datetime.date.today()
    dates = pd.date_range(end=today, periods=days, freq="D")

    base_up = np.cumsum(np.random.normal(0.3, 0.9, size=days))  # trending upward
    base_flat = np.cumsum(np.random.normal(0.01, 0.4, size=days))  # sideways trend
    base_vol = np.abs(np.random.normal(0, 1, size=days))  # noisy

    return dates, base_up, base_flat, base_vol


def build_sector(name):
    dates, t1, t2, t3 = generate_live_timeseries()

    if name == "ICT":
        return pd.DataFrame({
            "date": dates,
            "Funding_ZAR_M": (50 + t1 * 2).round(2),
            "Sentiment": (50 + t2).clip(1, 99).round(1),
            "Growth_YoY_%": (5 + t3).round(1),
            "Social_Mentions": (500 + t1 * 10 + np.random.randint(0, 200, len(dates))).round()
        })

    if name == "FinTech":
        return pd.DataFrame({
            "date": dates,
            "Funding_ZAR_M": (80 + t1 * 3).round(2),
            "Sentiment": (40 + t2 * 1.2).clip(1, 99).round(1),
            "Growth_YoY_%": (2 + t3 * 0.5).round(1),
            "Social_Mentions": (300 + t1 * 8 + np.random.randint(0, 150, len(dates))).round()
        })

    if name == "AgriTech":
        return pd.DataFrame({
            "date": dates,
            "Investment_ZAR_M": (40 + t1 * 2.5).round(2),
            "Sentiment": (55 + t2).clip(1, 99).round(1),
            "Adoption_%": (10 + t3).round(1),
            "Policy_Mentions": (200 + np.abs(t2) * 5).round()
        })

    if name == "Health & Wellness":
        return pd.DataFrame({
            "date": dates,
            "Investment_ZAR_M": (60 + t1 * 1.5).round(2),
            "Sentiment": (45 + t2).clip(1, 99).round(1),
            "Adoption_%": (20 + t3).round(1),
            "Policy_Mentions": (250 + np.abs(t3) * 10).round()
        })

    if name == "Tourism & Hospitality":
        return pd.DataFrame({
            "date": dates,
            "Investment_ZAR_M": (70 + t1 * 2).round(2),
            "Sentiment": (50 + t2 * 1.1).clip(1, 99).round(1),
            "Adoption_%": (15 + t3 * 1.3).round(1),
            "Policy_Mentions": (300 + np.abs(t1)).round()
        })


# map sectors to dataframes
all_sectors = {
    "ICT": build_sector("ICT"),
    "FinTech": build_sector("FinTech"),
    "AgriTech": build_sector("AgriTech"),
    "Health & Wellness": build_sector("Health & Wellness"),
    "Tourism & Hospitality": build_sector("Tourism & Hospitality")
}



# ============================
# REPORT BUTTON (center-top)
# ============================

colA, colB, colC = st.columns([1, 2, 1])
with colB:
    st.download_button(
        label="📄 Download Sector Report",
        data="Preview report content...",
        file_name="BN_Market_Report.pdf",
        type="secondary",
        use_container_width=True
    )



# ============================
# SECTOR SELECTOR
# ============================

sector = st.selectbox(
    "Choose sector",
    list(all_sectors.keys()),
    label_visibility="collapsed"
)

df = all_sectors[sector]



# ============================
# KPIs — HORIZONTAL
# ============================

st.markdown("<div class='card'>", unsafe_allow_html=True)

if sector in ["ICT", "FinTech"]:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div><div class='kpi'>R {df['Funding_ZAR_M'].iloc[-1]:,.1f}M</div>
        <div class='kpi-label'>Funding</div></div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div><div class='kpi'>{df['Sentiment'].iloc[-1]}</div>
        <div class='kpi-label'>Sentiment (0–100)</div></div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div><div class='kpi'>{df['Growth_YoY_%'].iloc[-1]}%</div>
        <div class='kpi-label'>YoY Growth</div></div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div><div class='kpi'>{int(df['Social_Mentions'].iloc[-1]):,}</div>
        <div class='kpi-label'>Social Mentions</div></div>
        """, unsafe_allow_html=True)


else:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div><div class='kpi'>R {df['Investment_ZAR_M'].iloc[-1]:,.1f}M</div>
        <div class='kpi-label'>Investment</div></div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div><div class='kpi'>{df['Adoption_%'].iloc[-1]}%</div>
        <div class='kpi-label'>Adoption Rate</div></div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div><div class='kpi'>{df['Sentiment'].iloc[-1]}</div>
        <div class='kpi-label'>Sentiment</div></div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div><div class='kpi'>{int(df['Policy_Mentions'].iloc[-1]):,}</div>
        <div class='kpi-label'>Policy Mentions</div></div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)



# ============================
# TREND CHART — CENTERED
# ============================

trend = st.columns([0.05, 0.9, 0.05])
with trend[1]:
    numeric_cols = df.select_dtypes(include=[np.number]).drop(columns=["Social_Mentions", "Policy_Mentions"], errors="ignore")
    st.line_chart(numeric_cols.set_index(df["date"]), height=240)



# ============================
# OPTIONAL: DATA TABLE (hidden by default)
# ============================

with st.expander("📊 View full dataset"):
    st.dataframe(df, height=300)
