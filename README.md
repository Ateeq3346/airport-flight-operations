# ✈️ Airport Flight Operations & Decision Support System

A MySQL-powered **Airport Flight Operations & Decision Support System** built with **Python, Streamlit, Pandas, Plotly, and MySQL**.

The project provides a web-based operational dashboard for monitoring flights, passengers, bookings, delays, airlines, routes, and operational performance.

---

## 1. Project Overview

The system converts airport operational data into a practical **Airport Operations & Decision Support System**.

The final architecture has two major responsibilities:

1. **MySQL / SQL** handles relational data, joins, filtering, aggregation, and analytics.
2. **Python / Streamlit** provides the application interface, executes SQL queries, and presents results through dashboards, tables, and charts.

**MySQL is the single source of truth.** The application does not depend on hardcoded operational records.

---

## 2. Project Journey

### Phase 1 — Requirements

The original objective was to build an airport-focused SQL project that demonstrated more than table creation.

The final goal became:

> Build an Airport Flight Operations & Decision Support System that demonstrates relational database design, SQL querying, analytics, and a usable Streamlit application.

### Phase 2 — Database Design

The database was designed around the operational lifecycle of a flight.

Core entities include:

```text
Airlines
Aircraft Types
Aircraft
Airports
Terminals
Gates
Pilots
Flights
Passengers
Bookings
Flight Status History
```

The `flights` table is one of the central operational entities. Flights reference airlines, aircraft, airports, gates, status, schedules, and delay information. Bookings connect passengers with flights.

This relational structure allows realistic SQL analysis without duplicating the same information across unrelated tables.

### Phase 3 — Application Integration

The application follows:

```text
Streamlit UI
    ↓
Python services
    ↓
Database/query layer
    ↓
MySQL
    ↓
SQL result
    ↓
Pandas
    ↓
Streamlit
```

This separation keeps UI code understandable and keeps database logic close to the data layer.

### Phase 4 — Live Database Integration

The application was moved from prototype/hardcoded data toward a live database-driven design.

The final flow is:

```text
MySQL Workbench
       ↓
MySQL Server
       ↓
airport_operations database
       ↓
SQL queries
       ↓
Python services
       ↓
Streamlit
```

**Important:** Streamlit is not connected to MySQL Workbench itself. Workbench is a management/client tool. Both Workbench and the Streamlit application connect to the same MySQL Server.

---

## 3. Final Architecture

```text
                    USER
                      │
                      ▼
              ┌───────────────┐
              │   Streamlit   │
              │      UI       │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │    Python     │
              │ Application   │
              │ / Services    │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ MySQL Query   │
              │ / Connection  │
              │     Layer     │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │     MySQL     │
              │ airport_      │
              │ operations    │
              └───────────────┘
```

### Responsibility of each layer

| Layer | Responsibility |
|---|---|
| Streamlit | UI, navigation, tables, charts, filters |
| Python | Application logic and query execution |
| Pandas | DataFrame handling and presentation transformations |
| Plotly | Interactive charts |
| MySQL | Storage, relationships, joins, aggregation, analytics |
| Git/GitHub | Version control |

---

## 4. Repository Structure

```text
airport-flight-operations/
│
├── app.py
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── pages/
│   ├── 1_Dashboard.py
│   ├── 2_Flight_Operations.py
│   ├── 3_Passengers_Bookings.py
│   ├── 4_Operational_Intelligence.py
│   └── 5_Analytics_Reports.py
│
├── services/
│   ├── __init__.py
│   └── data_service.py
│
├── sql/
│   └── SQL analysis/query files
│
├── assets/
├── tests/
├── docs/
│
├── database/
│   └── Airlines data.sql
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### Database dump

The file:

```text
database/Airlines data.sql
```

is the exported MySQL database dump.

It is intended to allow another developer/team member to recreate the same database structure and data on their own computer.

---

## 5. Main Application

### `app.py`

`app.py` is the Streamlit entry point.

It configures:

- page title
- page icon
- wide layout
- application introduction
- navigation through the Streamlit pages

The pages in `pages/` provide the individual application screens.

---

# 6. Streamlit Pages

## Dashboard

File:

```text
pages/1_Dashboard.py
```

Purpose:

Provide an operational overview.

Main KPIs:

- Total Flights
- On-Time Flights
- Delayed Flights
- Cancelled Flights
- Total Passengers

Visualizations:

- Flight Status Distribution
- Flights by Airline

The dashboard also provides recent arrival and departure flight information in table form using the scheduled/actual timestamps available in the database.

The dashboard reads its values from MySQL, so changes made to the database are reflected when the application refreshes its data.

---

## Flight Operations

File:

```text
pages/2_Flight_Operations.py
```

Purpose:

Provide detailed flight-level operational information.

Typical fields include:

- Flight number
- Airline
- Origin
- Destination
- Scheduled departure
- Actual departure
- Scheduled arrival
- Actual arrival
- Status
- Delay
- Passenger count
- Gate

An important implementation decision was to derive passenger count from bookings rather than depend on a non-existent `flights.passenger_count` column.

---

## Passengers & Bookings

File:

```text
pages/3_Passengers_Bookings.py
```

Purpose:

Connect passenger information with bookings and flights.

Typical information includes:

- Passenger
- Booking reference
- Flight
- Seat
- Travel class
- Booking status
- Ticket price

---

## Operational Intelligence

File:

```text
pages/4_Operational_Intelligence.py
```

Purpose:

Turn operational data into decision-support information.

Potential analyses include:

- high-delay flights
- aircraft utilization
- load factor
- gate utilization
- operational alerts
- turnaround information

Business calculations should preferably be performed in SQL using the actual database schema.

---

## Analytics & Reports

File:

```text
pages/5_Analytics_Reports.py
```

Purpose:

Provide higher-level analytical reporting.

The analytics layer includes:

- Airline Performance
- Route Performance
- Daily Flight Summary
- Average Delay
- Booking/Passenger analysis
- Flight-volume analysis

Plotly is used for interactive visualizations.

---

# 7. Database Connection

The application uses:

```text
mysql-connector-python
```

Database configuration is read from environment variables.

Example:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=airport_operations
DB_USER=root
DB_PASSWORD=your_password
```

Credentials should **never** be hardcoded into application source files.

The intended project setup uses `.env` locally and `.env.example` as the safe template committed to Git.

---

# 8. How MySQL Workbench, MySQL, and Streamlit Are Connected

A common point of confusion is that the application is not connected to Workbench.

The actual architecture is:

```text
                    MySQL Server
                         │
                airport_operations
                    /           \
                   /             \
                  ▼               ▼
        MySQL Workbench       Streamlit App
        (management tool)          │
                                   ▼
                              Python
                                   │
                              mysql.connector
```

### MySQL Workbench

Used to:

- inspect tables
- run SQL manually
- insert/update data
- test queries
- export the database
- import the database

### MySQL Server

Actually stores:

- tables
- records
- relationships
- indexes
- database objects

### Streamlit

Connects directly to MySQL Server through Python.

Therefore:

> If a record is changed in MySQL Workbench, the Streamlit application will see the changed database data the next time its query is executed/refreshed.

---

# 9. Query and Service Layer

Reusable database functions are kept in:

```text
services/data_service.py
```

Examples include:

```text
get_flight_data()
get_booking_data()
get_dashboard_summary()
get_flight_status_distribution()
get_airline_flight_counts()
get_database_counts()
get_airline_performance()
get_route_performance()
get_daily_flight_summary()
```

The application flow is:

```text
Streamlit Page
      ↓
Service Function
      ↓
SQL Query
      ↓
MySQL
      ↓
Pandas DataFrame
      ↓
Streamlit
```

This avoids putting every database query directly inside the UI.

---

# 10. Important SQL Design Decision — Passenger Count

An early application version expected:

```sql
flights.passenger_count
```

The actual relational model stores passengers through bookings.

Therefore the final flight query derives passenger count with:

```sql
COUNT(b.booking_id)
```

and:

```sql
LEFT JOIN bookings b
    ON f.flight_id = b.flight_id
```

with the required `GROUP BY`.

This is preferable because it uses the actual relational model instead of maintaining duplicate passenger-count information.

---

# 11. Dashboard KPI Design

Operational values are retrieved from MySQL.

For example:

```sql
SELECT COUNT(*)
FROM flights;
```

provides the total number of flights.

A delayed-flight count can be calculated with:

```sql
SELECT COUNT(*)
FROM flights
WHERE status = 'Delayed';
```

The result is then displayed as a Streamlit metric.

The principle is:

```text
MySQL calculates
      ↓
Python retrieves
      ↓
Streamlit displays
```

---

# 12. Analytics Design

The analytics layer deliberately uses SQL aggregation.

Airline performance can calculate:

- total flights
- on-time flights
- delayed flights
- cancelled flights
- average delay
- bookings

Route analysis groups by:

```text
Origin + Destination
```

Daily analysis can use:

```sql
DATE(scheduled_departure)
```

to produce daily operational trends.

---

# 13. Why SQL Instead of Doing Everything in Pandas?

This is fundamentally a SQL/database project.

### MySQL/SQL handles

- joins
- filtering
- grouping
- aggregation
- business calculations
- database-level analytics

### Python handles

- application logic
- calling queries
- formatting
- Streamlit UI
- visualization

### Pandas handles

- receiving SQL results
- lightweight DataFrame manipulation
- presentation-oriented transformations

This keeps database/business logic in the database rather than duplicating it in Python.

---

# 14. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Application development |
| Streamlit | Web application/UI |
| MySQL 8+ | Relational database |
| mysql-connector-python | MySQL connectivity |
| Pandas | DataFrame processing |
| Plotly | Interactive visualization |
| python-dotenv | Environment configuration |
| Git | Version control |
| GitHub | Repository hosting |

---

# 15. Fresh-Machine Installation

This section is specifically for another person who downloads the project from GitHub.

## Step 1 — Install MySQL

Install:

- MySQL Server
- MySQL Workbench

Make sure the MySQL Server is running.

During installation, the person will create their own MySQL password.

That password is **machine-specific**.

---

## Step 2 — Clone the Project

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd airport-flight-operations
```

---

## Step 3 — Create a Python Virtual Environment

```powershell
python -m venv .venv
```

Activate on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Alternative:

```powershell
.venv\Scripts\activate.bat
```

---

## Step 4 — Install Python Dependencies

```powershell
python -m pip install -r requirements.txt
```

If required:

```powershell
python -m pip install streamlit pandas plotly mysql-connector-python python-dotenv
```

---

# 16. Restore the Database From `Airlines data.sql`

The repository contains:

```text
database/Airlines data.sql
```

This is the database dump exported from the working project database.

### Option A — MySQL Workbench

Open MySQL Workbench and connect to the local MySQL Server.

Go to:

```text
Server
   ↓
Data Import
```

Choose:

```text
Import from Self-Contained File
```

Select:

```text
database/Airlines data.sql
```

If the dump contains the database creation/use statements, import it directly.

If it does not create the database automatically, first run:

```sql
CREATE DATABASE airport_operations;
```

Then select `airport_operations` as the target schema before importing.

---

## Option B — MySQL Command Line

If the dump requires a pre-created database:

```powershell
mysql -u root -p airport_operations < "database\Airlines data.sql"
```

Enter the MySQL password when prompted.

If the dump itself contains `CREATE DATABASE` and `USE` statements, follow the instructions inside the dump or import it through Workbench.

---

# 17. Verify the Restored Database

After importing the dump, open MySQL Workbench and run:

```sql
USE airport_operations;

SHOW TABLES;
```

The database should contain the project's core tables:

```text
airlines
aircraft_types
aircraft
airports
terminals
gates
pilots
flights
passengers
bookings
flight_status_history
```

Then verify sample counts:

```sql
SELECT COUNT(*) FROM airlines;
SELECT COUNT(*) FROM aircraft_types;
SELECT COUNT(*) FROM aircraft;
SELECT COUNT(*) FROM airports;
SELECT COUNT(*) FROM terminals;
SELECT COUNT(*) FROM gates;
SELECT COUNT(*) FROM pilots;
SELECT COUNT(*) FROM flights;
SELECT COUNT(*) FROM passengers;
SELECT COUNT(*) FROM bookings;
SELECT COUNT(*) FROM flight_status_history;
```

Also test:

```sql
SELECT * FROM flights LIMIT 5;
```

and:

```sql
SELECT * FROM bookings LIMIT 5;
```

---

# 18. Environment Configuration on Another PC

The `.env` file should **not** come from GitHub.

Create a local `.env` in the project root.

Copy the example:

```powershell
copy .env.example .env
```

Then open `.env`.

Example:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=airport_operations
DB_USER=root
DB_PASSWORD=THEIR_MYSQL_PASSWORD
```

`THEIR_MYSQL_PASSWORD` must be replaced with the password for the MySQL installation on that computer.

### Important

The application uses:

```text
localhost
```

which means it connects to the MySQL Server installed on that same computer.

The project does not automatically connect to the original developer's MySQL database.

---

# 19. Test the MySQL Connection Before Running Streamlit

From the project root:

```powershell
python -c "from services.data_service import get_connection; c=get_connection(); print('MYSQL CONNECTION SUCCESS'); c.close()"
```

Expected:

```text
MYSQL CONNECTION SUCCESS
```

If this fails with:

```text
Access denied for user 'root'@'localhost'
(using password: NO)
```

the `.env` password is missing/not being loaded.

If it fails with:

```text
Unknown database 'airport_operations'
```

the database has not been created/restored correctly.

If it fails with:

```text
Table 'airport_operations.flights' doesn't exist
```

the database exists but the SQL dump has not been imported correctly.

---

# 20. Run the Streamlit Application

Use:

```powershell
python -m streamlit run app.py
```

Then open the local address shown by Streamlit, normally:

```text
http://localhost:8501
```

---

# 21. Live Database Updates

The application is designed to query MySQL rather than use a permanently stored Python dataset.

Therefore, for example, if you run in MySQL Workbench:

```sql
UPDATE flights
SET status = 'Delayed',
    delay_minutes = 25
WHERE flight_id = 1;
```

the changed value will be reflected in Streamlit when the relevant page/query is refreshed or rerun.

Likewise, inserting a booking in MySQL changes the database result used by the application.

### The live flow is:

```text
MySQL Workbench
      ↓
MySQL Server
      ↓
Updated database
      ↓
Streamlit rerun / refresh
      ↓
Python executes SQL again
      ↓
Updated result appears
```

---

# 22. Common Database Setup Problems

## `Access denied for user 'root'@'localhost'`

Cause:

The application is not receiving the correct MySQL credentials.

Check `.env`:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_actual_password
DB_NAME=airport_operations
```

---

## `using password: NO`

Cause:

`DB_PASSWORD` is empty or `.env` is not being loaded.

Check:

```text
.env
```

exists in the **project root**, next to `app.py`.

Restart Streamlit after changing `.env`.

---

## `Unknown database 'airport_operations'`

Cause:

The database has not been created/restored.

Import:

```text
database/Airlines data.sql
```

---

## `Table doesn't exist`

Cause:

The database exists but the dump was not imported correctly.

Run:

```sql
USE airport_operations;
SHOW TABLES;
```

---

## `Unknown column 'f.passenger_count'`

Cause:

The query references a column that does not exist in the actual schema.

Resolution:

Use the relational booking model and calculate passenger count from bookings.

---

# 23. SQL Injection Prevention

User input should be parameterized.

Avoid:

```python
query = "SELECT * FROM flights WHERE flight_number = '" + flight_number + "'"
```

Prefer:

```python
query = """
SELECT *
FROM flights
WHERE flight_number = %s
"""

run_query(query, (flight_number,))
```

This keeps user input separate from SQL syntax.

---

# 24. Performance Principles

Do not retrieve unnecessary data.

Prefer:

```sql
SELECT required_columns
FROM flights
WHERE condition
LIMIT 100;
```

rather than loading an entire large table into Pandas and filtering it afterward.

Filtering, aggregation, and joins should generally happen in MySQL. The application should retrieve only what the current page needs.

---

# 25. Application Verification

After installation, test every page.

### Dashboard

Verify:

- page loads
- KPI values appear
- status chart appears
- airline chart appears
- recent arrival/departure table appears
- no SQL errors appear

### Flight Operations

Verify:

- records load
- joins work
- filters work
- timestamps appear
- passenger counts appear

### Passengers & Bookings

Verify:

- passenger information loads
- booking information loads
- analytics display

### Operational Intelligence

Verify:

- operational calculations load
- alerts/tables display
- no missing-column errors occur

### Analytics & Reports

Verify:

- airline performance loads
- route performance loads
- daily summary loads
- charts render
- tables render

---

# 26. Testing Database Changes

To confirm that the application is live, make a safe test change in Workbench and refresh Streamlit.

For example:

```sql
SELECT *
FROM flights
LIMIT 5;
```

After making a controlled change, refresh the relevant Streamlit page.

The new SQL result should be displayed.

This demonstrates that:

```text
Database change
      ↓
SQL query
      ↓
Python service
      ↓
Streamlit
```

is functioning correctly.

---

# 27. Evolution from Prototype to Final Application

During development, some early UI code used hardcoded Python sample records.

That was useful only for initially testing the interface.

The final direction is:

```text
Hardcoded Python data
        ↓
        ❌

MySQL database
        ↓
        SQL
        ↓
Python
        ↓
Streamlit
        ↓
        ✅
```

This change makes the application genuinely database-driven.

---

# 28. Git/GitHub Workflow

Check the repository:

```powershell
git status
```

Review changes:

```powershell
git diff
```

Stage:

```powershell
git add .
```

Commit:

```powershell
git commit -m "feat: finalize airport operations system"
```

---

# 29. `.gitignore`

The repository should ignore:

```text
.env
.venv/
__pycache__/
*.pyc
.vscode/
.streamlit/secrets.toml
```

Do **not** commit:

- `.env`
- MySQL passwords
- virtual environments
- local secrets

The safe file to commit is:

```text
.env.example
```

---

# 30. Replace the Previous Git Remote

Inspect the current remote:

```powershell
git remote -v
```

Remove the old remote:

```powershell
git remote remove origin
```

Add the new GitHub repository:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

Verify:

```powershell
git remote -v
```

---

# 31. Push the Final Project to `main`

```powershell
git branch -M main
```

Then:

```powershell
git add .
git commit -m "feat: finalize airport operations system"
git push -u origin main
```

Before pushing, verify:

```powershell
git status
```

Make sure `.env` is not staged.

If it accidentally appears as staged:

```powershell
git restore --staged .env
```

---

# 32. Final Fresh-PC Setup — Quick Version

A new developer should be able to do:

```powershell
git clone <REPOSITORY_URL>
cd airport-flight-operations

python -m venv .venv
.venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
```

Then:

1. Install/start MySQL Server.
2. Open MySQL Workbench.
3. Import `database/Airlines data.sql`.
4. Verify the `airport_operations` database and tables.
5. Copy `.env.example` to `.env`.
6. Enter the local MySQL password.
7. Test the connection.
8. Run Streamlit.

```powershell
python -m streamlit run app.py
```

---

# 33. Final Architecture Summary

```text
                    GitHub
                      │
          ┌───────────┴───────────┐
          │                       │
       Python                  SQL Dump
      Application            Airlines data.sql
          │                       │
          ▼                       ▼
      Streamlit              MySQL Server
          │                       │
          │                 airport_operations
          │                       │
          └───────────────┬───────┘
                          ▼
                    Live SQL Results
                          │
                          ▼
                    Streamlit UI
```

---

# 34. Final Data Flow

```text
Airport Operational Data
          ↓
     MySQL Database
          ↓
     SQL Queries
          ↓
    Python Services
          ↓
      DataFrames
          ↓
     Streamlit UI
          ↓
Operational Decisions
```

The completed project demonstrates:

- relational database design
- SQL querying
- joins
- aggregation
- analytical reporting
- database connectivity
- Python integration
- Streamlit development
- interactive visualization
- operational decision support
- Git/GitHub collaboration
- reproducible database setup

---

# 35. Viva / Interview Explanation

A concise explanation:

> "This project is an Airport Flight Operations and Decision Support System built using MySQL, Python, and Streamlit. MySQL is the data layer and contains the relational data. SQL is responsible for joins, filtering, aggregation, and operational analytics. Python provides the database-access and application layer, while Streamlit provides the presentation layer. The dashboard retrieves live results from MySQL and presents them as KPIs, tables, and interactive charts. The database can also be exported and restored on another machine using the included SQL dump."

---

# 36. Why This Architecture Was Chosen

### Simple

```text
Streamlit
   ↓
Python
   ↓
MySQL
```

### Maintainable

Database operations are separated from page presentation.

### SQL-focused

The project demonstrates actual SQL skills instead of hiding all logic inside Python.

### Extensible

Additional pages and analytical queries can be added without rebuilding the database.

### Portable

The database dump allows another developer to recreate the database and data locally.

### Easy to explain

The entire system can be clearly described during a viva/interview.

---

# 37. Final Project Principle

> **MySQL is the source of truth; SQL performs the database and analytical work; Python integrates the database with the application; Streamlit presents the results.**

The SQL dump file provides the database structure and data required to reproduce the working project on another machine.

---

## Quick Start

```powershell
git clone <REPOSITORY_URL>
cd airport-flight-operations

python -m venv .venv
.venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt

# Start MySQL Server

# Import database/Airlines data.sql using MySQL Workbench

# Copy .env.example to .env
copy .env.example .env

# Configure your local MySQL credentials in .env

# Test the database connection

# Start the application
python -m streamlit run app.py
```

**Built with:** Python · Streamlit · MySQL · SQL · Pandas · Plotly
