import math
from typing import List 
import sys
LARGE_DISTANCE = 100 # Infinity compared to our map

# from constant import DEGTORAD, DISTLAT
"""
In-door positioning system (IPS):
source: https://cpm.embedded.rwth-aachen.de/doc/display/CLD/Indoor+Positioning+System

Floor coordinates:

x [0, 4.5],  y [0, 4]

              y                               
                                                         
              |                                           
              |                                           
              |                                           
               __________  (4.5, 4)
              |          |
              |          |
              |          |
              |          |
              |__________| _ _ _ _ _ x
            (0, 0)

"""

class Position:

    def __init__(self, x:float=0, y:float=0, max_safe_speed=None, roads:List['Road']=None, id:int=None):
        self.id = id
        self.x = x
        self.y = y
        self.roads = roads
        if roads == None:
            self.roads = []
        self.max_safe_speed = max_safe_speed
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Position):
            return self.x == __o.x and self.y == __o.y
        return False

    def __str__(self) -> str:
        if self.id==None:
            return f'x: {self.x} , y: {self.y}'
        return f'id: {self.id} , x: {self.x} , y: {self.y}'
            

    # get distance to other position using pythagoras
    def get_distance(self, p: 'Position'):
        return math.sqrt(self.get_distance_squared(p)) 
        #return sqrt((self.x - p.x) ** 2 + (self.y-p.y) ** 2)

    def is_equal(self, p:'Position'):
        return self.x == p.x and self.y == p.y

    def get_distance_squared(self, p:'Position'):
        ## The following is for a globe
        # mean_lat = (self.y + p.y) * DEGTORAD / 2
        # dx = DISTLAT * math.Cos(mean_lat) * (self.x - p.x)
        # dy = DISTLAT * (self.y - p.y)
        # return dx * dx + dy * dy
        ## The following is for a flat earth (CPM lab)
        return (self.x - p.x) ** 2 + (self.y-p.y) ** 2

    def dot(self, p: 'Position'):
        return self.x * p.x + self.y * p.y

    def add(self, p: 'Position'):
        return Position(self.x + p.x, self.y + p.y)

    def sub(self, p: 'Position'):
        return Position(self.x - p.x, self.y - p.y)

    def mul(self, f: float):
        return Position(self.x * f, self.y * f)
    
    def get_closest_on_line(self, a: 'Position', b: 'Position'): # Line ab is considered a line segment, so find the point on that segment
        ba = b.sub(a)   # b with respect to a
        ds = self.sub(a).dot(ba) / ba.dot(ba)     #   (p - a). ba  / ||ba||^2 
        # if point is outside the line segment, get the closest point on the line segment (end of line)
        if ds < 0 :
            ds = 0 # closest point is a
        elif ds > 1:
            ds = 1 # closest point is b
        return a.add(ba.mul(ds))
    
    def get_centre_position(self, p:'Position'):
        return Position(x=(self.x+p.x)/2, y=(self.y+p.y)/2)

class Road:
    def __init__(self, position_A:Position, positions:List[Position]=None, position_B:Position=None, id:int=None): 
        self.id = id
        self.position_A = position_A
        self.positions = positions
        if position_B == None:
            print("position_B should not be None")
            sys.exit(1)
        self.position_B = position_B

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Road):
            a_b = self.position_A == __o.position_A and self.position_B == __o.position_B or self.position_A == __o.position_B and self.position_B == __o.position_A
            if self.position_A == __o.position_A and self.position_B == __o.position_B and len(self.positions) == len(__o.positions):
                for i in range(len(self.positions)):
                    if self.positions[i] != __o.positions[i]:
                        return False
            else:
                return False
            return True
        return False

    def __str__(self) -> str:
        return f'({self.position_A}) ---> ({self.position_B})'



    def get_length(self):
        if self.positions == None:
            return self.position_A.get_distance(self.position_B)
        length = 0
        cur_pos = self.position_A
        for position in self.positions:
            length += cur_pos.get_distance(position)
            cur_pos = position
        length += cur_pos.get_distance(self.position_B)
        return length
    

    # get closest point on "curved" road to a given position
    def get_closest_point(self, position: 'Position'): 
        min = LARGE_DISTANCE
        closest_point = None
        if self.positions == None or len(self.positions) == 0:
            return position.get_closest_on_line(self.position_A, self.position_B), [self.position_A, self.position_B]
        cur_pos = self.position_A
        pos_AB = [cur_pos, None]
        # loop on position and create straight lines and get the closest on each line, compare then get closest
        for next_pos in self.positions:
            closest_on_line = position.get_closest_on_line(cur_pos, next_pos)
            dist = position.get_distance(closest_on_line)
            if min > dist:
                min = dist
                closest_point = closest_on_line
                pos_AB = [cur_pos, next_pos]
            cur_pos = next_pos
        
        closest_on_line = position.get_closest_on_line(cur_pos, self.position_B)
        dist = position.get_distance(closest_on_line)
        
        if min > dist:
            min = dist
            closest_point = closest_on_line
            pos_AB = [cur_pos, self.position_B]

        return closest_point, pos_AB # pos_AB are the positions enclosing the closest point
        
    def get_road_heading(self):
        h = math.atan2(self.position_B.y - self.position_A.y , self.position_B.x - self.position_A.x )
        if h < 0:
            return h + math.pi*2
        return h
    
class Map:
    def __init__(self, positions: List[Position], roads: List[Road]):
        self.positions: List[Position] = positions
        self.roads = roads

    def __str__(self) -> str:
        return f'View Map Data:\n\nPositions:\n{list_str(self.positions)}\n\nRoads:\n{list_str(self.roads)}'

# Generic function to print any type of lists with new lines between elements
def list_str(lst) -> str:
    br = '\n'
    return f"{br}".join([str(p) for p in [i for i in lst]]) 