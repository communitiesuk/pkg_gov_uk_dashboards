"""Get data from a data source e.g. locally or blob storage"""

import os
from time import perf_counter
import polars as pl


def get_cds_odbc_connection_string(server: str) -> str:
    """Return the ODBC connection string for the CDS Dashboards database.

    Uses the Azure SQL username and password stored in environment variables.

    Raises:
        RuntimeError: If either required Azure SQL environment variable is missing.
    """
    username = os.environ.get("AZURE_SQL_SERVER_USER")
    password = os.environ.get("AZURE_SQL_SERVER_PASSWORD")

    if not username or not password:
        raise RuntimeError(
            "Missing AZURE_SQL_SERVER_USER or AZURE_SQL_SERVER_PASSWORD."
        )

    return (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={server};"
        "DATABASE=Dashboards;"
        f"UID={username};"
        f"PWD={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )


def read_cds_query_odbc(query: str, server: str) -> pl.DataFrame:
    """Read data from CDS using the direct ODBC path."""
    return pl.read_database(
        query,
        connection=get_cds_odbc_connection_string(server),
    )


class GenericDataQuery:
    """Static class for the generic data query."""

    filename: str
    dir: str
    query: str
    server: str
    stats_release: bool = False

    # @staticmethod
    def get_data_from_cds(self):
        """Pull data from CDS and write it to CSV."""
        print(self.filename)

        start = perf_counter()

        sql_query = read_cds_query_odbc(self.query(), self.server)

        print(f"{self.filename} query took {perf_counter()-start} seconds")

        os.makedirs(self.dir, exist_ok=True)
        sql_query.write_csv(self.get_file_location())

        if self.stats_release:
            return self.filename

        return None

    # @staticmethod
    def get_file_location(self):
        """Get the location of the file."""
        return os.path.join(self.dir, self.filename)
