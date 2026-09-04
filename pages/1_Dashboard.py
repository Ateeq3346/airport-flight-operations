import streamlit as st
import plotly.express as px

from services.data_service import (
    get_dashboard_summary,
    get_flight_status_distribution,
    get_airline_flight_counts,
    get_recent_arrivals,
    get_recent_departures,
)


st.set_page_config(
    page_title="Airport Operations Dashboard",
    page_icon="📊",
    layout="wide",
)


st.title("📊 Airport Operations Dashboard")
st.caption("Live operational overview from MySQL")


if st.button("🔄 Refresh Data"):
    st.rerun()


try:

    # ========================================================
    # LOAD DATA
    # ========================================================

    summary = get_dashboard_summary().iloc[0]

    status_df = get_flight_status_distribution()

    airline_df = get_airline_flight_counts()

    arrivals_df = get_recent_arrivals(10)

    departures_df = get_recent_departures(10)


    # ========================================================
    # KPI CARDS
    # ========================================================

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Total Flights",
            int(summary["Total_Flights"])
        )

    with col2:
        st.metric(
            "On Time",
            int(summary["On_Time_Flights"])
        )

    with col3:
        st.metric(
            "Delayed",
            int(summary["Delayed_Flights"])
        )

    with col4:
        st.metric(
            "Cancelled",
            int(summary["Cancelled_Flights"])
        )

    with col5:
        st.metric(
            "Passengers",
            f"{int(summary['Total_Passengers']):,}"
        )


    st.divider()


    # ========================================================
    # CHARTS
    # ========================================================

    left, right = st.columns(2)


    with left:

        st.subheader("Flight Status Distribution")

        if not status_df.empty:

            fig = px.pie(
                status_df,
                names="Flight_Status",
                values="Flight_Count",
                hole=0.35,
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info("No flight status data available.")


    with right:

        st.subheader("Flights by Airline")

        if not airline_df.empty:

            fig = px.bar(
                airline_df,
                x="Airline",
                y="Flight_Count",
                labels={
                    "Flight_Count": "Flights"
                },
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info("No airline data available.")


    st.divider()


    # ========================================================
    # RECENT ARRIVALS & DEPARTURES
    # ========================================================

    st.header("✈️ Recent Flight Activity")
    st.caption(
        "Latest scheduled and completed arrivals and departures"
    )


    arrivals_col, departures_col = st.columns(2)


    # ========================================================
    # RECENT ARRIVALS
    # ========================================================

    with arrivals_col:

        st.subheader("🛬 Recent Arrivals")

        if not arrivals_df.empty:

            arrivals_display = arrivals_df.copy()

            arrivals_display = arrivals_display.rename(
                columns={
                    "Flight": "Flight",
                    "Airline": "Airline",
                    "Origin": "From",
                    "Destination": "To",
                    "Status": "Status",
                    "Gate": "Gate",
                    "Scheduled_Arrival": "Scheduled",
                    "Actual_Arrival": "Actual",
                    "Delay_Minutes": "Delay (min)",
                }
            )

            st.dataframe(
                arrivals_display[
                    [
                        "Flight",
                        "Airline",
                        "From",
                        "To",
                        "Status",
                        "Gate",
                        "Scheduled",
                        "Actual",
                        "Delay (min)",
                    ]
                ],
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info("No recent arrival flights available.")


    # ========================================================
    # RECENT DEPARTURES
    # ========================================================

    with departures_col:

        st.subheader("🛫 Recent Departures")

        if not departures_df.empty:

            departures_display = departures_df.copy()

            departures_display = departures_display.rename(
                columns={
                    "Flight": "Flight",
                    "Airline": "Airline",
                    "Origin": "From",
                    "Destination": "To",
                    "Status": "Status",
                    "Gate": "Gate",
                    "Scheduled_Departure": "Scheduled",
                    "Actual_Departure": "Actual",
                    "Delay_Minutes": "Delay (min)",
                }
            )

            st.dataframe(
                departures_display[
                    [
                        "Flight",
                        "Airline",
                        "From",
                        "To",
                        "Status",
                        "Gate",
                        "Scheduled",
                        "Actual",
                        "Delay (min)",
                    ]
                ],
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info("No recent departure flights available.")


except Exception as e:

    st.error(
        "Dashboard could not load data from MySQL."
    )

    st.exception(e)