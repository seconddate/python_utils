"""
Created on 2020. 01. 29.
@author: seconddate
"""
from google.cloud import storage
import boto3

class GcsUtils:
    """
    Google Cloud Storage Utils
    """

    def __init__(self, env, gcp_credentials):
        """생성자

        Args:
            env (str): Stage
            gcp_credential (dict): gcp_credentials
        """

        project_id = 'solution-trendlab'

        storage_client = storage.Client(project=project_id, credentials=gcp_credentials)
        self.__bucket = storage_client.get_bucket(f"{env}-trendlab.emforce.co.kr")

    def gcs_object_is_exist(self, gcs_path):
        """Google Cloud Storage Object Check

        Args:
            gcs_path (str): Google Cloud Storage Path

        Returns:
            bool: exist_bool
        """
        gcs_check = False

        blob = self.__bucket.get_blob(gcs_path)

        if blob:
            if blob.exists():
                gcs_check = True

        return gcs_check

    def gcs_object_download_as_string(self, gcs_path):
        """GET Google Cloud Storage OBJECT

        Args:
            gcs_path (str): Google Cloud Storage Path

        Returns:
            str: Download_as_string Object
        """

        blob = self.__bucket.get_blob(gcs_path)

        return blob.download_as_string()

    def gcs_object_upload_from_string(self, gcs_path, upload_str, content_type):
        """Upload Google Cloud Storage String

        Args:
            gcs_path (str): gcs_path
            upload_str (str): 업로드String
            content_type (str): content_type
        """
        blob = self.__bucket.get_blob(gcs_path)

        blob.upload_from_string(upload_str, content_type=content_type)


    def gcs_object_upload_from_file(self, gcs_path, file_path, content_type):
        """Upload Google Cloud Storage File

        Args:
            file_path (str): file_path
            gcs_path (str): gcs_path
            content_type (str): content_type
        """

        blob = self.__bucket.blob(gcs_path)
        blob.upload_from_filename(filename=file_path, content_type=content_type)

    # def transfer_object_from_s3_to_gcs(self)
