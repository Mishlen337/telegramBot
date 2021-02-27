from matplotlib import pyplot as plt

def stock_plot(x_axis : list, y_axis : list):
    fig, ax = plt.subplots()
    p = plt.plot(x_axis, y_axis)
    plt.savefig("plot.png")
    
