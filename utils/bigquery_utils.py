"""
Created on 2020. 01. 29.
@author: seconddate
"""
from google.cloud import bigquery

class BigqueryUtils:
    """Bigquery Utils

    ###
    export GOOGLE_APPLICATION_CREDENTIALS=~/.gcp/credentials.json
    ###
    """
    query_timeout = 30 # in seconds

    def __init__(self, env):
        """생성자

        Args:
            env (str): Stage
            params (dict): parameters
        """

        self.dataset_id = f"{env}_keyword_research"
        self.__bigquery_client = bigquery.Client()
        self.__dataset = self.__bigquery_client.dataset(self.dataset_id)

    def is_exist_bigquery_table(self, table_id):
        """테이블 존재 여부 체크

        Args:
            table_id (str): 테이블 명
        """
        is_exist = False

        table_ref = self.__dataset.table(table_id)
        try:
            self.__bigquery_client.get_table(table_ref)
            is_exist = True
        except Exception as exception:
            print(str(exception))

        return is_exist

    def execute_delete_query(self, table_id, adv_id):
        """Bigquery 삭제 쿼리 실행

        Args:
            table_id (str): 테이블 명,
            created_at (str): 생성일
        """

        query = f"""
        DELETE FROM 
            {self.dataset_id}.{table_id}
        WHERE
            adv_id = '{adv_id}'
        """

        query_job = self.__bigquery_client.query(query)
        query_job.result()
        print(f'EXECUTE QUERY : {query}')

    def if_exist_delete_bigquery_table(self, table_id):
        """Bigquery 테이블 삭제(존재하면)

        Args:
            table_id (str): 테이블 명
        """
        table_ref = self.__dataset.table(table_id)
        self.__bigquery_client.delete_table(table_ref, not_found_ok=True)

    def create_partitioned_bigquery_table(self, table_id, schema, partition_field):
        """파티션으로 나뉜 빈 테이블 생성

        Args:
            table_id (str): 테이블 명
            schema (list): 스키마 정보
            partition_field (str): 파티션 필드
        """

        table_ref = self.__dataset.table(table_id)
        table = bigquery.Table(table_ref, schema=schema)
        table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field=partition_field
        )
        table = self.__bigquery_client.create_table(table)

        return table

    def load_from_gcs_to_bigquery_table(self, table_id, data_path, write_disposition):
        """GCS -> Bigquery Load

        Args:
            table_id (str): 테이블 명
            data_path (str): GCS PATH
            write_disposition (str): 테이블 쓰기 옵션
        """

        table_ref = self.__dataset.table(table_id)
        table = self.__bigquery_client.get_table(table_ref)

        job_config = bigquery.LoadJobConfig()
        job_config.source_format = 'NEWLINE_DELIMITED_JSON'
        job_config.ignore_unknown_values = True
        job_config.write_disposition = write_disposition

        load_job = self.__bigquery_client.load_table_from_uri(
            data_path,
            table,
            job_config=job_config
        )
        print(f"Load 시작 >>>>> {load_job.started}")
        print(f"Data_path >>>>> {data_path}")
        print(f"Table >>>>> {table}")
        load_job.result(timeout=300)
        assert load_job.state == 'DONE'
        print(f"Load 끝 >>>>> {load_job.ended}")
        print(f"Load Success!!!")

    def execute_select_on_bigquery(self, query):
        result_list = []

        print(f'EXECUTE QUERY : {query}')
        query_job = self.__bigquery_client.query(query)
        # assert query_job.state == 'RUNNING'

        # Waits for the query to finish
        iterator = query_job.result(timeout=self.query_timeout)
        rows = list(iterator)

        assert query_job.state == 'DONE'
        for row in rows:
            result_list.append(dict(row))

        return result_list

    def insert_rows(self, table_id, row_list):
        table_ref = self.__dataset.table(table_id)
        table = self.__bigquery_client.get_table(table_ref)
        if row_list:
            errors = self.__bigquery_client.insert_rows(table, row_list)

            print(errors)

            assert errors == []
        else:
            print('INSERT 데이터가 없습니다.')


    