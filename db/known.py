class known():
    def __init__(self,db):
        self.db = db
    def lookup(self,title,type):
        sql_query = "SELECT name,type,iid FROM known WHERE name = %s AND type = %s"
        rslt = self.db.execsql(sql_query,title,type)
        if len(rslt)==0:
            return ""
        else:
            return rslt[0][2]
    def lookupnames(self,iid,type):
        sql_query = "SELECT name FROM known WHERE iid = %s AND type = %s"
        rslt = self.db.execsql(sql_query,iid,type)
        newrslt = []
        for line in rslt:
            newrslt.append(line[0])
        return newrslt
    def add(self,title,type,iid):
        lookup = self.lookup(title,type)
        if lookup=="":
            sql_query = "INSERT INTO known (name,type,iid) VALUES (%s,%s,%s)"
            self.db.execsql(sql_query,title,type,iid)
            return iid
        elif lookup==iid:
            return iid
        else:
            return lookup
def getAPI(dbobj):
    return known(dbobj)