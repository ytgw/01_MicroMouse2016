import os
import time
import middleware as mw
import numpy as np

#-----------------------------------------------------------------------------#
# Declataion                                                                  #
#-----------------------------------------------------------------------------#
#    ( x  , y )
start = ( 0  , 0 )
goal  = ( (  4 , 11 ) , (  5 , 11 ) ,  (  4 , 12 ) , (  5 , 12 ) )
route = (  3 , 11 )
RIGHT  = 0b00000001
TOP    = 0b00000010
LEFT   = 0b00000100
BOTTOM = 0b00001000
POS_X  = 0
POS_Y  = 1

#-----------------------------------------------------------------------------#
# Class                                                                       #
#-----------------------------------------------------------------------------#
class Maze:
    def __init__(self):
        # wallinfo[ y ][ x ]
        self.N = 16
        self.minstep = 1
        self.wallinfo = np.array( [ [0] * self.N] * self.N )
        self.wallinfo[ start[ POS_X ]  ][ start[ POS_Y ]  ] = 13
        for pos in goal:
            self.wallinfo[ pos[ POS_X ] ][ pos[ POS_Y ] ] = 255
        self.wallinfo[ route[ POS_X ] ][ route[ POS_Y ] ] = 0
        # distinfo[ y ][ x ]
        self.distinfo = np.array( [ [255] * self.N] * self.N )
        self.distinfo[ start[ POS_X ]  ][ start[ POS_Y ]  ] = 255
        for pos in goal:
            self.distinfo[ pos[ POS_X ] ][ pos[ POS_Y ] ] = 255
        self.distinfo[ route[ POS_X ] ][ route[ POS_Y ] ] = 1
    def get_wallinfo(self):
        return self.wallinfo
    def set_wallinfo(self,set_pos,new_wallinfo):
        self.wallinfo[ set_pos[ POS_X ] ][ set_pos[ POS_Y ] ] &= ( 0b1110000 | int(new_wallinfo) )
        self.wallinfo[ set_pos[ POS_X ] ][ set_pos[ POS_Y ] ] &= ( 0b1110111 ) #search completed
    def display_wallinfo(self):
        self.wallinfo = rev_array(self.wallinfo, self.N)
        print "wallinfo = "
        print self.wallinfo
    def get_distinfo(self):
        return self.distinfo
    def set_distinfo(self,set_pos,new_distinfo):
        self.distinfo[ set_pos[0] ][ set_pos[ POS_Y ] ]  = new_distinfo
    def display_distinfo(self):
        self.distinfo = rev_array(self.distinfo, self.N)
        print "distinfo = "
        print self.distinfo
    def adachi(self):
        step = self.minstep
        flag = True
        while flag == True:
            for x in range(self.N):
                for y in range(self.N):
                    if self.distinfo[ x ][ y ] == step:
                        cntr =( x , y )
                        if cntr == start:
                            flag = False
                        nghbrs = self.neighbor_pos(cntr)
                        if (self.wallinfo[ cntr[ POS_X ] ][cntr[ POS_Y ] ] & RIGHT ) != RIGHT:
                            if self.distinfo[ nghbrs[ 0 ][ POS_X ] ][ nghbrs[ 0 ][ POS_Y ] ] > self.distinfo[ cntr[ POS_X ] ][ cntr[ POS_Y ] ]:
                                self.distinfo[ nghbrs[ 0 ][ POS_X ] ][ nghbrs[ 0 ][ POS_Y ] ] = 1 + self.distinfo[ cntr[ POS_X ] ][ cntr[ POS_Y ] ]
                        if (self.wallinfo[ cntr[ POS_X ] ][ cntr[ POS_Y ] ] & TOP ) != TOP:
                            if self.distinfo[ nghbrs[ 1 ][ POS_X ] ][ nghbrs[ 1 ][ POS_Y ] ] > self.distinfo[ cntr[ POS_X ] ][ cntr[ POS_Y ] ]:                            
                                self.distinfo[ nghbrs[ 1 ][ POS_X ] ][ nghbrs[ 1 ][ POS_Y ] ] = 1 + self.distinfo[ cntr[ POS_X ] ][ cntr[ POS_Y ] ]
                        if (self.wallinfo[ cntr[ POS_X ] ][ cntr[ POS_Y ] ] & LEFT ) != LEFT:
                            if self.distinfo[ nghbrs[ 2 ][ POS_X ] ][ nghbrs[ 2 ][ POS_Y ] ] > self.distinfo[ cntr[ POS_X ] ][ cntr[ POS_Y ] ]:
                                self.distinfo[ nghbrs[ 2 ][ POS_X ] ][ nghbrs[ 2 ][ POS_Y ] ] = 1 + self.distinfo[ cntr[ POS_X ] ][ cntr[ POS_Y ] ]
                        if (self.wallinfo[ cntr[ POS_X ] ][ cntr[ POS_Y ] ] & BOTTOM ) != BOTTOM:
                            if self.distinfo[ nghbrs[ 3 ][ POS_X ] ][ nghbrs[ 3 ][ POS_Y ] ] > self.distinfo[ cntr[ POS_X ] ][ cntr[ POS_Y ] ]:
                                self.distinfo[ nghbrs[ 3 ][ POS_X ] ][ nghbrs[ 3 ][ POS_Y ] ] = 1 + self.distinfo[ cntr[ POS_X ] ][ cntr[ POS_Y ] ]
            step += 1
    def neighbor_pos(self,center):
        n_right   = ( center[ POS_X ] + 1 , center[ POS_Y ]     )
        n_top     = ( center[ POS_X ]     , center[ POS_Y ] + 1 )
        n_left    = ( center[ POS_X ] - 1 , center[ POS_Y ]     )
        n_bottom  = ( center[ POS_X ]     , center[ POS_Y ] - 1 )
        neighbors = [ n_right , n_top , n_left , n_bottom ]
        for i,chk in enumerate(neighbors):
            if ( chk[ POS_X ] >= self.N ) or ( chk[ POS_Y ] >= self.N ):
                neighbors[i] = center
            elif ( chk[ POS_X ] <  0 ) or ( chk[ POS_Y ] < 0 ):
                neighbors[ i ] = center
        return neighbors

#-----------------------------------------------------------------------------#
# Function                                                                    #
#-----------------------------------------------------------------------------#
def rev_array(array,size):
    tempinfo = np.array( [ [0] * size] * size )
    for i in range(size):
        for j in range(size):
            tempinfo[ i ][ j ] = array[ j ][ i ]
    tempinfo[ 0 : size ] = tempinfo[ size-1 : : -1 ]
    revarray = tempinfo
    return revarray

def judge_shutdown():
    sw_st = mw.switchstate()
    if sw_st[0] == 1:
        # wait 1sec
        time.sleep(1)
        sw_st = mw.switch_state()
        if sw_st[0] == 1:
            # buzz 400Hz sound for 1sec
            mw.buzzer(400)
            time.sleep(1)
            # shutdown
            os.system("/sbin/shutdown -h now")
        else:
            ret = "switch[0] = ON->OFF"
    else:
        ret = "switch[0] = OFF->OFF"
    return ret