"""To hold and run database operations with the data gathered from scraping."""

import datetime
import dbcm
from scrape_weather import WeatherScraper

class DBOperations:
    """Class to run database Operations: create, purge, fetch, insert"""
    def __init__(self,cursor):
        """Initializes the class and sets the cursor"""
        self.curr = cursor
        # with dbcm.DBCM(self.db_name) as cursor:
        #     self.curr = cursor

    def initialize_db(self):
        """Uses Cursor when initialized to create the database and prints out message."""
        if self.curr is not None:
            self.curr.execute("""create table if not exists CHK_weather
            (id integer primary key autoincrement not null,
            sample_date text not null,
            location text not null,
            min_temp real not null,
            max_temp real not null,
            avg_temp real not null);""")
            print('Table created succesfully.')
    
    def purge_data(self):
        """Uses cursor on initialization to delete database"""
        if self.curr is not None:
            self.curr.execute("""DELETE FROM CHK_weather;""")

    def check_data(self,date):
        """in house function to check if the database already
         contains the date data returns True/false if it exists"""
        if self.curr is not None:
            exists = False
            if self.curr is not None:
                sql="""SELECT * FROM CHK_weather WHERE sample_date LIKE ?;"""
                sub_value = (date,)
                self.curr.execute(sql,sub_value)
            if self.curr.fetchone():
                exists = True
            else:
                exists = False
        return exists

    def save_data(self,data):
        """calls check data and based on the result will insert data into the database"""
        for key,value in data.items():
            temp_store = []
            exists = self.check_data(key)
            if not exists :
                sql = """INSERT INTO CHK_weather
                    (sample_date, location, min_temp, max_temp, avg_temp)
                    VALUES(?, ?, ?, ?, ?)"""
                for temp_key,temp_value in value.items():
                    temp_store.append(temp_value)
                vals = (key, "Canada", temp_store[0], temp_store[1], temp_store[2])
                self.curr.execute(sql,vals)

    def fetch_data(self):
        """returns data as a tuple to be used."""
        records = self.curr.execute("SELECT * FROM CHK_weather")
        for rows in records:
            print(rows)
        return records

        
data_dictionary = WeatherScraper()
# dict = data_dictionary.get_data()
scrape_dict = data_dictionary.update_scrape(datetime.datetime(2022,11,11))
print("Finished scraping...")

# with dbcm.DBCM("weather.sqlite") as dbcm_cursor:
#     ops = DBOperations(dbcm_cursor)
#     ops.initialize_db()
#     ops.purge_data()
#     ops.save_data(scrape_dict)

with dbcm.DBCM("weather.sqlite") as dbcm_cursor:
    ops = DBOperations(dbcm_cursor)
    ops.fetch_data()

