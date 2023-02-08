class dba:
    def __init__(self, db):
        self.database = db
    async def userExists(self, uid):
        sql_query = 'SELECT (id,iid) FROM USERS where id = %s'
        rslt = self.database.execsql(sql_query, str(uid))
        return len(rslt)==1