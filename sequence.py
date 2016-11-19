# coding: UTF-8

#-------------------------------------------------------------------------------
# Name:        sequence
# Purpose:      sequence all functions
#
# Author:      kitawaki
#
# Created:     31/08/2016
# Copyright:   (c) kitawki 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import middleware as mw
import recognition as rcg
import action as act
import stop as stop
import userutility as utl
import copy
#-----------------------------------------------------------------------------#
# Declation                                                                  #
#-----------------------------------------------------------------------------#
#タクトスイッチ押した判定用のカウンタ
swstatecnt = [0,0,0]

# 壁情報のビット表現
RIGHT  = 0b00000001
TOP    = 0b00000010
LEFT   = 0b00000100
BOTTOM = 0b00001000

# 距離情報取得用
FRONT_DIRECTION     = 0             # 前方
LEFT_DIRECTION      = 1             # 左方
RIGHT_DIRECTION     = 2             # 右方

ROTATERIGHT = -88
ROTATELEFT = 88
ROTATEOPPOSIT = 175

#-----------------------------------------------------------------------------#
# Functions                                                                  #
#-----------------------------------------------------------------------------#

def selectmode():
    mode = [0,0,0]
    # タクトスイッチのスイッチ取得
    swstate = mw.switchstate()
    # 走行モード
    for swno in [0, 1, 2]:
        if swstate[swno] == 0:
            swstatecnt[swno] += 1
            stop.stop()
        elif swstate[swno] == 1:
            if swstatecnt[swno] >= 3:
                mode[swno] = 1
                stop.stop()
            swstatecnt[swno] = 0
##    print swstate
##    print swstatecnt
    return mode

def change_the_world(mydirection, local_wallinfo):
    global_wallinfo = 0
    #print "mydirectionC=",mydirection
    #print "local_wallinfoC",local_wallinfo
    bit0 = ( local_wallinfo & 0b0001 ) >> 0
    bit1 = ( local_wallinfo & 0b0010 ) >> 1
    bit2 = ( local_wallinfo & 0b0100 ) >> 2 
    bit3 = ( local_wallinfo & 0b1000 ) >> 3
    
    if mydirection == RIGHT:
        new0 = bit1
        new1 = bit2
        new2 = bit3
        new3 = bit0
    elif mydirection == TOP:
        new0 = bit0
        new1 = bit1
        new2 = bit2
        new3 = bit3
    elif mydirection == LEFT:
        new0 = bit3
        new1 = bit0
        new2 = bit1
        new3 = bit2
    elif mydirection == BOTTOM:
        new0 = bit2
        new1 = bit3
        new2 = bit0
        new3 = bit1

    global_wallinfo = global_wallinfo | ( new0 << 0 )
    global_wallinfo = global_wallinfo | ( new1 << 1 )
    global_wallinfo = global_wallinfo | ( new2 << 2 )
    global_wallinfo = global_wallinfo | ( new3 << 3 )
    return global_wallinfo


def main():
    maze = utl.Maze()
    mypos = [ 0, 0 ]
    nextpos = [ 0, 0 ]
    POS_X, POS_Y = 0, 1
    safe_counter = 0
    newWallInfo = 0
    next_direction = TOP
    mydirection = TOP
    distance = [0, 0, 0]
    step = 1
    # 走行モードの初期化(0=探索,1=最短)
    runnninngmode = 0
    while(1):
        # 車輪回転中フラグの初期化(0:停止、1：回転中)
        flgMoving = 0
        # ゴール到達フラグの初期化(0:未達、1：到達)
        flgGoal = 0
        #状態ステータス(0：停止、1:開始、2:走行中)
        runstatus = 0
        mode = [0,0,0]
        mode = selectmode()
##        print mode[0]
        # タクトスイッチ0が押されたら
        if mode[0] == 1:
            # LED0を点灯
            mw.led([1,0,0,0])
            # 走行モードを探索に設定
            runnninngmode = 0

        # タクトスイッチ1が押されたら
        if mode[1] == 1:
            # LED1を点灯
            mw.led([0,1,0,0])
            # 走行モードを最短に設定
            runnninngmode = 1

        # タクトスイッチ2が押されたら
        if mode[2] == 1:
            # LED2を点灯
            mw.led([0,0,1,0])
            # 状態ステータスを開始に設定
            runstatus = 1
        
##        print "runnninngmode=", runnninngmode
        # 走行の1回目だけは0.5マス前進する
        # 走行モードが探索の場合
        while(runstatus == 1):
            # 走行モードが最短の場合
            if runnninngmode == 1:
                # 足立方で探索2
                maze.adachi_2nd_run()
                
            next_direction = TOP
            mydirection = TOP
            nextpos = [ 0, 0 ]
            # 現在位置を1順前の次の位置に設定
            mypos = copy.copy(nextpos)
            # 初期位置では必ずRIGHT & LEFT & BOTTOMに壁がある
            newWallInfo = 13
            maze.set_wallinfo( mypos, newWallInfo)
            # 0.5マス前進
            half_step()
            # 状態ステータスを走行中に設定
            runstatus = 2
            nextpos = (0,1)

        # 状態ステータスが開始or走行中
        while(runstatus == 2):
            # 走行モードが探索の場合
            if runnninngmode == 0 or runnninngmode == 1:
                distance = rcg.get_distance()
                
                distance[FRONT_DIRECTION] = -1
##                distance[LEFT_DIRECTION] = -1
##                distance[RIGHT_DIRECTION] = -1
   
                if act.is_running():
                    act.keep_order(distance[FRONT_DIRECTION],distance[LEFT_DIRECTION],distance[RIGHT_DIRECTION])
                else:
                    if mypos in utl.goal:
                        # 周囲の壁情報の取得
                        newWallInfo = rcg.check_wall()
                        newWallInfo = change_the_world(mydirection, newWallInfo)
                        # 地図に壁情報を書き込み
                        maze.set_wallinfo( mypos, newWallInfo)
                        if runnninngmode == 0:
                            # 0.5マス前進
                            half_step()
                            print "1st Goal!!"
                        elif runnninngmode == 1:
                            # 0.5マス前進
                            half_step()
                            print "2nd Goal!!"
                        # ゴールに到着
                        flgGoal = 1
                        # LED3を点灯
                        mw.led([0,0,0,1])
                    else:
                        # 現在位置を1順前の次の位置に設定
                        mypos = nextpos
                        # 現在位置の表示
                        #print "mypos = ",mypos
                        if runnninngmode == 0:
                            # 周囲の壁情報の取得
                            newWallInfo = rcg.check_wall()
                            # 周囲の壁情報の表示
                            #print "local wallinfo  = ", newWallInfo

                            newWallInfo = change_the_world(mydirection, newWallInfo)
                            #print "global wallinfo = ", newWallInfo                            
                            # 地図に壁情報を書き込み
                            maze.set_wallinfo( mypos, newWallInfo)
                            # 足立方で探索
                            maze.adachi()
                            #maze.display_distinfo()
                        elif runnninngmode == 1:
                            print "Adachi2"
##                            # 足立方で探索2
##                            maze.adachi_2nd_run()
                        # 次の移動位置を取得
                        nextpos = maze.get_nextpos( mypos )
                        # 次の移動方向を取得
                        next_direction = maze.get_nextaction( mypos, nextpos )
                        #print "mydirection=",mydirection
                        #print "next_direction=",next_direction
                        if runnninngmode == 1:
                            step = 1
                            origin_next_direction = next_direction
                            pre_nextpos = nextpos
                            while next_direction == mydirection:
                                pre_nextpos = nextpos
                                # 現在位置を1順前の次の位置に設定
                                mypos = nextpos
                                # 次の移動位置を取得
                                nextpos = maze.get_nextpos( mypos )
                                # 次の移動方向を取得
                                next_direction = maze.get_nextaction( mypos, nextpos)
                                step += 1
                                #print "pre_nextpospre_pypos=",pre_nextpos
                                #print "step=",step
                            if step > 1:
                                step -= 1
                                next_direction = origin_next_direction
                                nextpos = pre_nextpos
                        print "-------------------------"
     
                        # 次に進むべき方向と今自分が向いている方向から、回転角度を求め、move()を実行
                        if next_direction == 0:
                            stop.stop()
                        elif next_direction == RIGHT:
                            if mydirection == RIGHT:
                                act.go_straight(step,distance[FRONT_DIRECTION],distance[LEFT_DIRECTION],distance[RIGHT_DIRECTION])
                            elif mydirection == TOP:
                                go_rotate_go(0.5,ROTATERIGHT)
                            elif mydirection == LEFT:
                                go_rotate_go(0.5,ROTATEOPPOSIT)
                            elif mydirection == BOTTOM:
                                go_rotate_go(0.5,ROTATELEFT)
                        elif next_direction == TOP:
                            if mydirection == RIGHT:
                                go_rotate_go(0.5,ROTATELEFT)
                            elif mydirection == TOP:
                                act.go_straight(step,distance[FRONT_DIRECTION],distance[LEFT_DIRECTION],distance[RIGHT_DIRECTION])
                            elif mydirection == LEFT:
                                go_rotate_go(0.5,ROTATERIGHT)
                            elif mydirection == BOTTOM:
                                go_rotate_go(0.5,ROTATEOPPOSIT)
                        elif next_direction == LEFT:
                            if mydirection == RIGHT:
                                go_rotate_go(0.5,ROTATEOPPOSIT)
                            elif mydirection == TOP:
                                go_rotate_go(0.5,ROTATELEFT)
                            elif mydirection == LEFT:
                                act.go_straight(step,distance[FRONT_DIRECTION],distance[LEFT_DIRECTION],distance[RIGHT_DIRECTION])
                            elif mydirection == BOTTOM:
                                go_rotate_go(0.5,ROTATERIGHT)
                        elif next_direction == BOTTOM:
                            if mydirection == RIGHT:
                                go_rotate_go(0.5,ROTATERIGHT)
                            elif mydirection == TOP:
                                go_rotate_go(0.5,ROTATEOPPOSIT)
                            elif mydirection == LEFT:
                                go_rotate_go(0.5,ROTATELEFT)
                            elif mydirection == BOTTOM:
                                act.go_straight(step,distance[FRONT_DIRECTION],distance[LEFT_DIRECTION],distance[RIGHT_DIRECTION])

                        if next_direction == 0:
                            mydirection = mydirection
                        else:
                            mydirection = next_direction

                swstate = mw.switchstate()
                # タクトスイッチ1が押されたら
                if swstate[1] == 0:
                    # LED3を点灯
                    mw.led([0,0,0,1])
                    flgGoal = 1

                # ゴールに到着したら
                if flgGoal == 1:
                #if flgMoving == 0:
                    # 状態ステータスを停止に設定
                    runstatus = 0
                    stop.stop()
##                    print "End"
                else:
                    # 状態ステータスを走行中に設定
                    runstatus = 2


#--------------------------------------------------------------#
# 直進走行+回転走行+直進走行関数
#--------------------------------------------------------------#
def go_rotate_go(block_distance,degree_angle):
    '''
    回転走行関数rotateの概要
    入力:角度指令[°]
    出力:動作有無フラグ(Trueのとき動作中，Falseのとき停止中)
    '''
    # 変数の宣言
    distance = [0, 0, 0]
    local_is_running = False
    sequenceCount = 0
    #cnt = 0
    while sequenceCount < 4:
##        print "sequenceCount="
##        print sequenceCount
    
        distance = rcg.get_distance()
        distance[FRONT_DIRECTION] = distance[FRONT_DIRECTION]
        
        local_is_running = act.is_running()
        if local_is_running == True:
            if sequenceCount != 2:
                act.keep_order(distance[FRONT_DIRECTION],distance[LEFT_DIRECTION],distance[RIGHT_DIRECTION])
                #cnt = 0
            else:
                act.rotate(degree_angle)
                #print cnt
                #cnt += 1
        else:
            sequenceCount += 1
            if sequenceCount == 1:
                act.go_straight(block_distance,distance[FRONT_DIRECTION],distance[LEFT_DIRECTION],distance[RIGHT_DIRECTION])
        
            if sequenceCount == 2:
                act.rotate(degree_angle)

            if sequenceCount == 3:
                local_is_running = act.go_straight(block_distance,distance[FRONT_DIRECTION],distance[LEFT_DIRECTION],distance[RIGHT_DIRECTION])
    return False

#--------------------------------------------------------------#
#--------------------------------------------------------------#
def half_step():
    distance = rcg.get_distance()
    distance[FRONT_DIRECTION] = -1
##  distance[LEFT_DIRECTION] = -1
##  distance[RIGHT_DIRECTION] = -1
    # 0.5マス前進
    act.go_straight(0.60,distance[FRONT_DIRECTION],distance[LEFT_DIRECTION],distance[RIGHT_DIRECTION])
    # 0.5マス進み終わるまで待機
    while True:
        distance = rcg.get_distance()
        distance[FRONT_DIRECTION] = -1
        act.keep_order(distance[FRONT_DIRECTION],distance[LEFT_DIRECTION],distance[RIGHT_DIRECTION])
        if not(act.is_running()):
            break
    return True


if __name__ == '__main__':
    main()

