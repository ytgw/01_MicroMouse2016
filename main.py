import numpy as np
import middleware as mw
import userutility as utl

#-----------------------------------------------------------------------------#
# Declataion                                                                  #
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
# Function                                                                      #
#-----------------------------------------------------------------------------#
def main():
    utl.judge_shutdown()
    maze = utl.Maze()
    maze_info = maze.get_info()
    maze.display()
    maze_info[0][0] = "g"
    maze.update( maze_info )
    maze.display()

if __name__ == '__main__':
    main()