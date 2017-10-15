# coding: UTF-8

import time
import math
import numpy as np
import middleware as mw
import common

#-----------------------------------------------------------------------------#
# Declataion
#-----------------------------------------------------------------------------#
# 壁あり/なしの閾値[m]
FRONT_THRESHOLD = 0.15              # 閾値(前方)
LEFT_THRESHOLD  = 0.07              # 閾値(左方)
RIGHT_THRESHOLD = 0.07              # 閾値(右方)

# 壁距離換算の閾値[m]
F_NO_CHECK_F_MAX_THRESHOLD = 0.18   # 前判定不可領域閾値(前方)
LR_NO_CHECK_LR_MAX_THRESHOLD = 0.07 # 左右判定不可領域閾値(左右)
LR_NO_CHECK_F_MIN_THRESHOLD = 0.04  # 左右判定不可領域閾値(前方)

# センサ値取得用
FRONT_L_SENSOR_NO   = 3             # 前壁検出センサ(左)
FRONT_R_SENSOR_NO   = 0             # 前壁検出センサ(右)
LEFT_SENSOR_NO      = 2             # 左壁検出センサ
RIGHT_SENSOR_NO     = 1             # 右壁検出センサ
SENSOR_NUM          = 4             # センサ数

# LED点灯用
LED_OFF         = 0                 # LED消灯
LED_ON          = 1                 # LED点灯
EXEC_LED_NO     = 0                 # 実行中LED
LEFT_LED_NO     = 3                 # 左壁検出LED
FRONT_LED_NO    = 2                 # 前壁検出LED
RIGHT_LED_NO    = 1                 # 右壁検出LED

# フィルタ用
GET_SENSOR_NUM  = 10                # センサ値取得回数

#-----------------------------------------------------------------------------#
# Function
#-----------------------------------------------------------------------------#
def check_wall_info():
    # 初期化
    distance  = [0, 0, 0]
    wall_info = [0, 0, 0]
    # 距離取得
    distance = get_distance()
    # 壁ありなし判定
    if distance[common.FRONT] < FRONT_THRESHOLD and distance[common.FRONT] >= 0:
        wall_info[common.FRONT] = 1
    if distance[common.RIGHT] < RIGHT_THRESHOLD and distance[common.RIGHT] >= 0:
        wall_info[common.RIGHT] = 1
    if distance[common.LEFT] < LEFT_THRESHOLD and distance[common.LEFT] >= 0:
        wall_info[common.LEFT] = 1
    return wall_info

def get_distance():
    """ 距離[m]を取得
    """
    # 初期化
    distance = [0, 0, 0]
    sensor_value = get_sensor_value()
    # センサ値->距離
    distFL = (521.58 * sensor_value[FRONT_L_SENSOR_NO]**(-0.672))/100
    distFR= (1035.1 * sensor_value[FRONT_R_SENSOR_NO]**(-0.857))/100
    distance[common.FRONT] = (distFL+distFR)/2
    distance[common.LEFT]  = (-0.043*math.log(1+sensor_value[LEFT_SENSOR_NO])+0.2976+1.0e-2)
    distance[common.RIGHT] = (-0.036*math.log(1+sensor_value[RIGHT_SENSOR_NO])+0.2713-0.2e-2)

    # 左壁の距離検出なし条件
    if distance[common.LEFT]  > LR_NO_CHECK_LR_MAX_THRESHOLD or distance[common.FRONT] <= LR_NO_CHECK_F_MIN_THRESHOLD:
        distance[common.LEFT] = -1
    # 右壁の距離検出なし条件
    if distance[common.RIGHT] > LR_NO_CHECK_LR_MAX_THRESHOLD or distance[common.FRONT] <= LR_NO_CHECK_F_MIN_THRESHOLD:
        distance[common.RIGHT] = -1
    # 前壁の距離検出なし条件
    if distance[common.FRONT] > F_NO_CHECK_F_MAX_THRESHOLD:
        distance[common.FRONT] = -1

    return distance

def get_sensor_value():
    """ 距離センサより値を取得
    """
    # 初期化
    num = 0
    sensor_value = [0, 0, 0, 0]
    fl_buf = []
    fr_buf = []
    l_buf = []
    r_buf = []
    # 指定回数データ取得
    while num < GET_SENSOR_NUM:
        info = mw.sensorinfo()
        # センサ値が1未満の場合は距離出力時のエラー回避(logやゼロ割防止)のため1にする
        for sensor_num in range(0, SENSOR_NUM):
            if info[sensor_num] < 1:
                info[sensor_num] = 1
        # バッファに格納
        fl_buf.append(info[FRONT_L_SENSOR_NO])
        fr_buf.append(info[FRONT_R_SENSOR_NO])
        l_buf.append(info[LEFT_SENSOR_NO])
        r_buf.append(info[RIGHT_SENSOR_NO])
        num += 1;
    # 中央値取得
    sensor_value[FRONT_L_SENSOR_NO] = np.median(fl_buf)
    sensor_value[FRONT_R_SENSOR_NO] = np.median(fr_buf)
    sensor_value[LEFT_SENSOR_NO]    = np.median(l_buf)
    sensor_value[RIGHT_SENSOR_NO]   = np.median(r_buf)

    return sensor_value

def get_switch_state():
    """ スイッチ情報を取得
    """
    switch_state = mw.switchstate()
    return switch_state

#-----------------------------------------------------------------------------#
# Test
#-----------------------------------------------------------------------------#
def test_recognition():
    """ センサ値，距離，壁有無のチェックを実施しLEDを点灯する
    """
    #---------- センサ値のチェック ----------#
    sValue = get_sensor_value()
    print "sensor value (0:FR, 1:R, 2:L, 3:FL) : (%.1f, %.1f, %.1f, %,1f)" % tuple(sValue)

    #---------- センサ距離のチェック ----------#
    sDist = get_distance()
    sDistForPrint = (100*sDist[common.LEFT], 100*sDist[common.FRONT], 100*sDist[common.RIGHT])
    print "sensor distance (L,F,R) : (%.2f, %.2f, %.2f) [cm]" % sDistForPrint

    #---------- 壁の有無のチェック ----------#
    ledList = [0,0,0,0]
    wall = check_wall_info()
    print "wall (F, L, R) :", wall
    for i,x in wall:
        ledList[i] = x
    mw.led(ledList)

if __name__ == '__main__':
    while True:
        test_recognition()
        time.sleep(1)
