# coding: utf-8

import move as mv
import recognition as rcg

SPACE = 0
WALL = 1

def migite_method():
    # 初期値
    illegal_counter = 0
    while( 1 ):
        chk_wall = rcg.check_wall_front()
        #chk_wall = WALL

        if chk_wall == SPACE :
            print 'space'
            mv.move( 0, 1 )
        else :
            print 'wall'
            illegal_counter = illegal_counter + 1
            if illegal_counter >= 10 :
                print 'turn left'
                mv.move( 90, 0 )
                illegal_counter = 0
                print illegal_counter
            else :
                print 'turn right'
                print illegal_counter
                mv.move( -90, 0 )

if __name__ == '__main__':
    migite_method()
