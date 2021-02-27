from matplotlib import pyplot as plt
from yahoo_finance import Share

def stock_plot(x_axis, y_axis):
    fig, ax = plt.subplots()
    p = plt.plot(x_axis, y_axis)
    return plt

def get_plot(stockname, callback):
    stock = Share(stockname)
    stock.get_historical()
    pass

stock = Share("TSLA")
print(stock.get_historical("24-07-2020", "25-07-2020"))