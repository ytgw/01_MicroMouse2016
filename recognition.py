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
LR_NO_CHECK_F_MIN_THRESHOLD = 0.06  # 左右判定不可領域閾値(前方)

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
GET_SENSOR_NUM  = 5                # センサ値取得回数

#距離補正[m]
correct_distance_L = 0
correct_distance_R = 0
correct_distance_FL = 0
correct_distance_FR = 0

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
    THRESHOLD = 3e-2 # [m]
    # 初期化
    distance = [0, 0, 0]

    distanceForCalibration = get_distance_for_calibration()
    distFL = distanceForCalibration[FRONT_L_SENSOR_NO]
    distFR = distanceForCalibration[FRONT_R_SENSOR_NO]
    distL = distanceForCalibration[LEFT_SENSOR_NO]
    distR = distanceForCalibration[RIGHT_SENSOR_NO]

    if distFL == -1:
        distance[common.FRONT] = distFR
    elif distFR == -1:
        distance[common.FRONT] = distFL
    elif abs(distFL-distFR) > THRESHOLD:
        distance[common.FRONT] = min(distFL,distFR)
    else:
        distance[common.FRONT] = (distFL+distFR)/2

    distance[common.LEFT] = distL
    distance[common.RIGHT] = distR


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

def get_distance_for_calibration():
    """ 距離[m]を取得
    """
    THRESHOLD = 7e-2;
    # 初期化
    distance = [0, 0, 0, 0]
    sensor_value = get_sensor_value()
    # センサ値->距離
    distance[FRONT_L_SENSOR_NO] = (521.58 * sensor_value[FRONT_L_SENSOR_NO]**(-0.672))/100 - correct_distance_FL
    distance[FRONT_R_SENSOR_NO] = (1035.1 * sensor_value[FRONT_R_SENSOR_NO]**(-0.857))/100 - correct_distance_FR
    distance[LEFT_SENSOR_NO] = (-0.043*math.log(1+sensor_value[LEFT_SENSOR_NO])+0.2976-correct_distance_L)
    distance[RIGHT_SENSOR_NO] = (-0.036*math.log(1+sensor_value[RIGHT_SENSOR_NO])+0.2713-correct_distance_R)

    if abs(correct_distance_FL) > THRESHOLD:
        distance[FRONT_L_SENSOR_NO] = -1
    if abs(correct_distance_FR) > THRESHOLD:
        distance[FRONT_R_SENSOR_NO] = -1
    if abs(correct_distance_L) > THRESHOLD:
        distance[LEFT_SENSOR_NO] = -1
    if abs(correct_distance_R) > THRESHOLD:
        distance[RIGHT_SENSOR_NO] = -1

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

def set_correct_distance():
    """左右距離を校正
    """
    global correct_distance_L,correct_distance_R,correct_distance_FL,correct_distance_FR
    # 中央に置いた際の左右の壁までの距離
    CENTRAL_SIDE_DISTANCE  = 3.4e-2
    CENTRAL_FRONT_DISTANCE = 11e-2

    correct_distance_L = 0
    correct_distance_R = 0
    correct_distance_FL = 0
    correct_distance_FR = 0

    distance = get_distance_for_calibration()

    print "--- start of set_correct_distance ---"
    distanceForPrint = (100*distance[LEFT_SENSOR_NO], 100*distance[FRONT_L_SENSOR_NO], 100*distance[FRONT_R_SENSOR_NO], 100*distance[RIGHT_SENSOR_NO])
    print "BEFORE distance (L,FL,FR,R) : (%.2f, %.2f, %.2f, %.2f) [cm]" % distanceForPrint

    correct_distance_L  = distance[LEFT_SENSOR_NO]    - CENTRAL_SIDE_DISTANCE
    correct_distance_R  = distance[RIGHT_SENSOR_NO]   - CENTRAL_SIDE_DISTANCE
    correct_distance_FL = distance[FRONT_L_SENSOR_NO] - CENTRAL_FRONT_DISTANCE
    correct_distance_FR = distance[FRONT_R_SENSOR_NO] - CENTRAL_FRONT_DISTANCE

    distance = get_distance_for_calibration()
    distanceForPrint = (100*distance[LEFT_SENSOR_NO], 100*distance[FRONT_L_SENSOR_NO], 100*distance[FRONT_R_SENSOR_NO], 100*distance[RIGHT_SENSOR_NO])
    print "AFTER  distance (L,FL,FR,R) : (%.2f, %.2f, %.2f, %.2f) [cm]" % distanceForPrint
    offsetForPrint = (100*correct_distance_L, 100*correct_distance_FL, 100*correct_distance_FR, 100*correct_distance_R)
    print "offset (L,FL,FR,R) : (%.2f, %.2f, %.2f, %.2f) [cm]" % offsetForPrint
    print "--- end of set_correct_distance ---"

#-----------------------------------------------------------------------------#
# Test
#-----------------------------------------------------------------------------#
def test_recognition():
    """ センサ値，距離，壁有無のチェックを実施しLEDを点灯する
    """
    sensorValue = get_sensor_value()
    sensorValueForPrint = (sensorValue[LEFT_SENSOR_NO], sensorValue[FRONT_L_SENSOR_NO], sensorValue[FRONT_R_SENSOR_NO], sensorValue[RIGHT_SENSOR_NO])
    print "sensorValue (L,FL,FR,R) : (%.2f, %.2f, %.2f, %.2f)" % sensorValueForPrint

    distance = get_distance_for_calibration()
    distanceForPrint = (100*distance[LEFT_SENSOR_NO], 100*distance[FRONT_L_SENSOR_NO], 100*distance[FRONT_R_SENSOR_NO], 100*distance[RIGHT_SENSOR_NO])
    print "distance (L,FL,FR,R) : (%.2f, %.2f, %.2f, %.2f) [cm]" % distanceForPrint

    sDist = get_distance()
    sDistForPrint = (100*sDist[common.LEFT], 100*sDist[common.FRONT], 100*sDist[common.RIGHT])
    print "distanceForSequence (L,F,R) : (%.2f, %.2f, %.2f) [cm]" % sDistForPrint

    wallInfo = check_wall_info()
    wallForPrint = (wallInfo[common.LEFT], wallInfo[common.FRONT], wallInfo[common.RIGHT])
    print "wall (L, F, R) :", wallForPrint
    print ""

if __name__ == '__main__':
    set_correct_distance()
    while True:
        test_recognition()
        time.sleep(1)
