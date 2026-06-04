import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="BH-NS Binary Merger Dashboard",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- HEADER SECTION ---
st.title("🌌 Black Hole - Neutron Star Binary Mergers")
st.caption("Interactive Exploration of Gravitational Radiation Waveforms & Coalescence Physics")
st.write("---")

# --- SIMULATED DATA GENERATION ---
@st.cache_data
def load_simulated_waveform_data():
    t = np.linspace(-0.1, 0.02, 1000) 
    frequency = 50 / (0.01 - t + 1e-5)**0.25 
    amplitude = 1e-21 * (0.01 - t + 1e-5)**-0.25
    amplitude[t > 0.01] = 0 
    strain = amplitude * np.sin(2 * np.pi * frequency * t)
    radius = np.maximum(15, 100 * (0.01 - t + 1e-5)**0.25)
    
    df = pd.DataFrame({
        "Time (s)": t,
        "Strain": strain,
        "Orbital Radius (km)": radius,
        "Frequency (Hz)": np.clip(frequency, 0, 2000)
    })
    return df

df = load_simulated_waveform_data()

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.header("🔧 Simulation Parameters")
st.sidebar.markdown("Adjust binary system variables to run a custom fusion prediction analysis.")

black_hole_mass = st.sidebar.slider("Black Hole Mass (M☉)", min_value=3.0, max_value=20.0, value=7.0, step=0.5)
neutron_star_mass = st.sidebar.slider("Neutron Star Mass (M☉)", min_value=1.1, max_value=2.5, value=1.4, step=0.1)
initial_distance = st.sidebar.number_input("Initial Orbital Separation (km)", min_value=150, max_value=500, value=300)

submit_button = st.sidebar.button("💥 Run Merger Analysis", use_container_width=True)

# --- DEFAULT VISUALIZATION & KPI METRICS ---
# Using native st.metric cards to bypass Python 3.14 HTML wrapper conflicts
col1, col2, col3 = st.columns(3)
with col1:
    q_ratio = black_hole_mass / neutron_star_mass
    st.metric(label="Mass Ratio (q)", value=f"{q_ratio:.2f}")
with col2:
    chirp_mass = ((black_hole_mass * neutron_star_mass)**(3/5)) / ((black_hole_mass + neutron_star_mass)**(1/5))
    st.metric(label="Expected Chirp Mass", value=f"{chirp_mass:.2f} M☉")
with col3:
    st.metric(label="Physics Paradigm", value="Newtonian Coalescence")

# --- VISUALIZATION PLOTS ---
st.write("## 📈 Base Waveform Visualizations")

tab1, tab2 = st.tabs(["🔊 Gravitational Wave Strain", "🪐 Orbital Decay Profile"])

with tab1:
    fig_strain = px.line(df, x="Time (s)", y="Strain", title="Gravitational Radiation Waveform h(t)")
    fig_strain.update_layout(template="plotly_dark", xaxis_title="Time to Merger (seconds)", yaxis_title="Strain Amplitude")
    st.plotly_chart(fig_strain, use_container_width=True)

with tab2:
    fig_radius = go.Figure()
    fig_radius.add_trace(go.Scatter(x=df["Time (s)"], y=df["Orbital Radius (km)"], name="Radius", line=dict(color="orange")))
    fig_radius.update_layout(title="Orbital Radius Decay", template="plotly_dark", xaxis_title="Time (s)", yaxis_title="Separation Distance (km)")
    st.plotly_chart(fig_radius, use_container_width=True)

# --- ACTIONS TRIGGERED ON SUBMIT ---
if submit_button:
    st.write("---")
    st.write("## 🧬 Custom Merger Simulation Insights")
    
    with st.spinner("Processing event horizons and calculating gravitational flux..."):
        time.sleep(1.5) 
    
    total_mass = black_hole_mass + neutron_star_mass
    final_schwarzschild_radius = 2.95 * total_mass 
    time_to_coalescence = (initial_distance**4) / (total_mass * 1e4)
    
    st.success("Analysis Complete! Here are the localized physics insights based on your inputs:")
    
    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        st.subheader("📊 Computed Fusion Events")
        insight_data = {
            "Parameter": ["Total System Mass", "Calculated Event Horizon Radius", "Estimated Collapse Duration"],
            "Value": [f"{total_mass:.2f} M☉", f"{final_schwarzschild_radius:.2f} km", f"{time_to_coalescence:.4f} seconds"]
        }
        st.table(pd.DataFrame(insight_data))
        
    with res_col2:
        st.subheader("💡 Physical Phenomenon Insight")
        if (black_hole_mass / neutron_star_mass) > 5.0:
            st.warning("⚠️ **High Mass Ratio:** The Neutron Star is highly likely to be swallowed whole by the Black Hole's event horizon without producing a significant electromagnetic tidal disruption remnant.")
        else:
            st.info("✨ **Tidal Disruption Likely:** The tidal forces will likely rip the neutron star apart before crossing the event horizon, producing a vibrant accretion disk and a short Gamma-Ray Burst (sGRB).")

    fig_freq = px.area(df, x="Time (s)", y="Frequency (Hz)", title="Dynamic Frequency Shift (Chirp Phenomenon)", color_discrete_sequence=['#EC4899'])
    fig_freq.update_layout(template="plotly_dark")
    st.plotly_chart(fig_freq, use_container_width=True)
    
else:
    st.info("👈 Modify parameters on the left sidebar panel and press **Run Merger Analysis** to view custom system insights.")
