import sqlite3
from asyncio.windows_events import NULL
class DBCM():
    def __init__(self,name):
        self.conn = sqlite3.connect(name)
        self.curr = NULL
    def __enter__(self):
        try:
            self.curr= self.conn.cursor()
            return self.curr
        except Exception as error:
            print("Exception assigning cursor in dbcm")
       
        
    def __exit__(self, exc_type, exc_value, exc_trace):
        self.conn.commit()
        self.curr.close()
        self.conn.close()
        print("Database Commited and Connections and Cursor are closed.")