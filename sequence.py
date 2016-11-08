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
import stop as stop
import usageExampleOfAction as ueoa
#-----------------------------------------------------------------------------#
# Declation                                                                  #
#-----------------------------------------------------------------------------#
#タクトスイッチ押した判定用のカウンタ
swstatecnt = [0,0,0]
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
        elif swstate[swno] == 1:
            if swstatecnt[swno] >= 3:
                mode[swno] = 1
            swstatecnt[swno] = 0
    print swstate
    print swstatecnt
    return mode

def main():
    while(1):
        # 車輪回転中フラグの初期化(0:停止、1：回転中)
        flgMoving = 0
        # ゴール到達フラグの初期化(0:未達、1：到達)
        flgGoal = 0
        # 走行モードの初期化(0=探索,1=最短)
        runnninngmode = 0
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
                ueoa.tmp_function_for_group_meeting()
                mode = selectmode()
                # タクトスイッチ1が押されたら
                if mode[1] == 1:
                    # LED1を点灯
                    mw.led([0,1,0,0])
                    flgGoal = 1
                # マップを更新

                # ゴールに到着したら
        ##      if goal():
                if flgGoal == 1:
                #if flgMoving == 0:
                    # 状態ステータスを停止に設定
                    runstatus = 0
                    stop.stop()
                    print "End"
                else:
                    # 状態ステータスを走行中に設定
                    runstatus = 2
##            elif runnninngmode == 1:
                # 最短経路探索で移動先を選択
            

if __name__ == '__main__':
    main()

