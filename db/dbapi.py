import importlib
import os
def removeExt(name):
    new = ""
    for i in name.split(".")[:-1]:
        new+=i+"."
    return new[:-1]
class dbint:
    def __init__(self, dbobj):
        self.db = dbobj
        self.loaddbint()
    def loaddbint(self):
        dblibs = os.listdir("db")
        cnt = 0
        for lib in dblibs:
            if lib[0]!="_" and os.path.isfile("db/"+lib) and lib!="dbapi.py" and lib!="database.py":
                fixed = removeExt(lib)
                # print(fixed)
                module = __import__("db."+fixed)
                # print(module)
                getdb = getattr(getattr(module,fixed),"getAPI")
                setattr(self,fixed,getdb(self.db))
                cnt+=1
        print("loaded {} database API's".format(cnt))