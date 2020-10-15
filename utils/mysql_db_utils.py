"""
Created on 2019. 09. 05.
@author: seconddate
"""

import os
import json
import sys
from utils.logger import Logger
import pymysql
import pymysql.cursors

class MysqlDbUtils:

    def __init__(self):
        """생성자
        """
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) + '/config/config.json', 'r') as f:
            config = json.load(f)
        
        self.conn = pymysql.connect(
            host=config['DB_HOST'],
            user=config['USERNAME'],
            password=config['PASSWORD'],
            db=config['DB_NAME'],
            charset='utf8',
        )
        self.logger = Logger()

    def execute_select_query(self, sql, params=()):
        """EXECUTE SELECT QUERY

        Args:
            sql (str): SQL
            params (tuple): 파라미터

        Returns:
            list: Result LIST
        """
        self.logger.info(sql)
        with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchall()
            
        return result
    
    def execute_insert_query(self, sql, params=()):
        """EXECUTE INSERT QUERY

        Args:
            sql (str): SQL
            params (tuple): 파라미터
        """
        self.logger.info(sql)
        with self.conn.cursor() as cursor:
            cursor.execute(sql, params)
        self.conn.commit()

    def close_db(self):
        """Close Connection
        """
        self.conn.close()
