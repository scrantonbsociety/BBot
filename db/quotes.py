class dbq:
    def __init__(self, db):
        self.database = db

    def add(self, name: str, quote: str, userid: str):
        sql_query = 'INSERT INTO quotes (name,quote,user_id) VALUES (%s, %s, %s)' #might not work with auto_increment idk?
        rslt = self.database.execsql(sql_query,name,quote,userid)
        return userid

    #addQuote:

    def list(self, name: str):
        if(name == ""):
            sql_query = "SELECT * from quotes"        
            rslt = self.database.execsql(sql_query)
        else:
            sql_query = "SELECT * FROM quotes WHERE name=(%s)"
            rslt = self.database.execsql(sql_query,name)
        return rslt.fetchall()

    #removeQuote:
    
def getAPI(dbobj):
    return dbq(dbobj)