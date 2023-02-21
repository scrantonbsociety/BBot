# import asyncpg
import psycopg2
from psycopg2 import pool
import json
import random
import uuid
import os
class db(psycopg2.pool.AbstractConnectionPool):
    def __init__(self,dbconf):
        self.conf = dbconf
    def connect(self):
        self.pool = psycopg2.pool.SimpleConnectionPool(1,20,host=self.conf["host"], port=self.conf["port"], user=self.conf["user"], password=self.conf["password"], database=self.conf["database"])
        ps_connection = self.pool.getconn()
        if ps_connection:
            for init in os.listdir("db/initsql"):
                fullpath = "db/initsql/" + init
                if os.path.isfile(fullpath):
                    with open(fullpath,"r") as f:
                        fdata = f.read()
                        ps_cursor = ps_connection.cursor()
                        ps_cursor.execute(fdata)
                        ps_connection.commit()
                        ps_cursor.close()
            self.pool.putconn(ps_connection)
                    
                
    def __getattr__(self, attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        return getattr(self.pool, attr)
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