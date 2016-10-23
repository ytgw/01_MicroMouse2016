# -*- coding: utf-8 -*-
"""
ファイル usageExampleOfAction の概要
action.pyの使用例を記載
"""

import action

# 角度と距離の設定例
angle = 0
distance = 0.5

# 前と左右のセンサ値の設定例
# 0を正常状態として，負の値が壁に近く，正の値が壁に遠いとする
lengthF = 0
lengthL = 0
lengthR = 0
    
while True:
    # iMoveの出力:0→実行終了，1→実行中
    # 初期実行以外も常に呼び出す必要あり(初期実行命令以外は無視されるように実装予定)
    if action.iMove(angle,distance,lengthF,lengthL,lengthR) == 1:
        print action.GLOBAL_TIME
        # 終了処理を実装していないので，簡易的に0.001秒後に動作終了とした        
    else:
        break
    
