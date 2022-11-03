""" Returns a dataframe after connecting to CDS, otherwise uses a csv already saved in the file"""
import json
import pandas as pd
import pyodbc
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

CONN_STRING = (
    "Driver={SQL Server};"
    "Server=DAP-SQLTEST\\CDS;"
    "Database=Dashboards;"
    "Trusted_Connection=yes;"
)

CONN_STRING_DAP = (
    "Driver={/usr/lib/libmsodbcsql-18.so};"
    "Server=10.154.41.171\\CDS,1444;"
    "TrustServerCertificate=yes;"
    "Database=Dashboards;"
)


def get_data_from_cds_or_fallback_to_csv(
    cds_sql_query: str, csv_path: str
) -> pd.DataFrame:
    """Tries to return dataframe from CDS first via Pydash credentials,
    otherwise via Amazon WorkSpaces,
    otherwise via a file from folder.
    Inputs:
        cds_sql_query(str): SQL query string
        csv_path(str): Filepath for location of csv
    Returns:
        pd.DataFrame
    """
    try:
        conn = pyodbc.connect(_get_pydash_connection_string())
        print("Dataframe has been loaded from CDS using Pydash credentials")
        
        return pd.read_sql_query(
            cds_sql_query,
            conn,
        )

    except (ClientError, NoCredentialsError) as credential_error:
        try:
            print("Failed to load dataframe using Pydash credentials: ", credential_error)
            conn = pyodbc.connect(CONN_STRING)
            print("Dataframe has been loaded from CDS using Windows login authentication")
            
            return pd.read_sql_query(
                cds_sql_query,
                conn,
            )

        except pyodbc.Error as conn_error_except:
            print("Failed to load dataframe using Windows login authentication: ", conn_error_except)
            print("Dataframe has been loaded from CSV")
            
            return pd.read_csv(csv_path)


def _get_pydash_connection_string():
    """Pydash aka DAP Hosting requires username and password"""
    credentials = _pydash_sql_credentials()

    return (
        CONN_STRING_DAP
        + "UID="
        + credentials["username"]
        + ";"
        + "PWD="
        + credentials["password"]
        + ";"
    )


def _pydash_sql_credentials():
    """
    Logging into CDS from Pydash requires user name and password.
    This method will return a dictionary containing the keys "username" and "password".
    Raises `botocore.exceptions.ClientError` if no credentials could be obtained
    Returns:
        dict:   a dictionary containing the keys "username" and "password"
    """
    # These values have come from David Wheatley
    secret_name = "test-pydash-sql-access"
    region_name = "eu-west-1"
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.get_secret_value

    get_secret_value_response = client.get_secret_value(SecretId=secret_name)

    secret = get_secret_value_response["SecretString"]

    credentials = json.loads(secret)
    return credentials
