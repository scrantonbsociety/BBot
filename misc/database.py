import psycopg2
import json
import random
import uuid
with open("auth.config","r") as f:
    dbconf = json.load(f)["sql"]
con = psycopg2.connect(database = dbconf["database"], user = dbconf["username"], password = dbconf["password"], host=dbconf["host"], port=dbconf["port"])
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