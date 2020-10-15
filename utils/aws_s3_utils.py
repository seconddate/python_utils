"""
Created on 2019. 09. 05.
"""
import os
import json
import boto3
import botocore

with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) + '/config/config.json', 'r') as f:
    CONFIG = json.load(f)

class S3Utils():
    """ S3 Utils """
    s3 = boto3.resource('s3')
    bucket_name = CONFIG['BUCKET_NAME']

    def s3_upload_file(self, org_file_path, upload_file_path):
        '''
        S3 파일 업로드
        '''
        extra_args = {'CacheControl': 'max-age=20'}
        self.s3.meta.client.upload_file(org_file_path, self.bucket_name, upload_file_path, ExtraArgs=extra_args)

    def s3_download_file(self, download_file_path, output_file_name):
        '''
        S3 파일 다운로드
        '''
        try:
            print(self.s3.Bucket(self.bucket_name).download_file(download_file_path, output_file_name))
        except botocore.exceptions.ClientError as client_error:
            if client_error.response['Error']['Code'] == '404':
                print('파일이 없습니다. 경로를 확인해주세요.')
            else:
                raise Exception('파일 다운로드에서 에러가 발생하였습니다.')
