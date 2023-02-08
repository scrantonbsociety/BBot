import uuid
class dba:
    def __init__(self, db):
        self.database = db
    def getUser(self, uid):
        sql_query = 'SELECT id,iid FROM USERS where id = %s'
        rslt = self.database.execsql(sql_query, str(uid))
        if len(rslt)==0:
            return None
        else:
            return rslt[0][1]
    def register(self, uid):
        iid = self.getUser(uid)
        if iid==None:
            iid = str(uuid.uuid4())
            sql_query = 'INSERT INTO USERS(id,iid) VALUES (%s,%s)'
            self.database.execsql(sql_query, str(uid), iid)
            return iid,True
        return iid,False
