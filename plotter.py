import matplotlib.pyplot as plt
import numpy as np

# Create a 2D grid
grid_size = 10
x = np.arange(grid_size)
y = np.arange(grid_size)

# Create a meshgrid from x and y
X, Y = np.meshgrid(x, y)

# # Flatten the meshgrid coordinates
# x_flat = X.flatten()
# y_flat = Y.flatten()
#
# # Plot the grid
# plt.scatter(x_flat, y_flat, marker='o', color='blue')

dots_x = [2, 5, 7]
dots_y = [3, 6, 8]

plt.scatter(dots_x, dots_y, marker='o', color='red')

# Customize the plot
plt.title('Average Fitness Over Generations Of The Genetic Algorithm')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.grid(False)
plt.legend()

# Show the plot
plt.show()
