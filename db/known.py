class known():
    def __init__(self,db):
        self.db = db
    def lookup(self,title,type=""):
        sql_query = "SELECT name,iid FROM known WHERE name = %s AND iid like %s"
        rslt = self.db.execsql(sql_query,title.lower(),type.lower()+"%%")
        if len(rslt)==0:
            return ""
        else:
            return rslt[0][1]
    def lookupnames(self,iid):
        sql_query = "SELECT name FROM known WHERE iid = %s"
        rslt = self.db.execsql(sql_query,iid.lower())
        print(rslt)
        newrslt = []
        for line in rslt:
            newrslt.append(line[0])
        print(newrslt)
        return newrslt
    def add(self,title,iid,source):
        lookup = self.lookup(title,iid)
        if lookup=="":
            sql_query = "INSERT INTO known (name,iid,source) VALUES (%s,%s,%s)"
            self.db.execsql(sql_query,title.lower(),iid.lower(),str(source))
            return iid
        elif lookup==iid:
            return iid
        else:
            return lookup
def getAPI(dbobj):
    return known(dbobj)