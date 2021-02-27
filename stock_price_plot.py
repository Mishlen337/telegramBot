from matplotlib import pyplot as plt
import yfinance as yf

def stock_plot(x_axis : list, y_axis : list):
    fig, ax = plt.subplots()
    p = plt.plot(x_axis, y_axis)
    plt.savefig("plot.png")
    


stock_plot(['1','2'], ['3', '80'])