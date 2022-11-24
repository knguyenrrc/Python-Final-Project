import matplotlib.pyplot as plt
from db_operations import DBOperations

class PlotOperations():

    data = DBOperations.fetch_data

    plt.figure()
    plt.boxplot(data)

    plt.show()