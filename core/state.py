import streamlit as st


def init_session_state():
    """Initialize all session state variables with their defaults."""
    if "intrusion_active" not in st.session_state:
        st.session_state.intrusion_active = False
    if "attack_phase" not in st.session_state:
        st.session_state.attack_phase = 0
    if "terminal_lines" not in st.session_state:
        st.session_state.terminal_lines = []
    if "nis2_generated" not in st.session_state:
        st.session_state.nis2_generated = False
    if "attack_timestamp" not in st.session_state:
        st.session_state.attack_timestamp = None
    if "animating" not in st.session_state:
        st.session_state.animating = False
    if "selected_scenario" not in st.session_state:
        st.session_state.selected_scenario = 0
    if "log_stream_events" not in st.session_state:
        st.session_state.log_stream_events = []
