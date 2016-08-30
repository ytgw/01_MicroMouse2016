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
    mypos = [ 0, 0 ]
    POS_X, POS_Y = 0, 1
    #utl.judge_shutdown()
    print " -- start!! -- "
    maze = utl.Maze()
    sim  = ms.MazeSim()
    data = sim.open_mazefile()
    for i in range(80):
        maze.set_wallinfo(mypos, data[mypos[POS_X]][mypos[POS_Y]])
        maze.adachi()
        mypos = maze.get_nextpos(mypos)
    maze.display_wallinfo()
    maze.display_distinfo()
    print " -- completed!! -- "
    
if __name__ == '__main__':
    main()