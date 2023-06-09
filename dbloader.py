import json
from db import dbapi
from db import database
dblogin = {}
def loadConfig():
    global dblogin
    with open("auth.config","r") as f:
        config = json.load(f)
    dblogin = config["sql"]
def get():
    db = database.db(dblogin)
    db.connect()
    dba = dbapi.dbint(db)
    return dba
loadConfig()