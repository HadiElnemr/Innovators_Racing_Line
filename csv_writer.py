import csv
from map import Position

def write_csv(csv_content):
    i = 0
    with open('my_track.csv', 'w') as file:
        writer = csv.writer(file)
        for row in csv_content:
            i = 1-i
            if i == 0:
                continue
            
            writer.writerow([
                round(row[0].x*100, 10),
                round(row[0].y*100, 10),
                round(row[1]*100000, 10),
                round(row[1]*100000, 10)
            ])
