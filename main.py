# coding: UTF-8
import numpy as np
import middleware as mw
import userutility as utl
import maze_simulator.maze_simulator as ms

#-----------------------------------------------------------------------------#
# Function                                                                    #
#-----------------------------------------------------------------------------#
def first_run():
    mypos = [ 0, 0 ]
    POS_X, POS_Y = 0, 1
    safe_counter = 0
    sim  = ms.MazeSim()
    data = sim.open_mazefile()
    maze = utl.Maze() 
    while( 1 ):
        sim.display_maze( data, mypos )
        maze.set_wallinfo( mypos, data[ mypos[POS_X] ][ mypos[POS_Y] ] )
        maze.adachi()
        mypos = maze.get_nextpos( mypos, 2 )
        if mypos in utl.goal:
            print "1st Goal!!"
            break
        safe_counter += 1
        if safe_counter >= 100:
            break
    maze.display_wallinfo()
    maze.display_distinfo()

def second_run():
    mypos = [ 0, 0 ]
    POS_X, POS_Y = 0, 1
    safe_counter = 0 
    maze = utl.Maze()
    sim  = ms.MazeSim()
    data = sim.open_mazefile()
    while( 1 ):
        #sim.display_maze(data, mypos)
        maze.set_wallinfo( mypos, data[ mypos[POS_X] ][ mypos[POS_Y] ] )
        maze.adachi()
        mypos = maze.get_nextpos( mypos, 3 )
        if mypos in utl.goal:
            print "2th Goal!!"
            break
        safe_counter += 1
        if safe_counter >= 100:
            break

def main():
    print " -- start!! -- "
    first_run()
    print " -- re-start!! --"
    second_run()
    print " -- completed!! -- "
    
if __name__ == '__main__':
    main()