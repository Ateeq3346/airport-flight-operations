import streamlit as st
import plotly.express as px

from services.data_service import get_booking_data

st.set_page_config(
    page_title="Passengers & Bookings",
    page_icon="👥",
    layout="wide",
)

st.title("👥 Passengers & Bookings")
st.caption("Live booking and passenger analysis from MySQL")

if st.button("🔄 Refresh Data"):
    st.rerun()

df = get_booking_data()

total_bookings = int(df["Bookings"].sum())
total_passengers = int(df["Passengers"].sum())

col1, col2, col3 = st.columns(3)
col1.metric("Total Bookings", f"{total_bookings:,}")
col2.metric("Unique Passenger Bookers", f"{total_passengers:,}")
col3.metric(
    "Average Unique Passengers / Airline",
    f"{df['Passengers'].mean():,.0f}",
)

st.divider()

left, right = st.columns(2)

with left:
    fig = px.bar(
        df,
        x="Airline",
        y="Bookings",
        title="Bookings by Airline",
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    fig = px.bar(
        df,
        x="Airline",
        y="Passengers",
        title="Unique Passengers by Airline",
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Live Booking Overview")
st.dataframe(df, use_container_width=True, hide_index=True)
