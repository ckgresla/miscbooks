import matplotlib.pyplot as plt
import numpy as np

# Assuming you have a list of numbers
data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10])

# Create histogram
plt.hist(data, bins=10, color='lightgrey', edgecolor='black')

# calculate quartiles
quartiles = np.percentile(data, [25, 50, 75])

# plot quartiles
for quartile in quartiles:
    plt.axvline(x=quartile, color='r', linestyle='--')

plt.grid(axis='y', alpha=0.75)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Histogram with Quartiles')

plt.show()
