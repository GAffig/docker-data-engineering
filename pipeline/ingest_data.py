#!/usr/bin/env python
# coding: utf-8

import tempfile
import requests
import pyarrow.parquet as pq

import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm


# -------------------------------------------------------------------
# NOTE:
# dtype and parse_dates are no longer required for PARQUET,
# but keeping them here does NOT break anything.
# -------------------------------------------------------------------
dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


# -------------------------------------------------------------------
# INGEST FUNCTION (PARQUET, CSV-LIKE FLOW)
# -------------------------------------------------------------------
def ingest_data(
        url: str,
        engine,
        target_table: str,
        chunksize: int = 100000,
) -> None:
    """
    Ingest NYC Taxi PARQUET data into PostgreSQL using CSV-like chunk logic.
    """

    print(f"Downloading: {url}")

    # Keep everything inside this block so temp file stays alive
    with tempfile.NamedTemporaryFile(suffix=".parquet") as f:

        # 1) Download parquet file
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=1024 * 1024):  # 1MB
                if chunk:
                    f.write(chunk)
        f.flush()

        # 2) Create batch iterator (acts like read_csv(chunksize=...))
        pf = pq.ParquetFile(f.name)
        df_iter = pf.iter_batches(batch_size=chunksize)

        # 3) First batch → create table + insert
        first_chunk = next(df_iter).to_pandas()

        first_chunk.head(0).to_sql(
            name=target_table,
            con=engine,
            if_exists="replace",
            index=False
        )
        print(f"Table {target_table} created")

        first_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists="append",
            index=False
        )
        print(f"Inserted first chunk: {len(first_chunk)}")

        # 4) Remaining batches
        for batch in tqdm(df_iter):
            df_chunk = batch.to_pandas()
            df_chunk.to_sql(
                name=target_table,
                con=engine,
                if_exists="append",
                index=False
            )
            print(f"Inserted chunk: {len(df_chunk)}")

    print(f"done ingesting to {target_table}")


# -------------------------------------------------------------------
# CLI
# -------------------------------------------------------------------
@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL username')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default='5432', help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--year', default=2025, type=int, help='Year for data ingestion')
@click.option('--month', default=11, type=int, help='Month for data ingestion')
@click.option('--chunksize', default=100000, type=int, help='Chunk size')
@click.option('--target-table', default='yellow_taxi_data', help='Target table name')
def main(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, chunksize, target_table):
    """
    Ingest NYC Taxi data into PostgreSQL.
    """

    engine = create_engine(
        f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'
    )

    url_prefix = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
    url = f'{url_prefix}/green_tripdata_{year:04d}-{month:02d}.parquet'

    ingest_data(
        url=url,
        engine=engine,
        target_table=target_table,
        chunksize=chunksize
    )


if __name__ == '__main__':
    main()
