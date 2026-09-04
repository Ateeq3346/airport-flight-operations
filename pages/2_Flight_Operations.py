import streamlit as st
import plotly.express as px

from services.data_service import get_flight_data

st.set_page_config(
    page_title="Flight Operations",
    page_icon="✈️",
    layout="wide",
)

st.title("✈️ Flight Operations")
st.caption("Live schedules, status, delays, gates and booking-derived passenger counts")

if st.button("🔄 Refresh Data"):
    st.rerun()

df = get_flight_data()

col1, col2, col3 = st.columns(3)

with col1:
    airlines = ["All"] + sorted(df["Airline"].dropna().unique().tolist())
    selected_airline = st.selectbox("Airline", airlines)

with col2:
    statuses = ["All"] + sorted(df["Status"].dropna().unique().tolist())
    selected_status = st.selectbox("Flight Status", statuses)

with col3:
    gates = ["All"] + sorted(df["Gate"].dropna().unique().tolist())
    selected_gate = st.selectbox("Gate", gates)

filtered_df = df.copy()

if selected_airline != "All":
    filtered_df = filtered_df[filtered_df["Airline"] == selected_airline]

if selected_status != "All":
    filtered_df = filtered_df[filtered_df["Status"] == selected_status]

if selected_gate != "All":
    filtered_df = filtered_df[filtered_df["Gate"] == selected_gate]

st.divider()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Flights", f"{len(filtered_df):,}")
col2.metric("Bookings / Passengers", f"{int(filtered_df['Passengers'].sum()):,}")
col3.metric(
    "Delayed Flights",
    f"{int((filtered_df['Status'] == 'Delayed').sum()):,}",
)
avg_delay = filtered_df["Delay_Minutes"].mean()
col4.metric("Average Delay", f"{0 if filtered_df.empty else avg_delay:.1f} min")

st.divider()

left, right = st.columns(2)

with left:
    delay_data = (
        filtered_df.groupby("Airline", as_index=False)["Delay_Minutes"]
        .mean()
    )
    fig = px.bar(
        delay_data,
        x="Airline",
        y="Delay_Minutes",
        title="Average Delay by Airline",
        labels={"Delay_Minutes": "Average Delay (minutes)"},
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    gate_data = (
        filtered_df.groupby("Gate")
        .size()
        .reset_index(name="Flights")
    )
    fig = px.bar(
        gate_data,
        x="Gate",
        y="Flights",
        title="Flights by Gate",
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Live Flight Schedule")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)
