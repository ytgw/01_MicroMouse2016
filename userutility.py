import os
import time
import middleware as mw
import numpy as np

#-----------------------------------------------------------------------------#
# Declataion                                                                  #
#-----------------------------------------------------------------------------#
#    ( x  , y )
s  = ( 0  , 0 )
g1 = ( 11 , 4 )
g2 = ( 11 , 5 )
g3 = ( 12 , 4 )
g4 = ( 12 , 5 )
gr = ( 11 , 3 )
g1 = (  4 , 11 )
g2 = (  5 , 11 )
g3 = (  4 , 12 )
g4 = (  5 , 12 )
gr = (  3 , 11 )
RIGHT  = 0b00000001
TOP    = 0b00000010
LEFT   = 0b00000100
BOTTOM = 0b00001000

#-----------------------------------------------------------------------------#
# Class                                                                       #
#-----------------------------------------------------------------------------#
class Maze:
    def __init__(self):
        # wallinfo[ y ][ x ]
        self.N = 16
        self.wallinfo = np.array( [ [0] * self.N] * self.N )
        self.wallinfo[ s[1]  ][ s[0]  ] = 255
        self.wallinfo[ g1[1] ][ g1[0] ] = 0
        self.wallinfo[ g2[1] ][ g2[0] ] = 0
        self.wallinfo[ g3[1] ][ g3[0] ] = 0
        self.wallinfo[ g4[1] ][ g4[0] ] = 0
        self.wallinfo[ gr[1] ][ gr[0] ] = 0
        #self.wallinfo[ 0 : self.N ] = self.wallinfo[ self.N-1 : : -1 ]
        # distinfo[ y ][ x ]
        self.distinfo = np.array( [ [255] * self.N] * self.N )
        self.distinfo[ s[1]  ][ s[0]  ] = 255
        self.distinfo[ g1[1] ][ g1[0] ] = 0
        self.distinfo[ g2[1] ][ g2[0] ] = 0
        self.distinfo[ g3[1] ][ g3[0] ] = 0
        self.distinfo[ g4[1] ][ g4[0] ] = 0
        self.distinfo[ gr[1] ][ gr[0] ] = 1
        #self.wallinfo[ 0 : self.N ] = self.wallinfo[ self.N-1 : : -1 ]
    def get_wallinfo(self):
        return self.wallinfo
    def set_wallinfo(self,set_pos,new_wallinfo):
        self.wallinfo[ set_pos[1] ][ set_pos[0] ] &= ( 0b1110000 | new_wallinfo )
        self.wallinfo[ set_pos[1] ][ set_pos[0] ] &= ( 0b1110111 ) #search completed
    def get_distinfo(self):
        return self.distinfo
    def set_distinfo(self,set_pos,new_distinfo):
        self.distinfo[ set_pos[1] ][ set_pos[0] ]  = new_distinfo 
    def adachi(self,center):
        neighbors = self.neighbor_pos(center)
        if (self.wallinfo[ neighbors[ 0 ][ 0 ] ][ neighbors[ 0 ][ 1 ] ] & RIGHT ) != RIGHT:
            self.distinfo[ neighbors[ 0 ][ 0 ] ][ neighbors[ 0 ][ 1 ] ] = 1 + self.distinfo[ center[1] ][ center[0] ]
        if (self.wallinfo[ neighbors[ 1 ][ 0 ] ][ neighbors[ 1 ][ 1 ] ] & TOP ) != TOP:
            self.distinfo[ neighbors[ 1 ][ 0 ] ][ neighbors[ 1 ][ 1 ] ] = 1 + self.distinfo[ center[1] ][ center[0] ]
        if (self.wallinfo[ neighbors[ 2 ][ 0 ] ][ neighbors[ 2 ][ 1 ] ] & LEFT ) != LEFT:
            self.distinfo[ neighbors[ 2 ][ 0 ] ][ neighbors[ 2 ][ 1 ] ] = 1 + self.distinfo[ center[1] ][ center[0] ]
        if (self.wallinfo[ neighbors[ 3 ][ 0 ] ][ neighbors[ 3 ][ 1 ] ] & BOTTOM ) != BOTTOM:
            self.distinfo[ neighbors[ 3 ][ 0 ] ][ neighbors[ 3 ][ 1 ] ] = 1 + self.distinfo[ center[1] ][ center[0] ]
    def neighbor_pos(self,center):
        n_right   = ( center[1]     , center[0] + 1 )
        n_top     = ( center[1] + 1 , center[0]     )
        n_left    = ( center[1]     , center[0] - 1 )
        n_bottom  = ( center[1] - 1 , center[0]     )
        neighbors = [ n_right , n_top , n_left , n_bottom]
        return neighbors
        
    
#-----------------------------------------------------------------------------#
# Function                                                                    #
#-----------------------------------------------------------------------------#
def judge_shutdown():
    sw_st = mw.switch_state()
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

m = Maze()
print "wall_info = "
print m.get_wallinfo()
m.adachi(gr)
print "dist_info = "
print m.get_distinfo()