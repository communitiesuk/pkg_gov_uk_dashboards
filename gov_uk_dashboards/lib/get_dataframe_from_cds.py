""" Returns a dataframe after connecting to CDS, otherwise uses a csv already saved in the file"""
import json
import pandas as pd
import pyodbc
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from data.annual_housing_data import query
from lib.absolute_path import absolute_path

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

def data_from_cds_if_connected():
    """Tries to return dataframe from CDS first via Pydash credentials,
    otherwise via Amazon WorkSpaces,
    otherwise via a file from folder
    Returns:
        pd.DataFrame
    """
    try:
        credentials = pydash_sql_credentials()

        conn = pyodbc.connect(
            CONN_STRING_DAP
            + "UID="
            + credentials["username"]
            + ";"
            + "PWD="
            + credentials["password"]
            + ";"
        )
        print("From Pydash Data source is CDS")
        return pd.read_sql_query(
            query,
            conn,
        )

    except (ClientError, NoCredentialsError) as credential_error:
        try:
            conn = pyodbc.connect(CONN_STRING)
            print(credential_error, "From Amazon Workspace, data source is CDS")
            return pd.read_sql_query(
                query,
                conn,
            )

        except pyodbc.Error as conn_error_except:
            print(credential_error, conn_error_except, "Data source is CSV")
            return pd.read_csv(
                absolute_path("data/housing/2022-10-24_analyse_hd_annual_data.csv")
            )


def pydash_sql_credentials():
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