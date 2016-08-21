#%pylab inline --no-import-all
import numpy as np
from pylab import *

#-----------------------------------------------------------------------------#
# Declation                                                                   #
#-----------------------------------------------------------------------------#
RIGHT  = 0b00000001
TOP    = 0b00000010
LEFT   = 0b00000100
BOTTOM = 0b00001000
DATA_PATH = "maze_simulator\data.txt"

#-----------------------------------------------------------------------------#
# Class                                                                       #
#-----------------------------------------------------------------------------#
class MazeSim:
    def __init__(self):
        self.N = 16
        self.simmap = np.empty( (0,self.N) )
    def open_mazefile(self):
        with open(DATA_PATH,"r") as f:
            while 1:
                l = f.readline()
                if l == '':
                       break
                self.simmap =np.vstack([self.simmap,l.rstrip().split(' ')])
        self.simmap[0:self.N] = self.simmap[self.N-1: : -1]
        return self.simmap
    def display_maze(self):
        figure(figsize=(6, 6))
        maze_range = (0.5,self.N+0.5)
        plt.xticks([i for i in range(0,self.N+1,1)])
        plt.yticks([i for i in range(0,self.N+1,1)])
        plt.xlim(maze_range)
        plt.ylim(maze_range)
        for i in range(self.N):
            for j in range(self.N):
                plt.plot((0.5,self.N + 0.5),(j + 0.5, j + 0.5),"c--")
                plt.plot((i + 0.5, i + 0.5),(0.5,self.N + 0.5),"c--")
        info = self.open_mazefile()
        for y in range(self.N-1):
            for x in range(self.N-1):
                if ( int(info[y][x]) & RIGHT ) == RIGHT:
                    axis_x = (x+1.5,x+1.5)
                    axis_y = (y+0.5,y+1.5)
                    plt.plot(axis_x,axis_y,"r-")
                if ( int(info[y][x]) & TOP ) == TOP:
                    axis_x = (x+0.5,x+1.5)
                    axis_y = (y+1.5,y+1.5)
                    plt.plot(axis_x,axis_y,"r-")
        plt.show()