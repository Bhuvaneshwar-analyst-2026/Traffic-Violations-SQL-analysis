<div align="center">

# 🚦 DC Traffic Violations SQL Analysis

[![SQL](https://img.shields.io/badge/SQL-MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Python](https://img.shields.io/badge/Python-Pandas-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Tableau](https://img.shields.io/badge/Tableau-Dashboard-E97627?style=for-the-badge&logo=tableau&logoColor=white)](https://www.tableau.com/)
[![University](https://img.shields.io/badge/University_of_Dayton-MIS_664A-red?style=for-the-badge)](https://www.udayton.edu/)

**Analyzing 500,000+ real Washington DC traffic violation records alongside daily weather data to uncover enforcement patterns, peak violation hours, and weather correlations.**

</div>

---

## 📌 Project Overview

This project analyzes **real Washington DC moving violation records** alongside **daily weather data** to answer key business questions about traffic enforcement patterns, agency performance, and how weather conditions impact violations.

| 📚 Course | MIS 664A — Database Management Systems |
|---|---|
| 🏫 Institution | University of Dayton |
| 👤 Author | Bhuvaneshwar Sannappareddy |
| 🛠️ Tools | MySQL · Python · Pandas · SQLAlchemy · Matplotlib |

---

## 📂 Datasets

| Dataset | Source | Period | Records |
|---|---|---|---|
| 🚗 DC Moving Violations | Washington DC Open Data Portal | Aug–Nov 2024 | 500,000+ |
| 🌦️ DC Weather Data | Visual Crossing API | Sep 2024–Sep 2025 | 365 days |

---

## 🗄️ Database Structure

Two tables linked by **date field** in `sql_project` database:

### `moving_violations_raw` — One row per traffic ticket
