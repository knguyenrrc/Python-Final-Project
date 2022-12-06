import datetime
from db_operations import DBOperations
from plot_operations import PlotOperations
from scrape_weather import WeatherScraper

class WeatherProcessor:


    def __init__(self):
        self.ini_valid = False
        self.db = DBOperations()
        self.db.initialize_db()
        while(not self.ini_valid):
            self.initial_input = input("Select one of the options:\n"
            +"(1) Download ALL weather data.\n"
            +"(2) Update weather data.\n"
            +"(3) Generate box plot from (Year) to (Year)\n"
            +"(4) Generate Line plot for (Month + Year)\n"
            +"(Q) to quit!\n").strip()
            if self.initial_input == "1":
                print("Selected option 1: Downloading data...\n")
                self.download_data()  
            elif self.initial_input == "2":  
                print("Selected option 2: Update data...\n")
                self.update_data()               
            elif self.initial_input == "3":
                print("Selected option 3: Generate box plot"
                +"from (Year) to (Year)...\n")  
                self.gen_box_plot()             
            elif self.initial_input == "4":
                print("Selected option 4: Generate line plot"
                +"with (MM) + (YYYY)...\n")
                self.gen_line_plot()
            elif self.initial_input.lower() == "q":
                print("Good bye!")
                self.ini_valid = True
            else:
                print("Please Enter Valid Option!\n")

    def download_data(self):
        scraper = WeatherScraper()
        data = scraper.get_data()
        self.db.save_data(data)
        print("Downloaded All Data!\n")
    
    def update_data(self):
        scraper = WeatherScraper()
        return_date = self.db.fetch_latest_date()
        if return_date != "":
            latest_date = return_date.split('-')
            data = scraper.update_scrape(datetime.datetime(
                    int(latest_date[0]),
                    int(latest_date[1]),
                    int(latest_date[2])))
            print("Updated data!\n")

    def gen_box_plot(self):
        begin_year_valid = False
        end_year_valid = False
        quit = False
        today = datetime.date.today()
        current_year = today.year
      
        while not begin_year_valid and not quit:
            begin_year = input("Please enter the beginning year(YYYY) or (Q) to quit: ").strip()
            if begin_year.lower() == "q":
                quit = True     
            elif len(begin_year) == 4 and begin_year.isnumeric():
                begin_year = int(begin_year)
                if(begin_year<= current_year):
                    begin_year_valid = True
                    
                else:
                    print("Enter a valid beginning year!")
            else:
                print("Enter a valid beginning year")
                
               
        while not end_year_valid and not quit:
            end_year =input("Please enter the end Year(YYYY) or (Q) to quit: ").strip()
            
            if end_year.lower() == "q":
                quit = True
            elif len(end_year) == 4 and end_year.isnumeric():
                end_year = int(end_year)
                if(end_year<= current_year and end_year>=begin_year):
                    end_year_valid = True
                    
                else:
                    print("Enter a valid end year!")
            else:
                print("Enter a valid end year")

        
        if end_year_valid and begin_year_valid:
            plot_ops = PlotOperations()
            plot_ops.plot_box_graph(begin_year,end_year)

    def gen_line_plot(self):
        date = datetime.date.today()
        current_year = date.year
        month_valid = False
        year_valid = False
        quit = False
        while not month_valid and not quit:
            month = input("Please enter the month(MM) or (Q) to quit: ").strip()
            if month.lower() == "q":
                quit = True     
            elif len(month) <=2 and month.isnumeric():
                month = int(month)
                if month>0 and month<=12:
                    month_valid = True
                    
                else:
                    print("Enter a valid month!")
            else:
                print("Enter a valid month")
                
               
        while not year_valid and not quit:
            year =input("Please enter a Year(YYYY) or (Q) to quit: ").strip()
            
            if year.lower() == "q":
                quit = True
            elif len(year) == 4 and year.isnumeric():
                year = int(year)
                if(year<= current_year):
                    year_valid = True
                    
                else:
                    print("Enter a valid year!")
            else:
                print("Enter a valid year")
        
        if year_valid and month_valid:
            plot_ops = PlotOperations()
            plot_ops.plot_line_graph(year,month)

WeatherProcessor()

