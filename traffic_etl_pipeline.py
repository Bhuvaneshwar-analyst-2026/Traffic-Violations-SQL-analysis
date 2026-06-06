import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
import numpy as np

# Configuration & Connection 

DB_URL = "mysql+mysqlconnector://your_username:your_password@127.0.0.1:3306/sql_project"

# All columns from the Moving Violations Raw Data 
VIOLATION_COLUMNS = [
    'OBJECTID', 'LOCATION', 'XCOORD', 'YCOORD', 'ISSUE_DATE', 'ISSUE_TIME',
    'ISSUING_AGENCY_CODE', 'ISSUING_AGENCY_NAME', 'ISSUING_AGENCY_SHORT',
    'VIOLATION_CODE', 'VIOLATION_PROCESS_DESC', 'PLATE_STATE', 'ACCIDENT_INDICATOR',
    'DISPOSITION_CODE', 'DISPOSITION_TYPE', 'DISPOSITION_DATE', 'FINE_AMOUNT',
    'TOTAL_PAID', 'PENALTY_1', 'PENALTY_2', 'PENALTY_3', 'PENALTY_4', 'PENALTY_5',
    'RP_MULT_OWNER_NO', 'BODY_STYLE', 'LATITUDE', 'LONGITUDE', 'MAR_ID',
    'GIS_LAST_MOD_DTTM'
]

# All columns from the DC Weather Raw Data 
WEATHER_COLUMNS = [
    'name', 'datetime', 'tempmax', 'tempmin', 'temp', 'feelslikemax',
    'feelslikemin', 'feelslike', 'dew', 'humidity', 'precip', 'precipprob',
    'precipcover', 'preciptype', 'snow', 'snowdepth', 'windgust', 'windspeed',
    'winddir', 'sealevelpressure', 'cloudcover', 'visibility', 'solarradiation',
    'solarenergy', 'uvindex', 'severerisk', 'sunrise', 'sunset', 'moonphase',
    'conditions', 'description', 'icon', 'stations'
]

# DATA DIRECTORY AND FILE LISTS 
DATA_DIR = 'data/'

VIOLATION_FILES = [
    'Moving_Violations_Issued_in_November_2024.csv',
    'Moving_Violations_Issued_in_October_2024.csv',
    'Moving_Violations_Issued_in_September_2024.csv',
    'Moving_Violations_Issued_in_August_2024.csv'
]

WEATHER_FILES = [
    'Washington, DC, United St... 2024-09-01 to 2025-09-30.csv'
]

CHUNK_SIZE = 5000


try:
    ENGINE = create_engine(DB_URL)
    print("SQLAlchemy Engine created.")
except Exception as err:
    print(f"Error creating SQLAlchemy engine: {err}")
    raise


def reset_raw_tables(engine):
    """
    Truncate raw tables so the ETL can be re-run without PK conflicts.
    ONLY do this for staging/raw tables.
    """
    print("\nTruncating raw tables: dc_weather_raw, moving_violations_raw ...")
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE dc_weather_raw"))
        conn.execute(text("TRUNCATE TABLE moving_violations_raw"))
    print("Truncate complete.\n")


# 2) Weather Data Loading

def load_weather_pandas(filename, engine):
    """Reads weather data using Pandas and loads it to SQL."""
    print(f"Processing weather file: {filename}")
    full_path = DATA_DIR + filename

    try:
        df = pd.read_csv(full_path, encoding='utf-8')

        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce').dt.date
        df['sunrise'] = pd.to_datetime(df['sunrise'], errors='coerce')
        df['sunset'] = pd.to_datetime(df['sunset'], errors='coerce')

# Numeric Conversion 
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df['source_file'] = filename

        df.to_sql(
            name='dc_weather_raw',
            con=engine,
            if_exists='append',
            index=False
        )
        print(f"Weather rows inserted from {filename}. Total rows: {len(df)}\n")

    except Exception as e:
        print(f"ERROR reading/inserting weather file {filename}: {e}\n")


# 3) Violations Data Loading

def load_mv_pandas(filename, engine, chunk_size):
    """Reads violations data using Pandas chunking and loads it to SQL."""
    print(f"Processing violations file: {filename} (using {chunk_size} chunks)")
    full_path = DATA_DIR + filename

    all_cols_map = {col: 'object' for col in VIOLATION_COLUMNS}

# Columns that should be numeric
    numeric_to_float_cols = [
        'OBJECTID', 'XCOORD', 'YCOORD', 'MAR_ID',
        'FINE_AMOUNT', 'TOTAL_PAID', 'PENALTY_1', 'PENALTY_2', 'PENALTY_3',
        'PENALTY_4', 'PENALTY_5', 'LATITUDE', 'LONGITUDE'
    ]
    date_cols = ['ISSUE_DATE', 'DISPOSITION_DATE']

    try:
        total_rows_inserted = 0

        for i, chunk in enumerate(
            pd.read_csv(full_path, encoding='utf-8',
                        dtype=all_cols_map, chunksize=chunk_size)
        ):
            # Convert numeric columns
            for col in numeric_to_float_cols:
                if col in chunk.columns:
                    chunk[col] = pd.to_numeric(chunk[col], errors='coerce')

            for col in date_cols:
                if col in chunk.columns:
                    chunk[col] = chunk[col].astype(str).str.split().str[0]
                    chunk[col] = pd.to_datetime(
                        chunk[col],
                        format='%Y/%m/%d',
                        errors='coerce'
                    ).dt.date

            dttm_col = 'GIS_LAST_MOD_DTTM'
            if dttm_col in chunk.columns:
                chunk[dttm_col] = chunk[dttm_col].astype(str).str.split('+').str[0]
                chunk[dttm_col] = pd.to_datetime(
                    chunk[dttm_col],
                    format='%Y/%m/%d %H:%M:%S',
                    errors='coerce'
                )

            chunk['source_file'] = filename

            chunk.to_sql(
                name='moving_violations_raw',
                con=engine,
                if_exists='append',
                index=False
            )

            total_rows_inserted += len(chunk)
            print(f" {total_rows_inserted}")

        print("Violations file load complete. total_rows_inserted")

    except Exception as e:
        print(f"error reading/inserting violations file {filename} {e}")


# 4) Matplotlib Function
def plot_analysis(engine):
    """Executes Q3 and generates a bar chart using Matplotlib."""
    print("\n--- Generating Analysis Plot (Q3) ---")

    query_q3 = """
        SELECT 
            DAYNAME(ISSUE_DATE) AS DayOfWeek, 
            COUNT(OBJECTID) / COUNT(DISTINCT ISSUE_DATE) AS Avg_Tickets_Per_Day 
        FROM 
            moving_violations_raw 
        GROUP BY 
            DayOfWeek 
        ORDER BY 
            FIELD(DayOfWeek, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');
    """

    try:
        df_plot = pd.read_sql(query_q3, con=engine)

        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        df_plot['DayOfWeek'] = pd.Categorical(df_plot['DayOfWeek'],
                                              categories=day_order,
                                              ordered=True)
        df_plot = df_plot.sort_values('DayOfWeek')

        plt.figure(figsize=(10, 6))
        plt.bar(df_plot['DayOfWeek'], df_plot['Avg_Tickets_Per_Day'], color='darkcyan')
        plt.title('Average Daily Moving Violations by Day of the Week')
        plt.xlabel('Day of the Week')
        plt.ylabel('Average Tickets Issued')
        plt.grid(axis='y', linestyle='--', alpha=0.5)

        plot_filename = 'average_tickets_by_day.png'
        plt.savefig(plot_filename)
        plt.close()
        print("Plot saved successfully as {plot_filename}")

    except Exception as e:
        print(f"error generating plot {e}")


# 5) RUN THE LOADERS
if __name__ == '__main__':
    
    reset_raw_tables(ENGINE)

    for wf in WEATHER_FILES:
        load_weather_pandas(wf, ENGINE)

    for vf in VIOLATION_FILES:
        load_mv_pandas(vf, ENGINE, CHUNK_SIZE)

    plot_analysis(ENGINE)

    print("ETL Process Complete. Analysis Plot Generated.")
