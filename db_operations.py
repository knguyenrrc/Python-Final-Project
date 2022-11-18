from scrape_weather import WeatherScraper
from asyncio.windows_events import NULL
from contextlib import nullcontext
import sqlite3
import dbcm
import datetime

class DBOperations:
    def __init__(self,cursor):
        self.curr = cursor
        # with dbcm.DBCM(self.db_name) as cursor:
        #     self.curr = cursor

    def initialize_db(self):
      
        if(self.curr != NULL):
            self.curr.execute("""create table if not exists CHK_weather
            (id integer primary key autoincrement not null,
            sample_date text not null,
            location text not null,
            min_temp real not null,
            max_temp real not null,
            avg_temp real not null);""")
            print('Table created succesfully.')
    
    def purge_data(self):
        if(self.curr!=NULL):
            self.curr.execute("""DELETE FROM CHK_weather;""")

    def check_data(self,date):
        if(self.curr != NULL):
            exists = False
            if(self.curr!=NULL):
                sql="""SELECT * FROM CHK_weather WHERE sample_date LIKE ?;"""
                subVal = (date,)
                self.curr.execute(sql,subVal)
            if(self.curr.fetchone()):
                exists = True
            else:
                exists = False
        return exists

    def save_data(self,data):
        
        for k,v in data.items():
            temp_store = []
            exists = self.check_data(k)
            if(not exists):
                sql = """INSERT INTO CHK_weather
                    (sample_date, location, min_temp, max_temp, avg_temp)
                    VALUES(?, ?, ?, ?, ?)"""
                for kk,kv in v.items():
                    temp_store.append(kv)
                vals = (k, "Canada", temp_store[0], temp_store[1], temp_store[2])
                self.curr.execute(sql,vals)

    def fetch_data(self):
        records = self.curr.execute("SELECT * FROM CHK_weather")
        for rows in records:
            print(rows)
        return records

        
data_dictionary = WeatherScraper()
dict = data_dictionary.get_data()
print("Finished scraping...")

with dbcm.DBCM("weather.sqlite") as dbcm_cursor:
    ops = DBOperations(dbcm_cursor)
    ops.initialize_db()
    ops.purge_data()
    ops.save_data(dict)

with dbcm.DBCM("weather.sqlite") as dbcm_cursor:
    ops = DBOperations(dbcm_cursor)
    ops.fetch_data()

