"""Context Manager to open database Connections and Assign Cursor
and Commits at close"""
import sqlite3
from asyncio.windows_events import NULL
class DBCM():
    """Context Manager for Connection to the database."""
    def __init__(self,name):
        """dunder init that opens the connection to the database with sqlite3"""
        self.conn = sqlite3.connect(name)
        self.curr = NULL
    def __enter__(self):
        """enter checks to see if we can assign the cursor from the connection,
         wrapped around try/catch, exception will throw if connection fails"""
        try:
            self.curr= self.conn.cursor()
            return self.curr
        except Exception as error:
            print("Exception assigning cursor in dbcm,"+
            "connection to database may have failed. "+error)
    def __exit__(self, exc_type, exc_value, exc_trace):
        """upon exit will commit all database changes and close connections with a message."""
        self.conn.commit()
        self.curr.close()
        self.conn.close()
        print("Database Commited and Connections and Cursor are closed.")