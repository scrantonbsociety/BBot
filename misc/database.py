# import asyncpg
import psycopg2
from psycopg2 import pool
import json
import random
import uuid
class db:
    def __init__(self,dbconf):
        self.conf = dbconf
    def connect(self):
        self.pool = psycopg2.pool.SimpleConnectionPool(1,20,host=self.conf["host"], port=self.conf["port"], user=self.conf["user"], password=self.conf["password"], database=self.conf["database"])
    def execsql(self, query, *args):
        ps_connection = self.pool.getconn()
        if ps_connection:
            ps_cursor = ps_connection.cursor()
            ps_cursor.execute(query,args)
            try:
                records = ps_cursor.fetchall()
            except:
                records = []
            ps_connection.commit()
            ps_cursor.close()
            self.pool.putconn(ps_connection)
        return records