#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
ファイル common.py の概要
モジュール共通で利用する定数と変数の定義
"""

#-----------------------------------------------------------------------------#
# Constants
#-----------------------------------------------------------------------------#
# 状態
INITIAL_MODE = 0    # 初期状態
SEARCH_MODE  = 1    # 探索走行状態
FAST_MODE    = 2    # 最速走行状態
GOAL_MODE    = 3    # ゴール状態

# 方向
EAST  = 1
NORTH = 2
WEST  = 3
SOUTH = 4

# 距離センサ情報取得用
FRONT = 0     # 前方
LEFT  = 1     # 左方
RIGHT = 2     # 右方

# 初期状態
INITIAL_POSITION  = (0,0)
INITIAL_WALL_INFO = (0,0,0)
INITIAL_DIRECTION = NORTH

# ゴール座標
# GOAL_POSITIONS  = ( (3,3), (3,3) )
GOAL_POSITIONS  = ( (7,7), (7,7) )
# GOAL_POSITIONS = ( (7,7), (7,8), (8,7), (8,8) )
