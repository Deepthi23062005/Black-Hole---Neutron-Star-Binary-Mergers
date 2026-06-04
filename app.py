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

# --- CUSTOM CSS FOR BETTER UI ---
# Consolidated to a single-line string to ensure compatibility with Python 3.13+ parsing rules
custom_css = "<style>.main-header {font-size: 36px; font-weight: bold; color: #1E3A8A; text-align: center; margin-bottom: 10px;} .sub-header {font-size: 18px; color: #4B5563; text-align: center; margin-bottom: 30px;} .metric-card {background-color: #F3F4F6; padding: 15px; border-radius: 10px; border-left: 5px solid #3B82F6;}</style>"
st.markdown(custom_css, unsafe_with_html=True)

# --- HEADER SECTION ---
st.markdown("<div class='main-header'>🌌 Black Hole - Neutron Star Binary Mergers</div>", unsafe_with_html=True)
st.markdown("<div class='sub-header'>Interactive Exploration of Gravitational Radiation Waveforms & Coalescence Physics</div>", unsafe_with_html=True)
st.write("---")

# --- SIMULATED DATA GENERATION ---
# This matches William Henry Lee's Newtonian physics waveform trends
@st.cache_data
def load_simulated_waveform_data():
    t = np.linspace(-0.1, 0.02, 1000) # Time leading up to and slightly past merger
    
    # Frequency increases as orbit shrinks (chirp mass effect)
    frequency = 50 / (0.01 - t + 1e-5)**0.25 
    
    # Waveform strain h(t)
    amplitude = 1e-21 * (0.01 - t + 1e-5)**-0.25
    amplitude[t > 0.01] = 0 # Post-merger ringdown/cutoff
    strain = amplitude * np.sin(2 * np.pi * frequency * t)
    
    # Orbital radius shrinking over time
    radius = np.maximum(15, 100 * (0.01 - t + 1e-5)**0.25)
    
    df = pd.DataFrame({
        "Time (s)": t,
        "Strain": strain,
        "Orbital Radius (km)": radius,
        "Frequency (Hz)": np.clip(frequency, 0, 2000)
    })
    return df

# Load the base waveform profile
df = load_simulated_waveform_data()

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.header("🔧 Simulation Parameters")
st.sidebar.markdown("Adjust binary system variables to run a custom fusion prediction analysis.")

# User inputs (Placed BEFORE the metric charts call them)
black_hole_mass = st.sidebar.slider("Black Hole Mass ($M_{\odot}$)", min_value=3.0, max_value=20.0, value=7.0, step=0.5)
neutron_star_mass = st.sidebar.slider("Neutron Star Mass ($M_{\odot}$)", min_value=1.1, max_value=2.5, value=1.4, step=0.1)
initial_distance = st.sidebar.number_input("Initial Orbital Separation (km)", min_value=150, max_value=500, value=300)

# Submit Button
submit_button = st.sidebar.button("💥 Run Merger Analysis", use_container_width=True)

# --- DEFAULT VISUALIZATION & KPI METRICS ---
col1, col2, col3 = st.columns(3)
with col1:
    q_ratio = black_hole_mass / neutron_star_mass
    st.markdown(f"<div class='metric-card'><b>Mass Ratio ($q$)</b>
