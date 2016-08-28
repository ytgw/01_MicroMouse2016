# coding: UTF-8
import numpy as np
import middleware as mw
import userutility as utl
import maze_simulator.maze_simulator as ms

#-----------------------------------------------------------------------------#
# Declataion                                                                  #
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
# Function                                                                      #
#-----------------------------------------------------------------------------#
def main():
    #utl.judge_shutdown()
    print " -- start!! -- "
    maze = utl.Maze()
    sim  = ms.MazeSim()
    data = sim.open_mazefile()
    for x in range(maze.N):
        for y in range(maze.N):
            maze.set_wallinfo( (x,y) , int(data[x][y]) )
    maze.adachi()
    maze.display_wallinfo()
    maze.display_distinfo()
    print " -- completed!! -- "

if __name__ == '__main__':
    main()