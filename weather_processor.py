from datetime import date, datetime
from scrape_weather import WeatherScraper
# from db_operations import DBOperations
# from plot_operations import PlotOperations

def menu():
    """Displays the menu for the user to select from."""
    print("1. Scrape all weather data.")
    print("2. Update weather data.")
    print("3. Generate a box plot with a year range of interest.")
    print("4. Generate a line plot with a month and year range of interest.")
    print("5. Exit.")

weather = WeatherScraper()
# db = DBOperations()
# plot = PlotOperations()

menu()

option = int(input("\nPlease select an option: "))

while option != 5:
    if option == 1:
        data = weather.get_data()
        # db.save_data(data)
        print("\nScraping complete.\n")
        menu()
        option = int(input("\nPlease select an option: "))
    elif option == 2:
        end_month = int(input("\nPlease enter a end month: "))
        end_year = int(input("\nPlease enter an end year: "))
        weather.update_scrape(datetime(end_year, end_month, datetime.now().day))
        print("\nUpdating complete.\n")
        # db.save_data(data)
        menu()
        option = int(input("\nPlease select an option: "))
    elif option == 3:
        start_year = int(input("\nPlease enter a start year: "))
        end_year = int(input("\nPlease enter an end year: "))
        # plot.plot_box_graph(start_year, end_year)
        print("\nPlotting complete.\n")
        menu()
        option = int(input("\nPlease select an option: "))
    elif option == 4:
        year = int(input("\nPlease enter a year: "))
        month = int(input("\nPlease enter a month: "))
        # plot.plot_line_graph(year, month)
        print("\nPlotting complete.\n")
        menu()
        option = int(input("\nPlease select an option: "))
    else:
        print("Invalid option.")
        menu()
        option = int(input("\nPlease select an option: "))