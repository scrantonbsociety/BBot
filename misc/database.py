import asyncpg
import json
import random
import uuid
class db:
    def __init__(self,dbconf):
        self.conf = dbconf
    async def connect(self):
        self.con = await asyncpg.connect(host=self.conf["host"], port=self.conf["port"], user=self.conf["username"], password=self.conf["password"], database=self.conf["database"])
    async def execsql(self, query, *args):
        values = await self.con.fetch(query, args)
        return values
def test():
    print("test")
def userExists(uid):
    cur = con.cursor()
    sql_query = 'SELECT (id,iid) FROM USERS where id = %s'
    cur.execute(sql_query, (str(uid),))
    rslt = cur.fetchall()
    cur.close()
    return len(rslt)==1
def register(uid):
    cur = con.cursor()
    iid = str(uuid.uuid4())
    sql_query = 'INSERT INTO USERS VALUES (%s,%s)'
    cur.execute(sql_query, (str(uid),iid,))
    cur.close()
    return userExists(uid)