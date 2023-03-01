class dbc:
    def __init__(self,dba):
        self.db = dba
    def checkBal(self,iid,cid):
        sql_query = "SELECT iid,cid,amnt FROM CURRENCY WHERE iid = %s AND cid = %s"
        rslt = self.db.execsql(sql_query,iid,cid)
        if len(rslt)==0:
            return 0
        else:
            return rslt[0][2]
    def addCurrency(self,iid,cid,amnt):
        if amnt<=0:
            return False
        ps_connection = self.db.getconn()
        if ps_connection:
            ps_cursor = ps_connection.cursor()
            q1 = "SELECT (iid,cid,amnt) FROM CURRENCY WHERE iid = %s AND cid = %s"
            ps_cursor.execute(q1,(iid,cid))
            if ps_cursor.rowcount==0:
                q2 = "INSERT INTO CURRENCY (iid,cid,amnt) VALUES (%s,%s,%s)"
                ps_cursor.execute(q2,(iid,cid,amnt))
            else:
                q3 = "UPDATE CURRENCY SET amnt = amnt + %s WHERE iid = %s AND cid = %s"
                ps_cursor.execute(q3,(amnt,iid,cid))
            ps_connection.commit()
            ps_cursor.close()
            self.db.putconn(ps_connection)
        return True
    def deductCurrency(self,iid,cid,amnt):
        if amnt<=0:
            return False
        ps_connection = self.db.getconn()
        if ps_connection:
            ps_cursor = ps_connection.cursor()
            q1 = "UPDATE CURRENCY SET amnt = amnt - %s WHERE iid = %s AND cid = %s AND amnt >= %s"
            ps_cursor.execute(q1,(amnt,iid,cid,amnt))
            if ps_cursor.rowcount==0:
                rslt = False
            else:
                rslt = True
            ps_cursor.close()
            ps_connection.commit()
            self.db.putconn(ps_connection)
        return rslt