from matplotlib import pyplot as plt
from map import Position, Road
from typing import List

def plot_positions(positions:List[Position], positions_2:List[Position]=None, positions_3:List[Position]=None):
    x = []
    y = []
    for pos in positions:
        print(pos)
        x.append(pos.x)
        y.append(pos.y)
    plt.plot(x,y)
    if positions_2 is not None:
        plot_positions(positions_2)
    if positions_3 is not None:
        plot_positions(positions_3)
    # plt.show()
