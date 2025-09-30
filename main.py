import streamlit as st

st.set_page_config(
    page_title="Thyroid Detection",
    page_icon="🏥",
    layout="wide",
)

import src.ui_theme as ui_theme
import src.ui_inputs as ui_inputs
import src.prediction as prediction
import src.analytics as analytics
import src.session_manager as session_manager

from src.ui_theme import render_theme_toggle
session_manager.init_session()

# --- Theme ---
render_theme_toggle()
st.title("Thyroid Cancer Recurrence Predictor")

# --- Tabs ---
tab1, tab2 = st.tabs(["Prediction", "Analytics"])

with tab1:
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    st.subheader("Input Thyroid Form")
    session_manager.render_demo_controls()

    # --- Input form container ---
    st.markdown('<div class="themed-box">', unsafe_allow_html=True)
    inputs = ui_inputs.render_input_form()
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Prediction result container ---
    st.markdown('<div class="themed-box">', unsafe_allow_html=True)
    prediction.run_prediction(inputs)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    analytics.show_analytics()
    st.markdown('</div>', unsafe_allow_html=True)