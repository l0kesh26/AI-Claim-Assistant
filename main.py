import streamlit as st

from streamlit_app import login_page, policy_page, dashboard_page, claim_page

# SESSION
if "page" not in st.session_state:
    st.session_state.page = "login"

# ROUTER
if st.session_state.page == "login":
    login_page()

elif st.session_state.page == "policy":
    policy_page()

elif st.session_state.page == "dashboard":
    dashboard_page()

elif st.session_state.page == "claim":
    claim_page()