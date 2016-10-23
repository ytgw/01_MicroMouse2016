# -*- coding: utf-8 -*-
"""
ファイル action.py の概要
"""

import time
import math
import numpy as np
import middleware as mw

#--------------------------------------------------------------#
# グローバル変数の定義
#--------------------------------------------------------------#
GLOBAL_X = 1
GLOBAL_Y = 1
GLOBAL_PHI = 0

GLOBAL_TIME = 0
GLOBAL_OLD_CLOCK_TIME = time.clock()

GLOBAL_LEFT_SPEED = 0
GLOBAL_RIGHT_SPEED = 0
GLOBAL_RUN_FLAG = 0

#--------------------------------------------------------------#
# 関数本体
#--------------------------------------------------------------#
def iMove(angle,distance,lengthF,lengthL,lengthR):
    # グローバル変数の宣言
    global GLOBAL_X, GLOBAL_Y, GLOBAL_PHI
    global GLOBAL_TIME, GLOBAL_OLD_CLOCK_TIME
    global GLOBAL_LEFT_SPEED, GLOBAL_RIGHT_SPEED, GLOBAL_RUN_FLAG    
    
    # 定数の設定
    
    GLOBAL_TIME += time.clock() - GLOBAL_OLD_CLOCK_TIME
    GLOBAL_OLD_CLOCK_TIME = time.clock()
    
    if GLOBAL_RUN_FLAG == 0:
        # 初期呼び出し時の処理
        GLOBAL_RUN_FLAG = 1
        GLOBAL_TIME = 0
    else:
        # 初期呼び出し以外の処理
        GLOBAL_X += 1
    
    
    # timeの更新
    # 現在速度の取得
    # xy座標，phiの更新
    
    if GLOBAL_TIME > 0.001:
        GLOBAL_RUN_FLAG = 0
    
    return GLOBAL_RUN_FLAG

