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
#
#-------------------------------------------------------------------------------

import recognition as rcg
import action as act
import stop as stop
import userutility as utl
import common
import time
import os

#-----------------------------------------------------------------------------#
# Declation                                                                   #
#-----------------------------------------------------------------------------#
# グローバル変数
global_maze      = utl.Maze()                   # 迷路インスタンス
global_position  = common.INITIAL_POSITION      # 現在座標
global_direction = common.INITIAL_DIRECTION     # 現在の方向

#-----------------------------------------------------------------------------#
# Functions                                                                   #
#-----------------------------------------------------------------------------#
def main():
    '''
    マイクロマウスマシンの起動プログラム関数
    '''
    global global_position, global_direction

    print "Main function is called"
    nextMode = common.INITIAL_MODE

    while True:
        #----- 状態の遷移 -----#
        presentMode = nextMode
        nextMode = selectMode(presentMode, global_position, common.GOAL_POSITIONS)

        #----- デバッグ用表示 -----#
        if presentMode != nextMode:
            print "-----------------------------------------------------------------"
            if nextMode == common.INITIAL_MODE:
                act.led([1,0,0,0])
                print "Mode changed to INITIAL MODE"
            elif nextMode == common.SEARCH_MODE:
                act.led([0,1,0,0])
                global_position  = common.INITIAL_POSITION
                global_direction = common.INITIAL_DIRECTION
                print "Mode changed to SEARCH MODE"
            elif nextMode == common.FAST_MODE:
                act.led([0,0,1,0])
                global_position  = common.INITIAL_POSITION
                global_direction = common.INITIAL_DIRECTION
                print "Mode changed to FAST MODE"
            elif nextMode == common.GOAL_MODE:
                act.led([0,0,0,1])
                print "Mode changed to GOAL MODE"
            else:
                act.led([1,1,1,1])
                print "Mode changed to UNDEFINED MODE"

        #----- 状態ごとの動作切り替え -----#
        if nextMode == common.INITIAL_MODE:
            initialModeFunction()
        elif (nextMode == common.SEARCH_MODE) or (nextMode == common.FAST_MODE):
            print "---------- START MOVE MODE FUNCTION ----------"
            # moveModeFunctionは座標移動が完了するまで処理を専有する関数
            moveModeFunction(nextMode)
            print "END"
        elif nextMode == common.GOAL_MODE:
            goalModeFunction()
        else:
            act.led([1,1,1,1])
            print "You are in undefined mode"


def selectMode(presentMode, presentPosition, goalPositions):
    '''
    状態遷移関数
    入力:現在の状態，現在の位置，ゴール位置のリスト
    出力:遷移後の状態
    タクトスイッチ0を押すと初期状態へ遷移
    タクトスイッチ1を押すと初期状態のときは探索走行状態へ遷移するが，
    ゴール状態のときは最速走行状態へ遷移し，それ以外の状態では遷移なし
    タクトスイッチ2を長押しするとブザーを鳴らした後にシャットダウン
    探索状態もしくは最速走行状態時に，現在座標がゴール座標に含まれていたら
    ゴール状態に遷移
    '''
    mode = presentMode

    # タクトスイッチのスイッチ取得
    swState = rcg.get_switch_state()

    # スイッチ情報による遷移
    if swState[0] == 0:
        mode = common.INITIAL_MODE
    elif swState[1] == 0:
        if presentMode == common.INITIAL_MODE:
            mode = common.SEARCH_MODE
        elif presentMode == common.GOAL_MODE:
            mode = common.FAST_MODE
    elif swState[2] == 0:
        stop.stop()
        time.sleep(3)
        swState = rcg.get_switch_state()
        if swState[2] == 0:
            act.led([0,0,0,0])
            act.buzzerWithTime(2093,1)
            os.system("/sbin/shutdown -h now")

    # ゴール到達による遷移
    if (presentMode in [common.SEARCH_MODE, common.FAST_MODE]) \
    and (presentPosition in goalPositions):
        mode = common.GOAL_MODE

    return mode


def initialModeFunction():
    '''
    初期状態の動作関数
    '''
    global global_maze, global_position, global_direction
    # モータへの停止命令
    stop.stop()
    # LEDの表示
    act.led([1,0,0,0])
    # 迷路インスタンスのリセット
    global_maze = utl.Maze()
    # 座標のリセット
    global_position = common.INITIAL_POSITION
    # 方向のリセット
    global_direction = common.INITIAL_DIRECTION
    act.global_mode = act.GLOBAL_STOP_MODE


def moveModeFunction(mode):
    '''
    走行状態の動作関数
    入力:探索状態or最速走行状態
    '''
    global global_maze, global_position, global_direction, global_onoff
    RESIDUAL_DISTANCE = 0.55    # [block]
    ZERO_DISTANCE = 0           # [block]

    if global_position == common.INITIAL_POSITION:
        global_direction = common.INITIAL_DIRECTION
        wallInfoFromRcg  = common.INITIAL_WALL_INFO
        # 1block直進し[0,1]に移動
        act.startStraight(1)
        global_position = (0,1)

    #----- 区画の境界まで直進 -----#
    keepStraightUntilThreshold(RESIDUAL_DISTANCE)


    #----- 足立法からの情報取得 -----#
    print "Present",
    printPositionDirection(global_position, global_direction)

    # 壁情報の取得は探索状態のみ
    if mode == common.SEARCH_MODE:
        wallInfoFromRcg  = rcg.check_wall_info()
        wallForPrint = (wallInfoFromRcg[common.LEFT], wallInfoFromRcg[common.FRONT], wallInfoFromRcg[common.RIGHT])
        print "Wall Info From Rcg (Left, Front, Right) : ", wallForPrint
        # 壁情報のセット
        global_maze.set_wall_info(global_position, global_direction, wallInfoFromRcg)
        # print "after set wall info"

    # 座標と方向の更新，次行動(回転→直進)の取得
    (global_position, global_direction, nextAngle, nextDist) \
    = global_maze.get_next_info(global_position, global_direction, mode)
    print "(Next Angle, Next Distance) : ", (nextAngle, nextDist)
    print "Next",
    printPositionDirection(global_position, global_direction)

    #----- ゴール時と回転時と直進時で動作切り替え -----#
    if nextAngle != 0:
        # 区画中心まで直進
        # print "before keepStraightUntilThreshold"
        # keepStraightUntilThresholdで暴走する時がある
        keepStraightUntilThreshold(ZERO_DISTANCE)
        # print "after keepStraightUntilThreshold"
        # 回転動作
        act.rotateUntilLast(nextAngle-5)
        # print "after act.rotateUntilLast"
        # 直進開始
        act.startStraight(nextDist)
        # print "after act.startStraight"
    else:
        # 直進距離指令に追加
        act.addDistanceOrder(nextDist)

    if global_position in common.GOAL_POSITIONS:
        # 区画中心まで直進
        keepStraightUntilThreshold(ZERO_DISTANCE)
        global_maze.display_distinfo()
        global_maze.display_wallinfo()
        print "You reached goal"


def keepStraightUntilThreshold(threshold):
    '''
    指定の残り距離以下になるまで直進する関数
    入力:残り距離
    '''
    length = rcg.get_distance()     # 距離センサ情報の取得
    length[common.FRONT] = -1       # 前方向補正の無効化
    resDist = act.keepStraight(length[common.FRONT],length[common.LEFT],length[common.RIGHT])

    if threshold == 0:
        # minResDist = 0
        # maxDistance = 0
        while act.is_running():
            length = rcg.get_distance()     # 距離センサ情報の取得
            length[common.FRONT] = -1       # 前方向補正の無効化
            resDist = act.keepStraight(length[common.FRONT],length[common.LEFT],length[common.RIGHT])
            # if minResDist > resDist:
                # minResDist = resDist
            # if maxDistance < act.global_distance:
                # maxDistance = act.global_distance
                # print "order : %d [cm]" % (100*act.global_distance_order), " / maxDistance : %d [cm]" % (100*maxDistance)
        # print "minResDist %.1f [block]" % minResDist
        # distanceの更新値がおかしくて暴走する時がある
    else:
        while resDist > threshold:
            length = rcg.get_distance()     # 距離センサ情報の取得
            length[common.FRONT] = -1       # 前方向補正の無効化
            resDist = act.keepStraight(length[common.FRONT],length[common.LEFT],length[common.RIGHT])


def goalModeFunction():
    '''
    ゴール状態の動作関数
    '''
    # モータへの停止命令
    stop.stop()


def printPositionDirection(position, direction):
    '''
    座標と位置の表示関数
    入力:座標，方向
    出力:なし
    '''
    positionStr = ( "(%2d, %2d)" % (position[0], position[1]) )

    if direction == common.EAST:
        directionStr = "East"
    elif direction == common.NORTH:
        directionStr = "North"
    elif direction == common.WEST:
        directionStr = "West"
    elif direction == common.SOUTH:
        directionStr = "South"
    else:
        directionStr = "undefined direction"

    print "position : " + positionStr + "  /  direction : " + directionStr


#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    main()
