# Sample Usage of the sklearn.datasets `make_moons` function -- nice util for making toy data
# Docs- https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_moons.html

import matplotlib.pyplot as plt 
from sklearn.datasets import make_moons


x, y = make_moons(n_samples=2000, noise=0.25, random_state=42)
x = x.T #transpose data, a 2D array for the number of samples (each moon, y, has two x-values that specify where that class exists)

def plot(x, y):
    # Data Features
    plt.xlabel('X1')
    plt.ylabel('X2')

	# Actual Plot w ColorMap 
    plt.scatter(x[0, :], x[1, :], c=y, s=40, cmap=plt.cm.Spectral)
    plt.show()


# Sample Visualization
plot(x, y)

