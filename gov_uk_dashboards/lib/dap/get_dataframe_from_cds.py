"""Returns a dataframe after connecting to CDS, otherwise uses a csv already saved in the file"""

# import os
# import json
# import pyodbc
# import boto3


# def get_data_from_cds_or_fallback_to_csv(
#     cds_sql_query: str, csv_path: str, secret_name: str, cds_server_name: str
# ) -> pd.DataFrame:
#     """Tries to return dataframe from CDS first via Pydash credentials,
#     otherwise via Amazon WorkSpaces,
#     otherwise via a file from folder.
#     Inputs:
#         cds_sql_query(str): SQL query string
#         csv_path(str): Filepath for location of csv to fallback to
#         secret_name(str): AWS Secrets Manager, secret name containing CDS credentials.
#         cds_server_name(str): CDS Server name used in connection string
#     Returns:
#         pd.DataFrame
#     """
#     if (
#         "DATA_FOLDER_LOCATION" in os.environ
#         and os.environ["DATA_FOLDER_LOCATION"] == "tests/"
#     ) or ("STAGE" in os.environ and os.environ["STAGE"] == "testing"):
#         return pd.read_csv(csv_path)

#     try:
#         conn = pyodbc.connect(
#             _get_pydash_connection_string(secret_name, cds_server_name)
#         )
#         print("Dataframe has been loaded from CDS using Pydash credentials")

#         return pd.read_sql_query(
#             cds_sql_query,
#             conn,
#         )

#     except Exception as credential_error:  # pylint: disable=broad-except
#         try:
#             print(
#                 "Failed to load dataframe using Pydash credentials: ", credential_error
#             )
#             conn = pyodbc.connect(
#                 "Driver={SQL Server};"
#                 f"Server={cds_server_name};"
#                 "Database=Dashboards;"
#                 "Trusted_Connection=yes;"
#             )
#             print(
#                 "Dataframe has been loaded from CDS using Windows login authentication"
#             )

#             return pd.read_sql_query(
#                 cds_sql_query,
#                 conn,
#             )

#         except pyodbc.Error as conn_error_except:
#             print(
#                 "Failed to load dataframe using Windows login authentication: ",
#                 conn_error_except,
#             )
#             print("Dataframe has been loaded from CSV")
#             return pd.read_csv(csv_path)


# def _get_pydash_connection_string(secret_name: str, cds_server_name: str):
#     """
#     Pydash aka DAP Hosting requires username and password
#     Inputs:
#         secret_name(str): AWS Secrets Manager, secret name containing CDS credentials.
#         cds_server_name(str): CDS Server name used in connection string
#     """
#     credentials = _pydash_sql_credentials(secret_name)
#     conn_string_dap = (
#         "Driver={/usr/lib/libmsodbcsql-18.so};"
#         f"Server={cds_server_name};"
#         "TrustServerCertificate=yes;"
#         "Database=Dashboards;"
#     )
#     return (
#         f"{conn_string_dap}UID={credentials['username']};PWD={credentials['password']};"
#     )


# def _pydash_sql_credentials(secret_name: str):
#     """
#     Logging into CDS from Pydash requires user name and password.
#     This method will return a dictionary containing the keys "username" and "password".
#     Raises `botocore.exceptions.ClientError` if no credentials could be obtained
#     Inputs:
#         secret_name(str): AWS Secrets Manager, secret name containing CDS credentials.
#     Returns:
#         dict:   a dictionary containing the keys "username" and "password"
#     """
#     region_name = "eu-west-1"
#     # Create a Secrets Manager client
#     session = boto3.session.Session()
#     client = session.client(service_name="secretsmanager", region_name=region_name)
#     # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager
# .html#SecretsManager.Client.get_secret_value

#     get_secret_value_response = client.get_secret_value(SecretId=secret_name)

#     secret = get_secret_value_response["SecretString"]

#     credentials = json.loads(secret)
#     return credentials
