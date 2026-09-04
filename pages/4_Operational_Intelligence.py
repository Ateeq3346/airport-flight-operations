import streamlit as st
import plotly.express as px

from services.data_service import get_flight_data

st.set_page_config(
    page_title="Operational Intelligence",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 Operational Intelligence")
st.caption("Live operational risk and performance indicators")

if st.button("🔄 Refresh Data"):
    st.rerun()

df = get_flight_data()

delayed = df[df["Status"] == "Delayed"].copy()
cancelled = df[df["Status"] == "Cancelled"].copy()

avg_delay = df["Delay_Minutes"].mean()
delay_rate = len(delayed) / len(df) * 100 if len(df) else 0
cancel_rate = len(cancelled) / len(df) * 100 if len(df) else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Delay Rate", f"{delay_rate:.1f}%")
col2.metric("Cancellation Rate", f"{cancel_rate:.1f}%")
col3.metric("Average Delay", f"{avg_delay:.1f} min")
col4.metric("High Risk Flights", f"{len(delayed):,}")

st.divider()

left, right = st.columns(2)

with left:
    fig = px.bar(
        delayed,
        x="Flight",
        y="Delay_Minutes",
        title="Delayed Flights",
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    airline_delay = (
        df.groupby("Airline", as_index=False)["Delay_Minutes"]
        .mean()
    )
    fig = px.bar(
        airline_delay,
        x="Airline",
        y="Delay_Minutes",
        title="Average Delay by Airline",
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Operational Risk Assessment")

risk_df = df.copy()
risk_df["Risk Level"] = risk_df["Delay_Minutes"].apply(
    lambda x: "High" if x >= 30 else "Medium" if x > 0 else "Low"
)

st.dataframe(
    risk_df[
        [
            "Flight",
            "Airline",
            "Status",
            "Delay_Minutes",
            "Gate",
            "Risk Level",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)
