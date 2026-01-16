# Docker Data Engineering Pipeline

A containerized data engineering pipeline for ingesting and analyzing NYC taxi trip data into PostgreSQL using Docker and Docker Compose.

## Project Overview

This project demonstrates a modern data engineering workflow using Docker containerization and PostgreSQL for data storage. The pipeline downloads NYC taxi trip data in Parquet format, processes it with pandas, and loads it into a PostgreSQL database for analysis and querying.

**Key Features:**
- Automated data ingestion from remote Parquet files
- Docker containerization for consistent environments
- PostgreSQL database with pgAdmin4 UI for data management
- SQL queries for data analysis and insights
- Python-based data processing with pandas and SQLAlchemy
- Command-line interface for flexible data loading
- Comprehensive dependency management with `uv` package manager

## Project Structure

```
pipeline/
├── Dockerfile              # Container image definition with Python 3.13
├── docker-compose.yaml     # Multi-service orchestration (PostgreSQL + pgAdmin)
├── ingest_data.py          # Main data ingestion script
├── ingest_data_example.py  # Example ingestion script with sample data
├── pipeline.py             # Parameterized pipeline example
├── main.py                 # Entry point application
├── Homework1script.sql     # SQL analysis queries for taxi data
├── pyproject.toml          # Python project configuration and dependencies
└── notebook.ipynb          # Jupyter notebook for data exploration
```

## Technologies Used

- **Docker & Docker Compose**: Container orchestration and multi-service deployment
- **Python 3.13**: Core programming language
- **PostgreSQL 18**: Primary data warehouse
- **pgAdmin 4**: Web-based PostgreSQL administration and query tool
- **pandas**: Data manipulation and analysis
- **SQLAlchemy**: SQL toolkit and ORM for database interactions
- **PyArrow**: Efficient Parquet file handling
- **uv**: Fast Python package and project manager

## Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Python 3.13+ (for local development)
- Git for version control

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd docker-data-engineering/pipeline
   ```

2. **Start the Docker services:**
   ```bash
   docker compose up -d
   ```
   This will start:
   - PostgreSQL database on `localhost:5432`
   - pgAdmin4 on `localhost:8085`

3. **Build and run the ingestion container:**
   ```bash
   docker build -t taxi-pipeline .
   docker run --rm --network pipeline_default taxi-pipeline
   ```

4. **For local development with Python virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv sync
   ```

## Usage

### Docker-Based Data Ingestion

The Docker container automatically runs the ingestion script when started:

```bash
docker run --rm --network pipeline_default taxi-pipeline
```

### Local Python Execution

```bash
python ingest_data.py --help
```

### Accessing Data

**Via pgAdmin 4:**
1. Open browser: `http://localhost:8085`
2. Login with: admin@admin.com / root
3. Add PostgreSQL server with connection details:
   - Host: `pgdatabase`
   - Port: `5432`
   - User: `root`
   - Password: `root`

**Via SQL Query Tool (pgcli):**
```bash
pgcli -h localhost -U root -d ny_taxi
```

## Database Configuration

The `docker-compose.yaml` defines:

- **PostgreSQL Service (`pgdatabase`)**
  - Image: postgres:18
  - Database: ny_taxi
  - User: root
  - Password: root
  - Volume: `ny_taxi_postgres_data` (persistent storage)
  - Port: 5432

- **pgAdmin Service**
  - Image: dpage/pgadmin4
  - Email: admin@admin.com
  - Password: root
  - Port: 8085

## Data Ingestion Details

The `ingest_data.py` script provides:

- **Remote Data Download**: Downloads NYC taxi Parquet files via HTTP
- **Chunked Processing**: Handles large files efficiently with configurable chunk sizes (default: 100,000 rows)
- **Automatic Table Creation**: Creates PostgreSQL table from first chunk schema
- **Batch Insertion**: Appends data in chunks with progress tracking (tqdm)
- **Data Type Mapping**: Specifies proper PostgreSQL types for taxi data fields

### Data Types Supported

```python
VendorID, passenger_count, RatecodeID, PULocationID, DOLocationID, payment_type
trip_distance, fare_amount, extra, mta_tax, tip_amount, tolls_amount, 
improvement_surcharge, total_amount, congestion_surcharge
Datetime fields: tpep_pickup_datetime, tpep_dropoff_datetime
String fields: store_and_fwd_flag
```

## SQL Analysis Examples

The `Homework1script.sql` file contains sample analytical queries:

- **Trip Distance Analysis**: Count trips with distance ≤ 1 mile
- **Maximum Distance by Day**: Find the day with longest trip distance
- **Zone Revenue Analysis**: Calculate total amount by pickup location
- **Tip Analysis**: Identify highest tips and route information

## Development

### Install Development Dependencies

```bash
uv sync --group dev
```

This includes Jupyter for interactive notebooks and pgcli for command-line database access.

### Running Jupyter

```bash
jupyter notebook notebook.ipynb
```

### Python Dependencies

Core dependencies (from `pyproject.toml`):
- pandas >= 2.3.3
- psycopg2-binary >= 2.9.11
- pyarrow >= 22.0.0
- sqlalchemy >= 2.0.45
- tqdm >= 4.67.1

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Docker Container (taxi-pipeline)                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Python 3.13 + Dependencies                           │   │
│  │ • ingest_data.py (main ingestion logic)              │   │
│  │ • Downloads remote Parquet files                     │   │
│  │ • Processes data with pandas & PyArrow               │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
           │ (network: pipeline_default)
           │
           ├─────────────────────────────────────────────────┐
           │                                                 │
    ┌──────▼──────────┐                          ┌──────────▼────┐
    │  PostgreSQL 18  │                          │  pgAdmin 4     │
    │  ny_taxi        │                          │  localhost:8085│
    │  localhost:5432 │                          └────────────────┘
    │  Volume:        │
    │  ny_taxi_...    │
    └─────────────────┘
```

## Best Practices

- **Environment Isolation**: Use Docker containers to avoid dependency conflicts
- **Data Persistence**: Named volumes ensure data survives container restarts
- **Efficient Processing**: Parquet format and chunked processing for large datasets
- **Type Safety**: Explicit data type definitions for data integrity
- **Progress Tracking**: tqdm progress bars for long-running operations
- **Fast Package Management**: uv package manager for faster installation and lock-file management

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port already in use | Change port mapping in docker-compose.yaml |
| Cannot connect to database | Ensure services are running: `docker compose ps` |
| Permission denied on volume | Check Docker daemon and user permissions |
| Out of memory during ingestion | Reduce chunksize parameter in ingest_data.py |
| pgAdmin login fails | Verify PGADMIN_DEFAULT_EMAIL and PASSWORD in docker-compose.yaml |

## Future Enhancements

- [ ] Support for multiple data sources (yellow, green, fhv taxi data)
- [ ] Data validation and quality checks
- [ ] Scheduled pipeline execution with Airflow or cron
- [ ] Real-time data streaming with Kafka
- [ ] Advanced analytics and visualization with Metabase or Superset
- [ ] Automated testing and CI/CD pipeline
- [ ] Data partitioning for improved query performance

## Contributing

1. Create a feature branch
2. Make your changes
3. Test locally with Docker
4. Submit a pull request

## License

MIT License

## Contact & Support

For issues, questions, or contributions, please open an issue in the repository.
