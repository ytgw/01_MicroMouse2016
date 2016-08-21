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
    utl.judge_shutdown()
    maze = utl.Maze()
    sim  = ms.MazeSim()
    data = sim.open_mazefile()
    maze.set_wallinfo( (2,3) , data[2][3] )
    maze.adachi()
    maze.display_wallinfo()
    maze.display_distinfo()
    print " -- completed!! -- "

if __name__ == '__main__':
    main()