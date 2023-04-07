import numpy as np
import matplotlib.pyplot as plt

# Load the CSV data
data = np.loadtxt('/home/hadi/racing_line_optimisation/global_racetrajectory_optimization/inputs/tracks/scaled_data.csv', delimiter=',')

# Extract x and y coordinates of centerline
x_center = data[:, 0]
y_center = data[:, 1]

# Extract road width data
w_tr_right = data[:, 2]
w_tr_left = data[:, 3]

# Plot the centerline
plt.plot(x_center, y_center, color='black')

# Fill in the area to the right of the centerline
plt.fill_between(x_center, y_center-w_tr_right/2, y_center+w_tr_right/2,
                 color='gray', alpha=0.5)

# Fill in the area to the left of the centerline
plt.fill_between(x_center, y_center-w_tr_left/2, y_center+w_tr_left/2,
                 color='gray', alpha=0.5)

# Add labels and title
plt.xlabel('x_m')
plt.ylabel('y_m')
plt.title('Road centerline with width data')

# Show the plot
plt.show()
