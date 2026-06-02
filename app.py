import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import difflib
import random

# --- 1. THEME & UI CONFIGURATION ---
st.set_page_config(page_title="Predictive Skill Gap Intelligence Hub", layout="wide", page_icon="🔬")

st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    .stMetric { background-color: #FFFDE7; border: 1px solid #FFF59D; border-radius: 12px; padding: 15px; }
    .stTabs [data-baseweb="tab-list"] { gap: 12px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #FFFDE7; border-radius: 8px; padding: 12px 20px; border: 1px solid #FFF59D;
        font-weight: bold; color: #5D4037;
    }
    .stTabs [aria-selected="true"] { background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; }
    h1, h2, h3 { color: #5D4037; font-family: 'Georgia', serif; }
    </style>
""", unsafe_allow_html=True)

# --- 2. MULTI-DIMENSIONAL DATASET (Real 2025-26 GSDP Projections) ---
MASTER_DATA = {
    "Maharashtra": [19.1, 72.9, 10.9], "Tamil Nadu": [13.1, 80.3, 13.7],
    "Uttar Pradesh": [26.8, 80.9, 12.8], "Karnataka": [12.9, 77.6, 11.2],
    "Gujarat": [23.2, 72.6, 10.1], "West Bengal": [22.6, 88.4, 7.2],
    "Rajasthan": [26.9, 75.8, 12.6], "Telangana": [17.4, 78.5, 14.5],
    "Andhra Pradesh": [15.9, 80.5, 10.4], "Madhya Pradesh": [23.3, 77.4, 9.4],
    "Kerala": [8.5, 76.9, 11.9], "Delhi": [28.7, 77.1, 9.2],
    "Haryana": [29.1, 76.1, 11.3], "Odisha": [20.3, 85.8, 12.4],
    "Bihar": [25.6, 85.1, 14.5], "Assam": [26.1, 91.7, 12.1],
    "Sikkim": [27.5, 88.5, 14.7], "Goa": [15.3, 74.1, 12.5],
    "Punjab": [30.7, 76.8, 9.3], "Uttarakhand": [30.1, 79.0, 13.9]
}

# --- 3. ADVANCED ANALYTICS ENGINE ---
class ResearchEngine:
    @staticmethod
    def synthesize_skills(query):
        seed = sum(ord(c) for c in query)
        random.seed(seed)
        p = ["Quantum", "Neuromorphic", "Agentic", "Synthetic", "Autonomous", "Stochastic"]
        s = ["Orchestration", "Engineering", "Ethics", "Governance", "Architecture"]
        return [f"{random.choice(p)} {query} {random.choice(s)}" for _ in range(6)]

    @staticmethod
    def calculate_weighted_hub(query, geo_df):
        q = query.lower()
        weights = {
            "tech": ["Karnataka", "Telangana", "Maharashtra"],
            "data": ["Karnataka", "Delhi", "Telangana"],
            "mechanic": ["Tamil Nadu", "Gujarat", "Maharashtra"],
            "energy": ["Gujarat", "Rajasthan", "Andhra Pradesh"],
            "robot": ["Tamil Nadu", "Karnataka", "Haryana"]
        }
        geo_df['Dynamic_Momentum'] = geo_df['Growth']
        for key, states in weights.items():
            if key in q:
                geo_df.loc[geo_df['State'].isin(states), 'Dynamic_Momentum'] += 5.5
        return geo_df.nlargest(1, 'Dynamic_Momentum').iloc[0]

# --- 4. SIDEBAR COMMAND CENTER ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=60)
    st.header("⚙️ Research Parameters")
    manual_domain = st.text_input("Enter Focus Domain", "Quantum Data Analytics")
    target_firm = st.text_input("Target Enterprise", "Wipro Digital")
    st.divider()
    investment = st.slider("National R&D Investment (%)", 0, 100, 45)
    automation = st.slider("Automation Velocity (%)", 0, 100, 60)
    volatility = st.slider("Market Risk Coefficient", 1, 50, 15)
    policy_strength = st.slider("Policy Intervention Strength", 0, 100, 30)
    
    engine = ResearchEngine()
    future_competencies = engine.synthesize_skills(manual_domain)

# --- 5. DATA COMPUTATION ---
geo_df = pd.DataFrame([{"State": k, "Lat": v[0], "Lon": v[1], "Growth": v[2]} for k, v in MASTER_DATA.items()])
best_hub = engine.calculate_weighted_hub(manual_domain, geo_df)

years = np.arange(2024, 2031)
t = years - 2024
policy_boost = policy_strength / 500
d_rate = (best_hub['Growth']/100) + (automation/300) - (volatility/600)
s_rate = (best_hub['Growth']/100) + (investment/200) + policy_boost

demand_curve = 500 * (1 + d_rate)**t
supply_curve = 480 * (1 + s_rate)**t

# --- 6. MAIN UI ---
st.title("🔬 Predictive Skill Gap Intelligence Hub 2030")
st.markdown(f"**Research Target:** {manual_domain} @ {target_firm} | **System Status:** Active Simulation")

# Top KPI Strip
m1, m2, m3, m4 = st.columns(4)
gap_val = int(demand_curve[-1] - supply_curve[-1])
m1.metric("2030 Labor Demand", f"{int(demand_curve[-1])}k")
m2.metric("2030 Talent Supply", f"{int(supply_curve[-1])}k")
m3.metric("Critical Talent Gap", f"{abs(gap_val)}k", f"{int((gap_val/demand_curve[-1])*100)}%", delta_color="inverse")
m4.metric("GDP at Risk (2030)", f"₹{abs(gap_val) * 1.5:.1f} Cr")

# --- 7. TABBED FUNCTIONALITY ---
tabs = st.tabs(["📊 Forecasts", "🗺️ Opportunity Hotspots", "🧬 Skill-Bridge Analysis", "🛡️ Decision Support Sandbox", "🔗 Cluster Analysis"])

# --- TAB 1: FORECASTS ---
with tabs[0]:
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Probabilistic Demand-Supply Convergence**")
        
        fig_fore = go.Figure()
        fig_fore.add_trace(go.Scatter(x=years, y=demand_curve, name="Median Demand", line=dict(color='#D32F2F', width=4)))
        fig_fore.add_trace(go.Scatter(x=years, y=supply_curve, name="Supply Pipeline", line=dict(color='#1976D2', width=4)))
        fig_fore.update_layout(template="plotly_white")
        st.plotly_chart(fig_fore, use_container_width=True)
    with col_b:
        st.write("**Scenario Sensitivity: Demand Components**")
        comp_data = {"GSDP Momentum": best_hub['Growth'], "Automation Pull": automation/3, "Volatility Risk": -volatility/6}
        fig_bar = px.bar(x=list(comp_data.keys()), y=list(comp_data.values()), color=list(comp_data.keys()), color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_bar, use_container_width=True)

# --- TAB 2: GEOSPATIAL ---
with tabs[1]:
    st.subheader("📍 National Industrial Intensity Mapping")
    
    c_map, c_list = st.columns([2, 1])
    with c_map:
        fig_map = px.scatter_geo(geo_df, lat='Lat', lon='Lon', size='Dynamic_Momentum', color='Dynamic_Momentum', hover_name='State', scope='asia', center={'lat': 21.0, 'lon': 78.0}, color_continuous_scale='Viridis')
        fig_map.update_geos(lataxis_range=[5, 38], lonaxis_range=[65, 100])
        st.plotly_chart(fig_map, use_container_width=True)
    with c_list:
        st.write(f"### AI Research Strategy: {target_firm}")
        st.success(f"**Optimal Expansion Hub:** {best_hub['State']}")
        st.info(f"The domain of **{manual_domain}** shows peak concentration in **{best_hub['State']}**. Target investment here to mitigate predicted deficits.")

# --- TAB 3: SKILL RADAR ---
with tabs[2]:
    st.subheader("🧬 Neural Skill-Bridge Assessment")
    
    s_col1, s_col2 = st.columns([1.2, 1])
    with s_col1:
        resume_text = st.text_area("Live Resume / Profile Input", "Data Science, Python, Management")
        tokens = [s.strip().lower() for s in resume_text.split(',')]
        user_scores = [max([difflib.SequenceMatcher(None, target.lower(), token).ratio() for token in tokens]) * 100 if tokens else 0 for target in future_competencies]
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=user_scores, theta=future_competencies, fill='toself', name='User Profile', line_color='#FBC02D'))
        fig_radar.add_trace(go.Scatterpolar(r=[100]*6, theta=future_competencies, mode='lines', name='Industry Target', line=dict(color='#5D4037', dash='dot')))
        st.plotly_chart(fig_radar, use_container_width=True)
    with s_col2:
        st.write("**Competency Gap Decomposition**")
        gap_data = pd.DataFrame({"Skill": future_competencies, "Gap": [100 - s for s in user_scores]})
        st.plotly_chart(px.bar(gap_data, x='Gap', y='Skill', orientation='h', color='Gap', color_continuous_scale='Reds'), use_container_width=True)
        st.metric("Total Match Index", f"{np.mean(user_scores):.1f}%")

# --- TAB 4: POLICY SANDBOX ---
with tabs[3]:
    st.subheader("🛡️ Macro-Economic Resilience & Policy Simulation")
    
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        st.write("**GDP Opportunity Cost Projection (₹ Cr)**")
        loss_val = (demand_curve - supply_curve) * 1.5
        st.plotly_chart(px.line(x=years, y=loss_val, line_shape='spline', color_discrete_sequence=['#D32F2F']), use_container_width=True)
    with p_col2:
        st.write("**Policy Intervention Efficacy (Counter-Factual)**")
        no_pol_supply = 480 * (1 + (best_hub['Growth']/100) + (investment/200))**t
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Scatter(x=years, y=supply_curve, name="With Intervention", line=dict(color='#43A047', dash='dash')))
        fig_comp.add_trace(go.Scatter(x=years, y=no_pol_supply, name="Baseline", line=dict(color='#757575')))
        st.plotly_chart(fig_comp, use_container_width=True)
    st.info(f"**Policy Summary:** An intervention strength of {policy_strength}% reduces the **{manual_domain}** gap by approx {int(no_pol_supply[-1] - supply_curve[-1]) * -1}k workers.")

# --- TAB 5: CLUSTER CORRELATION & SKILL DECAY ---
with tabs[4]:
    st.subheader("🔗 Cluster Synergy & Skill Decay Analysis")
    
    c_col1, c_col2 = st.columns(2)
    
    with c_col1:
        st.write("**Skill Value Decay Rate (Obsolescence Index)**")
        decay_years = np.arange(0, 11)
        # Exponential decay model based on automation velocity
        skill_relevance = 100 * np.exp(-(automation/200) * decay_years)
        fig_decay = px.line(x=decay_years, y=skill_relevance, labels={'x': 'Years from Now', 'y': 'Relevance %'})
        fig_decay.update_layout(template="plotly_white", yaxis_range=[0, 100])
        st.plotly_chart(fig_decay, use_container_width=True)
        st.caption(f"Note: Automation velocity of {automation}% significantly reduces skill half-life.")

    with c_col2:
        st.write("**Localized Competitive Benchmarking**")
        top_5 = geo_df.nlargest(5, 'Dynamic_Momentum')
        fig_bench = px.bar(top_5, x='State', y='Dynamic_Momentum', color='Dynamic_Momentum', color_continuous_scale='Viridis')
        fig_bench.update_layout(template="plotly_white", showlegend=False)
        st.plotly_chart(fig_bench, use_container_width=True)
    
    st.divider()
    st.write("### AI Cross-Sector Ripple Effect Summary")
    ripple_impact = gap_val * 0.15 # 15% leakage into collateral GDP
    st.warning(f"**Talent Leakage Risk:** Shortage in **{manual_domain}** projected to create a ₹{abs(ripple_impact):.1f} Cr deficit in collateral sectors (Logistics, Hardware) within **{best_hub['State']}**.")

# --- FOOTER ---
st.divider()
st.caption(f"© 2026 Skill Intelligence Analytics | Researcher: JACOB TOM | Simulation: Advanced Stochastic Modeling")