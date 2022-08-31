# Solution to a Differential Equations Problem as Created by Codex in the work- https://www.pnas.org/doi/10.1073/pnas.2123433119 
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np


x, y = sp.symbols("x y")

f1 = 2*x - y
f2 = x - 3*y

critical_points = sp.solve([f1, f2], [x, y])
print(f"Critical Points: {critical_points}")

x_range = np.linspace(-5, 5, 100)
y_range = np.linspace(-5, 5, 100)

x_mesh, y_mesh = np.meshgrid(x_range, y_range)

dx = 2*x_mesh - y_mesh
dy = x_mesh - 3*y_mesh


plt.streamplot(x_mesh, y_mesh, dx, dy)
plt.show()

