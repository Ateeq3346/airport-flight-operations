import streamlit as st


st.set_page_config(
    page_title="Airport Flight Operations",
    page_icon="✈️",
    layout="wide",
)


st.title("✈️ Airport Flight Operations")
st.caption("Airport Operations & Decision Support System")

st.markdown(
    """
    Welcome to the Airport Flight Operations dashboard.

    Use the sidebar to navigate between:
    - Dashboard
    - Flight Operations
    - Passengers & Bookings
    - Operational Intelligence
    - Analytics Reports
    """
)