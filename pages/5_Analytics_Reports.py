import streamlit as st
import plotly.express as px

from services.data_service import (
    get_airline_performance,
    get_route_performance,
    get_daily_flight_summary,
)


st.set_page_config(
    page_title="Analytics & Reports",
    page_icon="📈",
    layout="wide",
)


st.title("📈 Analytics & Reports")
st.caption("Live performance analysis from MySQL")


if st.button("🔄 Refresh Data"):
    st.rerun()


try:

    airline_df = get_airline_performance()

    route_df = get_route_performance()

    daily_df = get_daily_flight_summary()


    # ========================================================
    # AIRLINE PERFORMANCE
    # ========================================================

    st.subheader("Airline Performance")


    if not airline_df.empty:

        left, right = st.columns(2)


        with left:

            fig = px.bar(
                airline_df,
                x="Airline",
                y="Flights",
                title="Flights by Airline",
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


        with right:

            fig = px.bar(
                airline_df,
                x="Airline",
                y="Average_Delay",
                title="Average Delay by Airline",
                labels={
                    "Average_Delay": "Average Delay (minutes)"
                },
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


        st.dataframe(
            airline_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info("No airline performance data available.")


    # ========================================================
    # ROUTE PERFORMANCE
    # ========================================================

    st.subheader("Route Performance")


    if not route_df.empty:

        st.dataframe(
            route_df,
            use_container_width=True,
            hide_index=True,
        )


        fig = px.bar(
            route_df.head(10),
            x="Origin",
            y="Flights",
            color="Destination",
            title="Top Routes by Flight Count",
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info("No route performance data available.")


    # ========================================================
    # DAILY FLIGHT SUMMARY
    # ========================================================

    st.subheader("Daily Flight Summary")


    if not daily_df.empty:

        fig = px.line(
            daily_df,
            x="Flight_Date",
            y="Flights",
            markers=True,
            title="Flights by Date",
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        st.dataframe(
            daily_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info("No daily flight data available.")


except Exception as e:

    st.error(
        "Analytics Reports could not load data from MySQL."
    )

    st.exception(e)