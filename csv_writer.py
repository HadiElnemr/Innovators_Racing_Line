import csv
from map import Position
import numpy as np

def write_csv(csv_content):
    i = 0
    with open('../global_racetrajectory_optimization/inputs/tracks/my_track.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(csv_content.pop(0).split(','))
        count = 0
        i = count
        for row in csv_content:
            # i = 1-i
            # if i == 0:
            #     continue
            if i != 0:
                i-=1
                continue
            
            writer.writerow([
                round(row[0].x, 100),
                round(row[0].y, 100),
                round(row[1], 100),
                round(row[1], 100)
            ])

            i = count
    
# if __name__ == "__main__":
#     ref_file = 'inputs/tracks/modena_2019.csv'
#     ref_data = np.loadtxt(ref_file, delimiter=',')

#     # Get min and max values for x, y, and road width
#     # ref_min = np.min(ref_data[:, [0, 1, 2, 3]], axis=0)
#     # ref_max = np.max(ref_data[:, [0, 1, 2, 3]], axis=0)



#     data_file = 'inputs/tracks/my_track.csv'
#     data = np.loadtxt(data_file, delimiter=',')
    
#     ref_min = np.min(data[:, [0, 1, 2, 3]], axis=0)
#     ref_max = np.max(data[:, [0, 1, 2, 3]], axis=0)

#     # Separate the x, y, w_tr_right_m, and w_tr_left_m columns
#     x = data[:, 0]
#     y = data[:, 1]
#     w_tr_right = data[:, 2]
#     w_tr_left = data[:, 3]

#     # Scale the x, y, and road width values
#     x_scaled = (x - ref_min[0]) / (ref_max[0] - ref_min[0])
#     y_scaled = (y - ref_min[1]) / (ref_max[1] - ref_min[1])
    
#     w_tr_right_scaled = (w_tr_right - ref_min[2] + 1) / (ref_max[2] - ref_min[2])
#     w_tr_left_scaled = (w_tr_left - ref_min[3] + 1) / (ref_max[3] - ref_min[3])
    
#     # w_tr_right_scaled = w_tr_right/w_tr_right * 2
#     # w_tr_left_scaled = w_tr_left/w_tr_left * 2


#     # Combine the scaled x, y, w_tr_right_m, and w_tr_left_m columns into a single array
#     scaled_data = np.column_stack((x_scaled, y_scaled, w_tr_right_scaled, w_tr_left_scaled))

#     scaled_file = 'inputs/tracks/scaled_data.csv'
#     with open(scaled_file, 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerows(scaled_data)