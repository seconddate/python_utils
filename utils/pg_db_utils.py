import psycopg2
import sys, os
import json


with open(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + '/config/config.json', 'r') as f:
    config = json.load(f)

class PgDbUtils:
    """
    Postgresql DB utils
    """
    rds_host  = config['PG_DB_HOST']
    user_name = config['PG_USER_NAME']
    password = config['PG_PASSWORD']
    db_name = config['PG_DB_NAME']
    port = '5432'

    def db_conn(self):
        conn = psycopg2.connect(
            user=self.user_name,
            password=self.password,
            host=self.rds_host,
            database=self.db_name,
            port=self.port,
        )

        return conn

    def execute_select_query(self, sql, params):
        try:
            conn = self.db_conn()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            result = cursor.fetchall()

            return result
        except Exception as e:
            print('raise Exception : ' + str(e))
            raise Exception('Error!!')
        finally:
            if conn:
                cursor.close()
                conn.close()
            
    def execute_insert_query(self, sql, params):
        try:
            conn = self.db_conn()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
        except Exception as e:
            print('raise Exception : ' + str(e))
            raise Exception('Error!!')
        finally:
            if conn:
                cursor.close()
                conn.close()


    

    