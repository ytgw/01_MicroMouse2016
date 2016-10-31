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

import time
import math
import numpy as np
import middleware as mw
import recognition as rcg
import action as act
#-----------------------------------------------------------------------------#
# Declation                                                                  #
#-----------------------------------------------------------------------------#
#タクトスイッチの状態格納変数
swstate = [2,2,2]
#タクトスイッチ押した判定用のカウンタ
swstatecnt = [0,0,0]
#走行モードステータス択(0=探索,1=最短)
runnninngmode = 0

#-----------------------------------------------------------------------------#
# Functions                                                                  #
#-----------------------------------------------------------------------------#

def selectmode():
    mode = [0,0,0]
    # タクトスイッチのスイッチ取得
    swstate = mw.switchstate()
    # 走行モード
    for swno in [0, 1, 2]:
        if swstate[swno] == -1:
            swstatecnt[swno] += 1
        elif swstate[swno] == 0:
            if swstatecnt[swno] >= 20:
                mode[swno] = 1
            swstatecnt[swno] = 0
    print swstate
    print swstatecnt
    return mode

def main():
    # 車輪回転中フラグの初期化(0:停止、1：回転中)
    flgMoving = 0
    # ゴール到達フラグの初期化(0:未達、1：到達)
    flgGoal = 0
    while(1):
        #状態ステータス(0：停止、1:開始、2:走行中)
        runstatus = 0
        mode = [0,0,0]
        mode = selectmode()
        print mode[0]
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

        # 状態ステータスが開始or走行中
        while(runstatus != 0):

            # 走行モードが探索の場合
            if runnninngmode == 0:
                if flgMoving == 0:
                    # 正面に壁がある場合
                    if rcg.check_wall_front():
                        # 時計回りに90度
                        flgMoving = act.rotate(90)
                    # 正面に壁が無い場合
                    else:
                        # 1ブロック直進
                        flgMoving = act.go_straight(0.5,0.1,0.02,0.02)
                    # マップを更新

                # ゴールに到着したら
        ##            if goal():
                if flgGoal == 1:
                    # 状態ステータスを停止に設定
                    runstatus = 0
                else:
                    # 状態ステータスを走行中に設定
                    runstatus = 2
##            elif runnninngmode == 1:
                # 最短経路探索で移動先を選択
            print "End"
            break

if __name__ == '__main__':
    main()

