"""Used to plot desired weather data on a line plot as well as a box plot."""
import matplotlib.pyplot as plt

import dbcm
from db_operations import DBOperations

class PlotOperations():
    """Fetches the requested data and outputs two plots."""
    with dbcm.DBCM("weather.sqlite") as curr:

        def plot_line_graph(self, year, month):
            """Collects the desired month and year then plots on line plot."""
            db_operations = DBOperations()
            data_line_plot = db_operations.fetch_data_for_line(year, month)

            day = []
            line_temp = []
            day_num = 0

            for rows in data_line_plot:
                day_num += 1
                day.append(day_num)
                line_temp.append(rows[1])
            plt.xlabel("Day of the Month")
            plt.ylabel("Average Temperature")
            plt.title("Daily Weather for " + str(month) + " / " + str(year))
            plt.plot(day, line_temp)
            plt.show()

        def plot_box_graph(self, start_year, end_year):
            """Collects the desired start year and end year then plots on a box plot."""
            db_operations = DBOperations()
            data_box_plot = db_operations.fetch_data_for_box(start_year, end_year)

            box_temp = []
            all_temps = []

            for month_list in data_box_plot:
                for list_of_tuples in month_list:
                    box_temp.append(list_of_tuples[0])
                all_temps.append(box_temp)
                box_temp = []

            plt.boxplot(all_temps)
            plt.title("Average Monthly Temperatures from " + str(start_year) + " to " + str(end_year))
            plt.show()


# test:
# show_graphs = PlotOperations()
# show_graphs.plot_line_graph(2022, 11)
# show_graphs.plot_box_graph(2022,2022)
