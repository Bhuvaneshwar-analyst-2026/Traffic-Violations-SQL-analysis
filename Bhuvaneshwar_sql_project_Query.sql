USE sql_project;

CREATE TABLE dc_weather_raw (
    name              VARCHAR(100),
    datetime          DATETIME,
    tempmax           DOUBLE,
    tempmin           DOUBLE,
    temp              DOUBLE,
    feelslikemax      DOUBLE,
    feelslikemin      DOUBLE,
    feelslike         DOUBLE,
    dew               DOUBLE,
    humidity          DOUBLE,
    precip            DOUBLE,
    precipprob        INT,
    precipcover       DOUBLE,
    preciptype        VARCHAR(50),
    snow              DOUBLE,
    snowdepth         DOUBLE,
    windgust          DOUBLE,
    windspeed         DOUBLE,
    winddir           DOUBLE,
    sealevelpressure  DOUBLE,
    cloudcover        DOUBLE,
    visibility        DOUBLE,
    solarradiation    DOUBLE,
    solarenergy       DOUBLE,
    uvindex           INT,
    severerisk        INT,
    sunrise           DATETIME,
    sunset            DATETIME,
    moonphase         DOUBLE,
    conditions        VARCHAR(100),
    description       VARCHAR(500),
    icon              VARCHAR(50),
    stations          VARCHAR(255),
    source_file       VARCHAR(255)
);
CREATE TABLE moving_violations_raw (
    OBJECTID               BIGINT,
    LOCATION               VARCHAR(255),
    XCOORD                 BIGINT,
    YCOORD                 BIGINT,
    ISSUE_DATE             DATE,
    ISSUE_TIME             VARCHAR(10),
    ISSUING_AGENCY_CODE    VARCHAR(20),
    ISSUING_AGENCY_NAME    VARCHAR(100),
    ISSUING_AGENCY_SHORT   VARCHAR(50),
    VIOLATION_CODE         VARCHAR(50),
    VIOLATION_PROCESS_DESC VARCHAR(255),
    PLATE_STATE            VARCHAR(10),
    ACCIDENT_INDICATOR     VARCHAR(5),
    DISPOSITION_CODE       VARCHAR(50),
    DISPOSITION_TYPE       VARCHAR(50),
    DISPOSITION_DATE       DATE,
    FINE_AMOUNT            DECIMAL(10,2),
    TOTAL_PAID             DECIMAL(10,2),
    PENALTY_1              DECIMAL(10,2),
    PENALTY_2              DECIMAL(10,2),
    PENALTY_3              DECIMAL(10,2),
    PENALTY_4              DECIMAL(10,2),
    PENALTY_5              DECIMAL(10,2),
    RP_MULT_OWNER_NO       VARCHAR(20),
    BODY_STYLE             VARCHAR(50),
    LATITUDE               DOUBLE,
    LONGITUDE              DOUBLE,
    MAR_ID                 BIGINT,
    GIS_LAST_MOD_DTTM      DATETIME,
    source_file            VARCHAR(255)
);


ALTER TABLE moving_violations_raw
MODIFY COLUMN OBJECTID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT;

SELECT COUNT(*) FROM dc_weather_raw;     
SELECT COUNT(*) FROM moving_violations_raw; 

select * from dc_weather_raw;
select * from moving_violations_raw;

USE sql_project;
# A.List every agency that has issued moving violations tickets for each month.
SELECT DATE_FORMAT(ISSUE_DATE, '%Y-%m') AS YearMonth, 
    ISSUING_AGENCY_NAME,
    COUNT(OBJECTID) AS violations_total_tickets
FROM moving_violations_raw 
GROUP BY YearMonth, ISSUING_AGENCY_NAME 
ORDER BY YearMonth, violations_total_tickets DESC;

# B. How many tickets have been issued by agencies since October 1, 2024?
SELECT ISSUING_AGENCY_NAME, COUNT(OBJECTID) AS Total_Tickets_Since_Oct_1st 
FROM moving_violations_raw 
WHERE ISSUE_DATE >= '2024-10-01'
GROUP BY ISSUING_AGENCY_NAME;    
    
# C. What is the average number of tickets issued by day of the week (i.e. Monday, Tuesday, etc.)?
SELECT DAYNAME(ISSUE_DATE) AS DayOfWeek, 
    COUNT(OBJECTID) / COUNT(DISTINCT ISSUE_DATE) AS Avg_Tickets_Per_Day 
FROM moving_violations_raw 
GROUP BY DayOfWeek 
ORDER BY FIELD(DayOfWeek, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');   
    
# D. How many tickets were issued during periods of rain?
SELECT COUNT(OBJECTID) AS Tickets_During_Rain
FROM moving_violations_raw
WHERE ISSUE_DATE IN (
    SELECT DATE(datetime) -- Get the list of rainy dates
    FROM dc_weather_raw
    WHERE precip > 0
);
    
# E. What was the total precipitation for each month?
SELECT DATE_FORMAT(datetime, '%Y-%m') AS YearMonth, 
    SUM(precip) AS Total_Precipitation_In_Inches 
FROM dc_weather_raw 
GROUP BY YearMonth 
ORDER BY YearMonth;    
    
# F. What is the total fine issued each month for vehicles traveling more than 10 mph over the speed limit?   
SELECT DATE_FORMAT(ISSUE_DATE, '%Y-%m') AS YearMonth, 
    SUM(FINE_AMOUNT) AS Total_Speeding_Fines_Revenue 
FROM moving_violations_raw 
WHERE VIOLATION_PROCESS_DESC LIKE '%SPEED%' 
AND VIOLATION_PROCESS_DESC NOT LIKE '%UP TO TEN MPH%' 
GROUP BY YearMonth 
ORDER BY YearMonth; 
    
# G. What is the average number of tickets written for each hour of a standard day (i.e. from 7:00-8:00am, 8:00-9:00am, etc.)?
SELECT LPAD(FLOOR(ISSUE_TIME / 100), 2, '0') AS Hour_Of_Day, 
    COUNT(OBJECTID) / COUNT(DISTINCT ISSUE_DATE) AS Avg_Tickets 
FROM moving_violations_raw 
GROUP BY Hour_Of_Day 
ORDER BY Hour_Of_Day;    
    
# H. Compare tickets associated with accidents on rainy days vs non-rainy days. 
SELECT
    CASE
        WHEN (
            SELECT w.precip 
            FROM dc_weather_raw w
            WHERE DATE(w.datetime) = v.ISSUE_DATE 
            LIMIT 1 
        ) > 0 THEN 'Rainy'
        ELSE 'Non-Rainy'
    END AS Weather_Condition,
    COUNT(v.OBJECTID) AS Accident_Tickets
FROM moving_violations_raw v
WHERE v.ACCIDENT_INDICATOR = 'Y'
GROUP BY Weather_Condition;