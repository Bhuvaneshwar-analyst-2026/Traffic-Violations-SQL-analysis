<div align="center">

# DC Traffic Violations SQL Analysis

## Project Overview

Analyzed **real Washington DC moving violation records** alongside daily weather data to uncover patterns in traffic enforcement, violations, and weather correlation using MySQL, Python, and Pandas.

**Course:** MIS 664A — Database Management Systems
**Institution:** University of Dayton
**Author:** Bhuvaneshwar Sannappareddy
**Tools:** MySQL · Python · Pandas · SQLAlchemy · Matplotlib

---

## Datasets

| Dataset | Source | Period | Records |
|---|---|---|---|
| DC Moving Violations | Washington DC Open Data Portal | Aug–Nov 2024 | 500,000+ |
| DC Weather Data | Visual Crossing API | Sep 2024–Sep 2025 | 365 days |

---

## Database Structure

Two tables linked by **date field** in `sql_project` database:

**`moving_violations_raw`** — Each row = one traffic ticket

| Column | Description |
|---|---|
| OBJECTID | Unique ticket ID |
| ISSUE_DATE | Date of violation |
| ISSUE_TIME | Time of violation |
| ISSUING_AGENCY_NAME | Name of issuing agency |
| VIOLATION_PROCESS_DESC | Type of violation |
| FINE_AMOUNT | Fine in dollars |
| ACCIDENT_INDICATOR | Whether accident was involved |
| LATITUDE / LONGITUDE | GPS location |

**`dc_weather_raw`** — Each row = one day of DC weather

| Column | Description |
|---|---|
| datetime | Date of weather record |
| temp | Average temperature |
| precip | Precipitation amount |
| conditions | Weather description |
| windspeed | Wind speed |
| humidity | Humidity percentage |

---

## SQL Analysis — 8 Key Business Questions

| # | Business Question | SQL Technique |
|---|---|---|
| A | Tickets issued per agency per month | GROUP BY, DATE_FORMAT |
| B | Tickets issued since October 1, 2024 | WHERE date filter |
| C | Average tickets by day of week | DAYNAME, COUNT/DISTINCT |
| D | Tickets issued during rain | Subquery, date JOIN |
| E | Total precipitation per month | SUM, DATE_FORMAT |
| F | Speeding fines over 10mph per month | LIKE filter, SUM |
| G | Average tickets by hour of day | FLOOR, LPAD, GROUP BY |
| H | Accident tickets — rainy vs non-rainy | CASE WHEN, Correlated Subquery |

---

## ETL Pipeline

Built a complete Python ETL pipeline using Pandas and SQLAlchemy:

1. Read raw CSV files in chunks of 5,000 rows
2. Clean and format date and time columns
3. Convert numeric fields with error handling
4. Load into MySQL using to_sql with append mode
5. Generate bar chart visualization using Matplotlib

---

## Key Findings

- Rainy weather correlates with higher accident related violations
- Ticket issuance peaks during weekday morning rush hours
- Multiple agencies show distinct monthly enforcement patterns
- Speeding fines over 10mph generate significant monthly revenue

---

## Files in This Repository

| File | Description |
|---|---|
| `Bhuvaneshwar_sql_project_Query.sql` | All 8 SQL queries and table creation scripts |
| `Bhuvaneshwar_sql_project_code.py` | Python ETL pipeline — Pandas and SQLAlchemy |
| `Bhuvaneshwar_sql_project_documentation.docx` | Full project documentation and analysis report |

---

## Skills Demonstrated

- **SQL** — Complex JOINs, Subqueries, CASE WHEN, GROUP BY, Date Functions
- **Python** — Pandas, SQLAlchemy, Matplotlib, chunked CSV processing
- **ETL** — Extract Transform Load pipeline design
- **Database Design** — MySQL schema creation and optimization
- **Data Analysis** — Weather correlation, time-series, agency benchmarking

---

> **Data Source:** Publicly available Washington DC Open Data portal and Visual Crossing weather API.
