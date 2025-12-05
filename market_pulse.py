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

