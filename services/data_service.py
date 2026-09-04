import mysql.connector
import pandas as pd

from config.settings import DATABASE_CONFIG


def get_connection():
    """Open a fresh MySQL connection for each request."""
    return mysql.connector.connect(**DATABASE_CONFIG)


def run_query(query, params=None):
    """Execute a read-only SQL query and return a DataFrame."""
    connection = get_connection()

    try:
        return pd.read_sql(query, connection, params=params)
    finally:
        connection.close()


# ============================================================
# FLIGHT OPERATIONS
# ============================================================

def get_flight_data():
    """
    Live flight dataset from MySQL.

    Passenger count is calculated from bookings because
    flights.passenger_count does not exist.
    """

    query = """
        SELECT
            f.flight_id AS Flight_ID,
            f.flight_number AS Flight,
            a.airline_name AS Airline,

            ao.airport_code AS Origin,
            ad.airport_code AS Destination,

            f.status AS Status,

            COUNT(b.booking_id) AS Passengers,

            COALESCE(f.delay_minutes, 0) AS Delay_Minutes,

            g.gate_code AS Gate,

            f.scheduled_departure AS Scheduled_Departure,
            f.scheduled_arrival AS Scheduled_Arrival,
            f.actual_departure AS Actual_Departure,
            f.actual_arrival AS Actual_Arrival

        FROM flights f

        JOIN airlines a
            ON f.airline_id = a.airline_id

        JOIN airports ao
            ON f.origin_airport_id = ao.airport_id

        JOIN airports ad
            ON f.destination_airport_id = ad.airport_id

        LEFT JOIN gates g
            ON f.gate_id = g.gate_id

        LEFT JOIN bookings b
            ON f.flight_id = b.flight_id

        GROUP BY
            f.flight_id,
            f.flight_number,
            a.airline_name,
            ao.airport_code,
            ad.airport_code,
            f.status,
            f.delay_minutes,
            g.gate_code,
            f.scheduled_departure,
            f.scheduled_arrival,
            f.actual_departure,
            f.actual_arrival

        ORDER BY f.flight_id
    """

    return run_query(query)


# ============================================================
# BOOKINGS
# ============================================================

def get_booking_data():
    """Live booking and passenger aggregation."""

    query = """
        SELECT
            a.airline_name AS Airline,

            COUNT(b.booking_id) AS Bookings,

            COUNT(DISTINCT b.passenger_id) AS Passengers

        FROM bookings b

        JOIN flights f
            ON b.flight_id = f.flight_id

        JOIN airlines a
            ON f.airline_id = a.airline_id

        GROUP BY
            a.airline_id,
            a.airline_name

        ORDER BY Bookings DESC
    """

    return run_query(query)


# ============================================================
# DASHBOARD SUMMARY
# ============================================================

def get_dashboard_summary():
    """
    Dashboard KPI summary.

    Important:
    Avoid aliases such as Delayed and Cancelled because
    they can cause SQL parsing problems depending on MySQL
    version/configuration.
    """

    query = """
        SELECT

            (
                SELECT COUNT(*)
                FROM flights
            ) AS Total_Flights,

            (
                SELECT COUNT(*)
                FROM flights
                WHERE status = 'On Time'
            ) AS On_Time_Flights,

            (
                SELECT COUNT(*)
                FROM flights
                WHERE status = 'Delayed'
            ) AS Delayed_Flights,

            (
                SELECT COUNT(*)
                FROM flights
                WHERE status = 'Cancelled'
            ) AS Cancelled_Flights,

            (
                SELECT COUNT(*)
                FROM passengers
            ) AS Total_Passengers
    """

    return run_query(query)


# ============================================================
# FLIGHT STATUS DISTRIBUTION
# ============================================================

def get_flight_status_distribution():

    query = """
        SELECT
            status AS Flight_Status,
            COUNT(*) AS Flight_Count

        FROM flights

        GROUP BY status

        ORDER BY Flight_Count DESC
    """

    return run_query(query)


# ============================================================
# FLIGHTS BY AIRLINE
# ============================================================

def get_airline_flight_counts():

    query = """
        SELECT
            a.airline_name AS Airline,
            COUNT(f.flight_id) AS Flight_Count

        FROM flights f

        JOIN airlines a
            ON f.airline_id = a.airline_id

        GROUP BY
            a.airline_id,
            a.airline_name

        ORDER BY Flight_Count DESC
    """

    return run_query(query)


# ============================================================
# DATABASE COUNTS
# ============================================================

def get_database_counts():
    """Return live row counts for all core tables."""

    query = """
        SELECT

            (SELECT COUNT(*)
             FROM airlines) AS Airlines,

            (SELECT COUNT(*)
             FROM aircraft_types) AS Aircraft_Types,

            (SELECT COUNT(*)
             FROM aircraft) AS Aircraft,

            (SELECT COUNT(*)
             FROM airports) AS Airports,

            (SELECT COUNT(*)
             FROM terminals) AS Terminals,

            (SELECT COUNT(*)
             FROM gates) AS Gates,

            (SELECT COUNT(*)
             FROM pilots) AS Pilots,

            (SELECT COUNT(*)
             FROM flights) AS Flights,

            (SELECT COUNT(*)
             FROM passengers) AS Passengers,

            (SELECT COUNT(*)
             FROM bookings) AS Bookings,

            (SELECT COUNT(*)
             FROM flight_status_history) AS Flight_Status_History
    """

    return run_query(query)


# ============================================================
# AIRLINE PERFORMANCE
# ============================================================

def get_airline_performance():
    """
    Airline operational performance.

    Important:
    Flights are counted with COUNT(DISTINCT f.flight_id)
    so multiple bookings do not inflate flight totals.
    """

    query = """
        SELECT

            a.airline_name AS Airline,

            COUNT(DISTINCT f.flight_id) AS Flights,

            COUNT(
                DISTINCT CASE
                    WHEN f.status = 'On Time'
                    THEN f.flight_id
                END
            ) AS On_Time_Flights,

            COUNT(
                DISTINCT CASE
                    WHEN f.status = 'Delayed'
                    THEN f.flight_id
                END
            ) AS Delayed_Flights,

            COUNT(
                DISTINCT CASE
                    WHEN f.status = 'Cancelled'
                    THEN f.flight_id
                END
            ) AS Cancelled_Flights,

            COALESCE(
                ROUND(
                    AVG(f.delay_minutes),
                    1
                ),
                0
            ) AS Average_Delay,

            COUNT(b.booking_id) AS Bookings

        FROM airlines a

        LEFT JOIN flights f
            ON a.airline_id = f.airline_id

        LEFT JOIN bookings b
            ON f.flight_id = b.flight_id

        GROUP BY
            a.airline_id,
            a.airline_name

        ORDER BY
            Flights DESC,
            Airline
    """

    return run_query(query)


# ============================================================
# ROUTE PERFORMANCE
# ============================================================

def get_route_performance():
    """Live route-level flight and booking analysis."""

    query = """
        SELECT

            ao.airport_code AS Origin,

            ad.airport_code AS Destination,

            COUNT(DISTINCT f.flight_id) AS Flights,

            COUNT(b.booking_id) AS Bookings,

            COALESCE(
                ROUND(
                    AVG(f.delay_minutes),
                    1
                ),
                0
            ) AS Average_Delay

        FROM flights f

        JOIN airports ao
            ON f.origin_airport_id = ao.airport_id

        JOIN airports ad
            ON f.destination_airport_id = ad.airport_id

        LEFT JOIN bookings b
            ON f.flight_id = b.flight_id

        GROUP BY
            ao.airport_code,
            ad.airport_code

        ORDER BY
            Flights DESC,
            Bookings DESC
    """

    return run_query(query)


# ============================================================
# DAILY FLIGHT SUMMARY
# ============================================================

def get_daily_flight_summary():
    """Daily operational flight summary."""

    query = """
        SELECT

            DATE(scheduled_departure) AS Flight_Date,

            COUNT(*) AS Flights,

            SUM(
                CASE
                    WHEN status = 'On Time'
                    THEN 1
                    ELSE 0
                END
            ) AS On_Time_Flights,

            SUM(
                CASE
                    WHEN status = 'Delayed'
                    THEN 1
                    ELSE 0
                END
            ) AS Delayed_Flights,

            SUM(
                CASE
                    WHEN status = 'Cancelled'
                    THEN 1
                    ELSE 0
                END
            ) AS Cancelled_Flights,

            COALESCE(
                ROUND(
                    AVG(delay_minutes),
                    1
                ),
                0
            ) AS Average_Delay

        FROM flights

        GROUP BY
            DATE(scheduled_departure)

        ORDER BY
            Flight_Date
    """

    return run_query(query)

def get_recent_arrivals(limit=10):
    """Return the most recent arrival flights."""

    query = """
        SELECT
            f.flight_number AS Flight,
            a.airline_name AS Airline,
            ao.airport_code AS Origin,
            ad.airport_code AS Destination,
            f.status AS Status,
            g.gate_code AS Gate,
            f.scheduled_arrival AS Scheduled_Arrival,
            f.actual_arrival AS Actual_Arrival,
            COALESCE(f.delay_minutes, 0) AS Delay_Minutes

        FROM flights f

        JOIN airlines a
            ON f.airline_id = a.airline_id

        JOIN airports ao
            ON f.origin_airport_id = ao.airport_id

        JOIN airports ad
            ON f.destination_airport_id = ad.airport_id

        LEFT JOIN gates g
            ON f.gate_id = g.gate_id

        WHERE f.scheduled_arrival IS NOT NULL

        ORDER BY
            COALESCE(
                f.actual_arrival,
                f.scheduled_arrival
            ) DESC

        LIMIT %s
    """

    return run_query(query, (limit,))


def get_recent_departures(limit=10):
    """Return the most recent departure flights."""

    query = """
        SELECT
            f.flight_number AS Flight,
            a.airline_name AS Airline,
            ao.airport_code AS Origin,
            ad.airport_code AS Destination,
            f.status AS Status,
            g.gate_code AS Gate,
            f.scheduled_departure AS Scheduled_Departure,
            f.actual_departure AS Actual_Departure,
            COALESCE(f.delay_minutes, 0) AS Delay_Minutes

        FROM flights f

        JOIN airlines a
            ON f.airline_id = a.airline_id

        JOIN airports ao
            ON f.origin_airport_id = ao.airport_id

        JOIN airports ad
            ON f.destination_airport_id = ad.airport_id

        LEFT JOIN gates g
            ON f.gate_id = g.gate_id

        WHERE f.scheduled_departure IS NOT NULL

        ORDER BY
            COALESCE(
                f.actual_departure,
                f.scheduled_departure
            ) DESC

        LIMIT %s
    """

    return run_query(query, (limit,))