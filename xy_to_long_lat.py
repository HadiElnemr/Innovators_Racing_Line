import math
# from map import Position
import csv
import matplotlib.pyplot as plt
import numpy as np


# Convert x, y coordinates to latitude and longitude
def convert_x_y_to_long_lat(data, ref_lat=0, ref_lon=0):
    R = 6371000.0 # Earth's radius in meters

    # Convert reference latitude and longitude to radians
    ref_lat_rad = math.radians(ref_lat)
    ref_lon_rad = math.radians(ref_lon)

    # Calculate bearing and distance from x, y coordinates
    # bearing = math.atan2(data.y, data.x)
    bearing = math.atan2(data[1], data[0])
    distance = math.sqrt(data[0]**2 + data[1]**2)

    # Calculate latitude and longitude using spherical trigonometry
    lat_rad = math.asin(math.sin(ref_lat_rad) * math.cos(distance / R) + math.cos(ref_lat_rad) * math.sin(distance / R) * math.cos(bearing))
    lon_rad = ref_lon_rad + math.atan2(math.sin(bearing) * math.sin(distance / R) * math.cos(ref_lat_rad), math.cos(distance / R) - math.sin(ref_lat_rad) * math.sin(lat_rad))

    # Convert radians to degrees
    lat_deg = math.degrees(lat_rad)
    lon_deg = math.degrees(lon_rad)

    return [lon_deg, lat_deg]


# read csv file
def read_csv_file(file_name):
    xy_data = np.loadtxt(file_name, delimiter=',')
    long_lat_data = [convert_x_y_to_long_lat(data) for data in xy_data]
    plt.plot(*zip(*long_lat_data))
    print(np.array([long_lat_data[i][:]+[xy_data[i][2]] for i in range(len(long_lat_data))]))
    np.savetxt("racetraj_vel_3d_(shortest_path)_long_lat.csv", np.array([long_lat_data[i][:]+[xy_data[i][2]] for i in range(len(long_lat_data))]), delimiter=",", header=" longitude, latitude (or opposite), vx_mps")



read_csv_file('../global_racetrajectory_optimization/racetraj_vel_3d_(shortest_path).csv')
plt.show()