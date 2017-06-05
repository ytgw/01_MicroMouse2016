# coding: UTF-8
import userutility as utl
import maze_simulator.maze_simulator as ms

#-----------------------------------------------------------------------------#
# Function                                                                    #
#-----------------------------------------------------------------------------#
class mode:
    def __init__( self ):
        self.sim  = ms.MazeSim()
        self.data = ms.MazeSim().open_mazefile()
        self.maze = utl.Maze()        
    def first_run( self ):
        mypos = [ 0, 0 ]
        POS_X, POS_Y = 0, 1
        safe_counter = 0
        self.sim.display_maze( self.data, mypos )
        while( 1 ):
            self.maze.set_wallinfo( mypos, self.data[ mypos[POS_X] ][ mypos[POS_Y] ] )
            self.maze.adachi()
            mypos = self.maze.get_nextpos( mypos )
            self.sim.display_maze( self.data, mypos )
            if mypos in utl.goal:
                print "1st Goal!!"
                break
            safe_counter += 1
            if safe_counter >= 100:
                break
        self.maze.display_wallinfo()
        self.maze.display_distinfo()
    def second_run( self ):
        mypos = [ 0, 0 ]
        POS_X, POS_Y = 0, 1
        safe_counter = 0 
        self.sim.display_maze( self.data, mypos )
        while( 1 ):
            self.maze.set_wallinfo( mypos, self.data[ mypos[POS_X] ][ mypos[POS_Y] ] )
            self.maze.adachi_2nd_run()
            mypos = self.maze.get_nextpos( mypos )
            self.sim.display_maze( self.data, mypos )
            if mypos in utl.goal:
                print "2th Goal!!"
                break
            safe_counter += 1
            if safe_counter >= 80:
                distinfo = self.maze.get_distinfo()
                break
        self.maze.display_wallinfo()
        self.maze.display_distinfo()

def adachi_run():
    md = mode()
    print " -- start!! -- "
    md.first_run()
    print " -- re-start!! --"
    md.second_run()
    print " -- completed!! -- "
    
if __name__ == '__main__':
    adachi_run()
