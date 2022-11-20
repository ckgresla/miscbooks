# Example of a ScatterPlot in Matplotlib with a trend line (moving average via a cumsum)

import numpy as np 
import matplotlib
import matplotlib.pyplot as plt


values = np.random.randint(0, 100, 1000) #generate sample scatter data
values = [i**2 for i in values if i % 2 == 0] #add some noise

# Trend Line via Moving Average
ma_n = 100 #number of timesteps in moving average
def moving_avg(x, n=ma_n):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[n:] - cumsum[:-n]) / float(n)


# Will display output in a python window on local os (can also save output as a png)
if __name__ == "__main__":
    plt.scatter(np.arange(len(values)), values, label='individual timesteps & their values')
    plt.plot(moving_avg(values), label=f'moving average of last {ma_n} timesteps', color="pink")
    plt.title(f'Sample Scatterplot w Trendline')
    plt.xlabel('Timesteps')
    plt.ylabel('Value of Interest')
    plt.legend()
    plt.show()
