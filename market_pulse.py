import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time

# ============================
# PAGE CONFIG
# ============================

st.set_page_config(page_title="BN Pulse Board", layout="wide")

# Remove padding and add animations
st.markdown("""
<style>
body { margin:0; padding:0; }
div.block-container { padding-top: 0rem; }

/* Card styling */
.card {
    background-color: rgba(255,255,255,0.04);
    border-radius: 8px;
    padding: 10px 14px;
    border-left: 4px solid #4CC9F0;
    animation: pulse 2s infinite;
}

/* KPI animations */
.kpi {
    font-size: 1.25rem;
    font-weight: 600;
    background: linear-gradient(90deg, #4CC9F0, #4361EE);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: kpiPulse 3s ease-in-out infinite;
}

.kpi-label {
    font-size: 0.75rem;
    color: #ccc;
}

/* Animations */
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(76, 201, 240, 0.4); }
    70% { box-shadow: 0 0 0 10px rgba(76, 201, 240, 0); }
    100% { box-shadow: 0 0 0 0 rgba(76, 201, 240, 0); }
}

@keyframes kpiPulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.8; }
}

@keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

/* Update indicator */
.update-indicator {
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 0.7rem;
    color: #4CC9F0;
    animation: blink 1s infinite;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* Live badge */
.live-badge {
    display: inline-block;
    background: linear-gradient(90deg, #FF416C, #FF4B2B);
    color: white;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.7rem;
    font-weight: bold;
    animation: fadeInOut 2s infinite;
    margin-left: 8px;
}

@keyframes fadeInOut {
    0%, 100% { opacity: 0.3; transform: scale(0.95); }
    50% { opacity: 1; transform: scale(1); }
}

/* Sector selector styling */
.sector-selector-container {
    background: rgba(20, 20, 40, 0.7);
    border-radius: 12px;
    padding: 15px;
    margin: 10px 0;
    border: 1px solid rgba(76, 201, 240, 0.2);
}

footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ============================
# SYNTHETIC DAILY-LIVE DATA WITH REAL-TIME UPDATES
# ============================

def generate_live_timeseries(days=150, base_trend=None):
    """Generate realistic rolling market data over time with real-time fluctuations."""
    today = datetime.date.today()
    dates = pd.date_range(end=today, periods=days, freq="D")
    
    # Add small real-time fluctuations
    real_time_noise = np.random.normal(0, 0.1, size=days)
    
    if base_trend is None:
        base_up = np.cumsum(np.random.normal(0.3, 0.9, size=days)) + real_time_noise
        base_flat = np.cumsum(np.random.normal(0.01, 0.4, size=days)) + real_time_noise * 0.5
        base_vol = np.abs(np.random.normal(0, 1, size=days)) + np.abs(real_time_noise) * 2
    else:
        base_up = base_trend[0] + real_time_noise
        base_flat = base_trend[1] + real_time_noise * 0.5
        base_vol = base_trend[2] + np.abs(real_time_noise) * 2
    
    return dates, base_up, base_flat, base_vol


def build_sector(name, iteration=0):
    """Build sector data with time-based variations for slideshow effect."""
    dates, t1, t2, t3 = generate_live_timeseries()
    
    # Add iteration-based variation for slideshow effect
    phase = iteration * 0.1
    t1 = t1 + np.sin(np.linspace(0, 2*np.pi, len(t1)) + phase) * 2
    t2 = t2 + np.cos(np.linspace(0, 2*np.pi, len(t2)) + phase) * 1.5
    t3 = t3 + np.sin(np.linspace(0, 2*np.pi, len(t3)) + phase * 2) * 1

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


# ============================
# STATE MANAGEMENT FOR AUTO-ROTATION
# ============================

if 'sector_index' not in st.session_state:
    st.session_state.sector_index = 0
    st.session_state.iteration = 0
    st.session_state.last_update = datetime.datetime.now()

# Auto-advance sectors every 10 seconds
time_diff = (datetime.datetime.now() - st.session_state.last_update).total_seconds()
if time_diff > 10:  # Change sector every 10 seconds
    st.session_state.sector_index = (st.session_state.sector_index + 1) % 5
    st.session_state.iteration += 1
    st.session_state.last_update = datetime.datetime.now()

# ============================
# GENERATE DATA WITH ITERATION
# ============================

sector_names = ["ICT", "FinTech", "AgriTech", "Health & Wellness", "Tourism & Hospitality"]
all_sectors = {name: build_sector(name, st.session_state.iteration) for name in sector_names}

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
# SECTOR SELECTOR WITH AUTO-ROTATION
# ============================

# Manual sector selector
sector = st.selectbox(
    "Choose sector (auto-rotates every 10 seconds)",
    sector_names,
    index=st.session_state.sector_index,
    key="sector_selector",
    label_visibility="collapsed"
)

st.markdown("</div>", unsafe_allow_html=True)

# Update index if manually selected
if sector != current_sector:
    st.session_state.sector_index = sector_names.index(sector)
    st.rerun()

df = all_sectors[sector]

# ============================
# LIVE KPIs — ANIMATED
# ============================

st.markdown("<div class='card'>", unsafe_allow_html=True)

if sector in ["ICT", "FinTech"]:
    cols = st.columns(4)
    
    metrics = [
        (f"R {df['Funding_ZAR_M'].iloc[-1]:,.1f}M", "Funding", "#4CC9F0"),
        (f"{df['Sentiment'].iloc[-1]}", "Sentiment (0–100)", "#F72585"),
        (f"{df['Growth_YoY_%'].iloc[-1]}%", "YoY Growth", "#7209B7"),
        (f"{int(df['Social_Mentions'].iloc[-1]):,}", "Social Mentions", "#3A0CA3")
    ]
    
    for (value, label, color), col in zip(metrics, cols):
        with col:
            st.markdown(f"""
            <div>
                <div class='kpi' style='background: linear-gradient(90deg, {color}, #4361EE); -webkit-background-clip: text;'>{value}</div>
                <div class='kpi-label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

else:
    cols = st.columns(4)
    
    metrics = [
        (f"R {df['Investment_ZAR_M'].iloc[-1]:,.1f}M", "Investment", "#4CC9F0"),
        (f"{df['Adoption_%'].iloc[-1]}%", "Adoption Rate", "#F72585"),
        (f"{df['Sentiment'].iloc[-1]}", "Sentiment", "#7209B7"),
        (f"{int(df['Policy_Mentions'].iloc[-1]):,}", "Policy Mentions", "#3A0CA3")
    ]
    
    for (value, label, color), col in zip(metrics, cols):
        with col:
            st.markdown(f"""
            <div>
                <div class='kpi' style='background: linear-gradient(90deg, {color}, #4361EE); -webkit-background-clip: text;'>{value}</div>
                <div class='kpi-label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ============================
# TREND CHART — ANIMATED
# ============================

st.markdown("<div style='animation: slideIn 0.5s ease-out;'>", unsafe_allow_html=True)
trend = st.columns([0.05, 0.9, 0.05])
with trend[1]:
    numeric_cols = df.select_dtypes(include=[np.number]).drop(columns=["Social_Mentions", "Policy_Mentions"], errors="ignore")
    st.line_chart(numeric_cols.set_index(df["date"]), height=240)
st.markdown("</div>", unsafe_allow_html=True)

# ============================
# AUTO-REFRESH
# ============================

# Auto-refresh the page every 5 seconds for live updates
time.sleep(5)  # Refresh every 5 seconds
st.rerun()



