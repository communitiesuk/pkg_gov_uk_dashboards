"""BlobStorageGateway class"""

import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from dotenv import load_dotenv

load_dotenv(override=True)


class BlobStorageGateway:
    """A class for getting information about a storage container."""

    def __init__(
        self,
        container: str = None,
        conn_string_env_variable: str = None,
        storage_account_url_env_variable: str = None,
    ):
        self.conn_string_env_variable = conn_string_env_variable
        self.storage_account_url_env_variable = storage_account_url_env_variable
        self.blob_service_client = self.get_blob_service_client()
        self.container_client = (
            self.blob_service_client.get_container_client(container)
            if container
            else None
        )

    def get_blob_service_client(self):
        """
        Create and return an Azure BlobServiceClient.

        This method first checks for an Azure Storage connection string in the
        `AZURE_STORAGE_CONNECTION_STRING` environment variable. If present, the
        client is created using the connection string.

        If no connection string is found, the method falls back to using
        `DefaultAzureCredential`, which supports Azure Managed Identity.

        Returns:
            BlobServiceClient: An authenticated client for accessing Azure Blob
            Storage.
        """
        if self.conn_string_env_variable and os.getenv(self.conn_string_env_variable):
            return BlobServiceClient.from_connection_string(
                os.getenv(self.conn_string_env_variable)
            )
        if self.storage_account_url_env_variable and os.getenv(
            self.storage_account_url_env_variable
        ):
            credential = DefaultAzureCredential()
            account_url = os.getenv(self.storage_account_url_env_variable)
            return BlobServiceClient(account_url=account_url, credential=credential)
        if os.getenv("AZURE_STORAGE_CONNECTION_STRING"):
            return BlobServiceClient.from_connection_string(
                os.getenv("AZURE_STORAGE_CONNECTION_STRING")
            )
        credential = DefaultAzureCredential()
        account_url = os.getenv("STORAGE_ACCOUNT_URL")
        return BlobServiceClient(account_url=account_url, credential=credential)

    def get_blob_client(self, blob_name: str):
        """
        Get a BlobClient for a specific blob within the configured container.

        This method returns a `BlobClient` scoped to the container provided when
        the `BlobStorageGateway` was initialised. The returned client can be used
        to perform blob-level operations such as upload, download, delete, or
        retrieving blob properties.

        Args:
            blob_name (str): The name or path of the blob within the container.

        Returns:
            BlobClient: A client for interacting with the specified blob.
        """
        return self.container_client.get_blob_client(blob_name)

    def download_blob_as_bytes(self, blob_name, max_concurrency=None, encoding=None):
        """
        Download a blob from Azure Blob Storage.

        Args:
            blob_name (str): Name or path of the blob within the container.
            max_concurrency (int, optional): Maximum number of parallel connections
                used for downloading. Defaults to None.
            encoding (str, optional): Encoding used to decode the blob content.
                Defaults to None.

        Returns:
            bytes | str: Blob contents as bytes, or as a string if encoding is specified.
        """
        blob_downloader = self.container_client.download_blob(
            blob_name, max_concurrency=max_concurrency, encoding=encoding
        )
        return blob_downloader.readall()

    def upload_blob(self, blob_name, data, overwrite: bool):
        """Upload data to the blob."""
        blob_client = self.get_blob_client(blob_name)
        blob_client.upload_blob(data, overwrite=overwrite)
