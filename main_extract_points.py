
from fastkml import kml, geometry
from matplotlib import pyplot as plt
from map import Position, Road
import math, plotting
from typing import List
import csv_writer

def convert_long_lat_to_x_y(data):
    # define the reference point (in this case, the first data point)
    ref_lat, ref_lon = 0, 0

    # convert latitude and longitude to radians
    lat_rad = math.radians(data.y)
    lon_rad = math.radians(data.x)

    # calculate the differences between each point and the reference point
    dx = math.cos(ref_lat) * math.sin(lat_rad) - math.sin(ref_lat) * math.cos(lat_rad) * math.cos(lon_rad - ref_lon)
    dy = math.sin(lon_rad - ref_lon) * math.cos(lat_rad)

    # convert differences to distances in meters using the Haversine formula
    R = 6371000.0 # Earth's radius in meters
    distances = R * math.sqrt(dx * dx + dy * dy)

    # assign the first data point as the origin
    x, y = [0], [0]

    # calculate x and y coordinates
    distance = distances
    bearing = math.atan2(dy, dx)
    # x.append(distance * math.cos(bearing))
    # y.append(distance * math.sin(bearing))
    return Position(distance * math.cos(bearing), distance * math.sin(bearing))

def parse_geometries(placemark:geometry):
        if hasattr(placemark, "geometry"):  # check if the placemark has a geometry or not
            # if isinstance(placemark.geometry, geometry.Point):
                # self.add_point(placemark)
            if isinstance(placemark.geometry, geometry.LineString):
                # print(placemark.geometry.coords)
                right_x, right_y = [], []
                left_x, left_y = [], []
                for idx,coordinate in enumerate(placemark.geometry.coords):
                    if idx > 223:
                        left_x.append(coordinate[0])
                        left_y.append(coordinate[1])    
                    else:
                        right_x.append(coordinate[0])
                        right_y.append(coordinate[1])
                
                # print('right x,y:', len(right_x), len(right_y))
                # print('left x,y:', len(left_x), len(left_y))
                # plt.plot(left_x,left_y)
                # plt.show()
                return left_x, left_y, right_x, right_y
            

def parse_placemarks(document):
    for feature in document:
        if isinstance(feature, kml.Placemark):
            return parse_geometries(feature)
        if isinstance(feature, kml.Folder):
            return parse_placemarks(list(feature.features()))
        if isinstance(feature, kml.Document):
           return parse_placemarks(list(feature.features()))
    
if __name__ == '__main__':
    kml_file = '/home/hadi/racing_line_optimisation/GUC/New Paul Armagnac Data.kml'
    k = kml.KML()
    with open(kml_file) as myfile:
        k.from_string(myfile.read().encode("utf-8"))

    left_x, left_y, right_x, right_y = parse_placemarks(list(k.features()))
    left_size = len(left_x)
    right_size = len(right_x)
    # print(left_size)
    # print(right_size)

    left_positions:List[Position] = []
    right_positions:List[Position] = []

    for i in range(left_size):
        left_positions.append(Position(left_x[i],left_y[i]))
    for i in range(right_size):
        right_positions.append(Position(right_x[i],right_y[i]))
    plotting.plot_positions(right_positions,left_positions)
    left_road = Road(left_positions[0], left_positions[1:], left_positions[0])
    right_road = Road(right_positions[0], right_positions[1:], right_positions[0])
    
    updated_left_points:List[Position] = []
    centre_points:List[Position] = []
    csv_content = []

    for position in right_positions:
        updated_left_points.append(left_road.get_closest_point(position)[0])

    # Get centre positions    
    for i in range(len(right_positions)):
        centre_points += [right_positions[i].get_centre_position(updated_left_points[i])]
    

    
    # scale y axis and x axis for all points
    scale_y = 1
    scale_x = 1
    
    for i in range(len(centre_points)):
        # max_x = max(max_x, centre_points[i].x)
        # min_x = min(min_x, centre_points[i].x)
        # max_y = max(max_y, centre_points[i].y)
        # min_y = min(min_y, centre_points[i].y)
        
        centre_points[i].y = centre_points[i].y * scale_y
        centre_points[i].x = centre_points[i].x * scale_x
        updated_left_points[i].y = updated_left_points[i].y * scale_y
        updated_left_points[i].x = updated_left_points[i].x * scale_x
        right_positions[i].y = right_positions[i].y * scale_y
        right_positions[i].x = right_positions[i].x * scale_x
    
    # CSV file writing
    
    csv_content.append("# x_m,y_m,w_tr_right_m,w_tr_left_m")

    for i in range(len(centre_points)):
        # if centre_points[i].get_distance(right_positions[i]) == 0:
        #     continue
        # csv_content.append((centre_points[i], centre_points[i].get_distance(right_positions[i])))
        centre = convert_long_lat_to_x_y(centre_points[i])
        right = convert_long_lat_to_x_y(right_road.get_closest_point(centre_points[i])[0])
        csv_content.append((centre, centre.get_distance(right)))
        # csv_content.append((centre_points[i], centre_points[i].get_distance(right_road.get_closest_point(centre_points[i])[0])))
    csv_writer.write_csv(csv_content)
    
    
    
    # max_x = 0
    # min_x = 0
    # max_y = 0
    # min_y = 0
    
    plotting.plot_positions(centre_points)
    # plotting.plot_positions(updated_left_points, right_positions, centre_points)
    plt.show()


