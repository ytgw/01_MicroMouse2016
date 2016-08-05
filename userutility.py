import os
import time
import middleware as mw
import numpy as np

#-----------------------------------------------------------------------------#
# Declataion                                                                  #
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
# Class                                                                       #
#-----------------------------------------------------------------------------#
class Maze:
    def __init__(self):
        N = 16
        self.map = np.array( [ ["0"] * N] * N )
        self.map[ 0, 0 ] = "s"
        self.map[ 0 : N ] = self.map[ N-1 : : -1 ]
    def display(self):
        print "maze_info = "
        print self.map
    def get_info(self):
        return self.map
    def update(self,new_map):
        self.map = new_map
        return map

#-----------------------------------------------------------------------------#
# Function                                                                  #
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