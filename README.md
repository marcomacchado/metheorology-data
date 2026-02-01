# INMET Historical Weather Data Pipeline

> An ETL pipeline and REST API to ingest, normalize, and serve historical meteorological data from the Brazilian National Institute of Meteorology (INMET).

## 📖 Project Overview

This project aims to solve the challenge of processing fragmented and heterogeneous weather data files provided by INMET. It builds a robust backend infrastructure to consolidate decades of hourly measurements from automatic stations into a structured Relational Database, exposing this data via a clean HTTP API for analysis and visualization.

**Key Features:**
* **Data Ingestion:** Automated parsing of raw CSV files (2000-2025) handling inconsistent headers, date formats, and numeric delimiters.
* **Normalization:** Type-safe conversion of meteorological variables (Temperature, Humidity, Pressure, etc.) to standard units.
* **Persistence:** High-performance storage using PostgreSQL for time-series data.
* **Access:** RESTful API (FastAPI) for querying station metadata and observation history.

---

## 🛠️ Technology Stack

* **Language:** Python 3.10+
* **Database:** PostgreSQL 15 (planned)
* **Infrastructure:** Docker & Docker Compose
* **API Framework:** FastAPI (planned)
* **Data Source:** [INMET Portal](https://portal.inmet.gov.br/dadoshistoricos)

---

## 📂 Data Structure

The project handles two main types of data:

1.  **Station Metadata (`stations`):**
    * Source: `CatalogoEstaçõesAutomáticas.csv`
    * Contains: Station Name, WMO Code (e.g., A001), Latitude, Longitude, Altitude, Operation Status.

2.  **Hourly Observations (`observations`):**
    * Source: Yearly `.zip` archives containing daily CSVs per station.
    * Volume: Millions of records from year 2000 to present.
    * **Challenge:** The raw files contain varying schemas, encoding (`Latin-1` vs `UTF-8`), and floating-point separators (comma vs dot) which this pipeline normalizes.

---

## 🚀 Development Status & Roadmap

The project is currently in the **Infrastructure & Ingestion** phase.

### Phase 1: Core Logic & Parsing (✅ Completed)
- [x] **Exploratory Data Analysis:** Identified header variations and date/time patterns across 20+ years of files.
- [x] **Parser Implementation:** Created robust logic to convert raw CSV rows into typed Python dictionaries.
- [x] **Unit Conversion:** Handling of sentinel values (`-9999` to `None`) and decimal normalization.

### Phase 2: Infrastructure & Database (🚧 In Progress)
- [ ] **Containerization:** Setup `docker-compose` for PostgreSQL.
- [ ] **Schema Definition:** Design SQL tables for `stations` and `observations`.
- [ ] **Migration System:** Setup database version control (likely via Alembic or raw SQL).

### Phase 3: Ingestion Pipeline (📅 Planned)
- [ ] **Catalog Loader:** Script to populate the `stations` table.
- [ ] **Bulk Ingestion:** Efficiently process all `.zip` files and insert data into the database.
- [ ] **Error Handling:** Logging system for corrupted or malformed files.

### Phase 4: API & Distribution (📅 Planned)
- [ ] **API Setup:** Basic FastAPI skeleton.
- [ ] **Endpoints:** `/stations` (list/filter) and `/observations` (time-series query).
- [ ] **Documentation:** Swagger/OpenAPI auto-generated docs.

---

## 💻 Getting Started

### Prerequisites
* Python 3.10 or higher
* Docker & Docker Compose (for the database layer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/marcomacchado/metheorology-data.git](https://github.com/marcomacchado/metheorology-data.git)
    cd metheorology-data
    ```

2.  **Set up the environment (Example):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/Mac
    # .venv\Scripts\activate   # Windows
    pip install -r requirements.txt
    ```

3.  **Run the demo parser:**
    To verify the parsing logic on a sample file:
    ```bash
    python -m scripts.demo_parse_single_file
    ```

---