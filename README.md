# Meteorology Data (INMET)

Python project for ingestion, normalization and disponibility of INMET (Brazil National Institute of Methereology) automic stations data through an API.

## 1. Project Goal

Build a back-end service that:

- Imports historical meteorological data from INMET .csv files into a relational database.
- Cleans and normalizes the data (types, missing values, invalid sentinel values like '-9999').
- Exposes an HTTP API to query station metadata and time series observations with filters and simples aggregations.

## 2. Data Sources

- **Station Catalog:**
    - CatalogogEstaçõesAutomáticas.csv
        - Contains metadata about meteorological stations (code, name, state, status, etc.).

- **Historical Data:**
    - Yearly _.zip_ files from years 2000-2025.
    - Each compressed file contains CSV files with hourly observations for each active station in that year.
    - The files include a metadata block followed by a header row and hourly measurements.

- Known data issues:
    - Some numeric fields use comma as decimal separator (e.g. `943,3`).
    - Some records have invalid or missing values represented as `-9999`.
    - Older and newer files may have slightly different header labels and date/time formats which must be normalized during ingestion.

## 3. Planned Architecture (High-level)
- **Language:** Python 3.10.12
- **Database:** PostgreSQL (relational, for time series and station metadata).
- **API:** FastAPI (HTTP endpoints with automatic documentation via OpenAPI/Swagger).
- **Environment:** WSL2, with support for running via Docker in the future.

### Core Components

1. **Ingestion/ETL**
    - Read station catalog CSV and load station metadata into the database.
    - Read yearly station CSV files.
    - Parse dates and times, converte to a 'timestamp' in UTC.
    - Convert numeric fields (handling comma decimal separators).
    - Replace invalid sentinel values (e.g '-9999') with 'NULL'.
    - Enforce uniqueness per (station_code, timestamp).

2. **Database Model**
    - *stations*
        - station_code (PK)
        - name
        - state
        - latitude
        - longitude
        - altitude
        - status (operational, inactive, etc.)
        - operation_start_date
    
    - *observations*
        - id (PK)
        - station_code (FK -> stations)
        - timestamp_utc (datetime representing thhe measurement date and hour in UTC)
        - temperature_air (°C)
        - humidity_air (%)
        - pressure (mB)
        - preciptation (mm)
        - wind_speed (m/s)
        - *other fields in .csv files*

3. **API Endpoints**

- GET /stations
    - List all stations, with optional filters like 'state' or 'status'

- GET /stations/{code}
    - Get the metadata for a single station

- GET /observations
    - Query observations with filters:
        - station_code
        - start (datetime)
        - end (datetime)
    - Pagination support

- GET /observations/daily
    - Aggregated daily statistics (min/avg/max temperature, total precipitation, etc.) for a station and period

## 4. Roadmap

Planned implementation step (high-level):

1. Define project structure and basic Python environment (dependencies, 'requirements.txt').
2. Implement station catalog parser (load `CatalogoEstaçõesAutomáticas.csv`, inspect columns and prepare data to be inserted into the `stations` table).
3. Define database schema and create initial migration.
4. Implement ingestion pipeline for a single station and a single year 
5. Generalize ingestion to process all years and stations
6. Implement API endpoints for station and observations.
7. Add basic tests (unit + integration)
8. Containerize the application with Docker and document how to run it locally.

## 5. Ho to Run (TO BE COMPLETED)
> This section will describe how to set up the virtual environment, install dependencies, configure the database and run the ingestion scripts and API.