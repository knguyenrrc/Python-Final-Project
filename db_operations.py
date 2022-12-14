"""To hold and run database operations with the data gathered from scraping."""
import datetime
import dbcm
from scrape_weather import WeatherScraper

class DBOperations:
    """Class to run database Operations: create, purge, fetch, insert"""

    def __init__(self):
        """Initializes the class and sets the cursor"""
        # self.curr = cursor
        # with dbcm.DBCM(self.db_name) as cursor:
        #     self.curr = cursor

    def initialize_db(self):
        """Uses Cursor when initialized to create the database and prints out message."""
        with dbcm.DBCM("weather.sqlite") as curr:
            if curr is not None:
                curr.execute("""create table if not exists CHK_weather
                (id integer primary key autoincrement not null,
                sample_date text not null,
                location text not null,
                min_temp real not null,
                max_temp real not null,
                avg_temp real not null);""")
                print('Table created succesfully.')

    def purge_data(self):
        """Uses cursor on initialization to delete database"""
        with dbcm.DBCM("weather.sqlite") as curr:
            if curr is not None:
                curr.execute("""DELETE FROM CHK_weather;""")

    def check_data(self,date):
        """in house function to check if the database already
         contains the date data returns True/false if it exists"""
        with dbcm.DBCM("weather.sqlite") as curr:
            if curr is not None:
                exists = False
                if curr is not None:
                    sql="""SELECT * FROM CHK_weather WHERE sample_date LIKE ?;"""
                    sub_value = (date,)
                    curr.execute(sql,sub_value)
                if curr.fetchone():
                    exists = True
                else:
                    exists = False
            return exists

    def save_data(self,data):
        """calls check data and based on the result will insert data into the database"""
        with dbcm.DBCM("weather.sqlite") as curr:
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
                    curr.execute(sql,vals)

    def fetch_data(self):
        """returns data as a tuple to be used."""
        with dbcm.DBCM("weather.sqlite") as curr:
            records = curr.execute("SELECT * FROM CHK_weather")
            # for rows in records:
            #     print(rows)
            return records

    def fetch_data_for_box(self, start_year, end_year):
        """Fetches and returns the weather data for a given set of years."""
        with dbcm.DBCM("weather.sqlite") as curr:
            records = []
            begin = str(start_year) + "-01-01"
            end = str(end_year) + "-12-31"

            for month in range(1, 13):
                if month <= 9:
                    weather_data = ("SELECT avg_temp FROM CHK_weather WHERE (sample_date BETWEEN '" + begin + "' AND '" + end + "') AND sample_date LIKE '____%-0" + str(month) + "-__%'")
                    curr.execute(weather_data)
                    records.append(curr.fetchall())
                else:
                    weather_data = ("SELECT avg_temp FROM CHK_weather WHERE (sample_date BETWEEN '" + begin + "' AND '" + end + "') AND sample_date LIKE '____%-" + str(month) + "-__%'")
                    curr.execute(weather_data)
                    records.append(curr.fetchall())

        return records


    def fetch_data_for_line(self, year, month):
        """Fetches the weather data for a given month of a given year."""
        with dbcm.DBCM("weather.sqlite") as curr:
            start_data = str(year) + "-" + str(month) + "-__%"
            _sql_ = ("Select sample_date, avg_temp FROM CHK_weather WHERE sample_date LIKE '" + start_data + "'" )
            curr.execute(_sql_)
            records = curr.fetchall()

        return records
    
    def fetch_latest_date(self):
        """Fetches latest date stored in database"""
        with dbcm.DBCM("weather.sqlite") as curr:
            record = curr.execute("SELECT MAX(sample_date) FROM CHK_weather")
            result = curr.fetchone()
        return result[0]

# data_dictionary = WeatherScraper()
# dict = data_dictionary.get_data()
# scrape_dict = data_dictionary.update_scrape(datetime.datetime(2022,11,11))
# print("Finished scraping...")

# with dbcm.DBCM("weather.sqlite") as dbcm_cursor:
#     ops = DBOperations(dbcm_cursor)
#     ops.initialize_db()
#     ops.purge_data()
#     ops.save_data(dict)

# with dbcm.DBCM("weather.sqlite") as dbcm_cursor:
#     ops = DBOperations(dbcm_cursor)
#     ops.fetch_data()

# with dbcm.DBCM("weather.sqlite") as dbcm_cursor:
#     ops = DBOperations(dbcm_cursor)
#     ops.fetch_data_for_box(2022, 2022)

# database = DBOperations()
# print(database.fetch_data_for_box(2021, 2022))

# db = DBOperations()

# a = db.fetch_latest_date().split('-')
# for val in a:
#     val = int(val)
# print(datetime.datetime(int(a[0]),int(a[1]),int(a[2])))
