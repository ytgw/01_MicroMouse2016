# coding: UTF-8
#%pylab inline --no-import-all
import numpy as np
#from pylab import *
from matplotlib import pyplot as plt
import copy

#-----------------------------------------------------------------------------#
# Declation
#-----------------------------------------------------------------------------#
POS_X = 0
POS_Y = 1
RIGHT  = 0b00000001
TOP    = 0b00000010
LEFT   = 0b00000100
BOTTOM = 0b00001000
DATA_PATH = "maze_simulator/data.txt"
#DATA_PATH = "data.txt"

#-----------------------------------------------------------------------------#
# Class
#-----------------------------------------------------------------------------#
class MazeSim:
    def __init__( self ):
        self.N = 16
        self.mypos_prev = [ 0, 0 ]
        tempinfo = np.array( [ [0] * self.N ] * self.N )
        maze_info = self.open_mazefile()
        for i in range( self.N ):
            for j in range( self.N ):
                tempinfo[ i ][ j ] = maze_info[ j ][ i ]
        maze_info = tempinfo
        plt.figure( figsize=( 6, 6 ) )
        plt.xticks([i for i in range( -1, self.N, 1 ) ] )
        plt.yticks([i for i in range( -1, self.N, 1 ) ] )
        maze_range = ( -0.5, self.N - 0.5 )
        plt.xlim( maze_range )
        plt.ylim( maze_range )
        for i in range( self.N ):
            for j in range( self.N ):
                plt.plot( ( -0.5, self.N - 0.5 ), ( j - 0.5, j - 0.5 ), "c--" )
                plt.plot( ( i - 0.5, i - 0.5 ), ( -0.5, self.N - 0.5 ), "c--" )
        for y in range( self.N-1 ):
            for x in range( self.N-1 ):
                if ( int( maze_info[y][x] ) & RIGHT ) == RIGHT:
                    axis_x = ( x + 0.5, x + 0.5 )
                    axis_y = ( y - 0.5, y + 0.5 )
                    plt.plot( axis_x, axis_y, "r-" )
                if ( int( maze_info[y][x]) & TOP ) == TOP:
                    axis_x = ( x - 0.5, x + 0.5 )
                    axis_y = ( y + 0.5, y + 0.5 )
                    plt.plot( axis_x, axis_y, "r-" )
    def open_mazefile( self ):
        simmap = np.empty( ( 0, self.N ) )
        with open( DATA_PATH, "r" ) as f:
            while 1:
                l = f.readline()
                if l == '':
                       break
                simmap =np.vstack( [ simmap, l.rstrip().split(' ') ] )
        simmap[ 0 : self.N ] = simmap[ self.N-1 : : -1 ]
        # utility.pyのset_wallinfoと配列の並びを揃える必要がある
        tempinfo = np.array( [ [0] * self.N ] * self.N )
        for i in range( self.N ):
            for j in range( self.N ):
                tempinfo[ i ][ j ] = simmap[ j ][ i ]
        simmap = tempinfo
        return simmap
    def display_maze( self, maze_info, mypos ):
        plt.scatter( self.mypos_prev[POS_X], self.mypos_prev[POS_Y], marker='o' , c = "w")
        plt.scatter( mypos[POS_X], mypos[POS_Y], marker='o', c = "r" )
        plt.pause( 0.01 )
        self.mypos_prev = copy.copy(mypos)

if __name__ == '__main__':
    print "start"
    mypos = [7,7]
    m = MazeSim()
    info = m.open_mazefile()
    for i in range(3):
        mypos[0] += i
        mypos[1] -= i
        m.display_maze( info, mypos)
