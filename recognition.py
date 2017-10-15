# coding: UTF-8

import time
import math 
import numpy as np
import middleware as mw
import common

#-----------------------------------------------------------------------------#
# Declataion                                                                  #
#-----------------------------------------------------------------------------#
# 壁あり/なしの閾値[m]
FRONT_THRESHOLD = 0.15              # 閾値(前方)
##LEFT_THRESHOLD  = 0.05              # 閾値(左方)
LEFT_THRESHOLD  = 0.07              # 閾値(左方)
##RIGHT_THRESHOLD = 0.05              # 閾値(右方)
RIGHT_THRESHOLD = 0.07              # 閾値(右方)

# 壁接近の閾値[m]
FRONT_NEAR_THRESHOLD    = 0.01      # 閾値(前方)
LEFT_NEAR_THRESHOLD     = 0.01      # 閾値(左方)
RIGHT_NEAR_THRESHOLD    = 0.01      # 閾値(右方)

# 壁距離換算の閾値[m]
F_NO_CHECK_F_MAX_THRESHOLD = 0.18   # 前判定不可領域閾値(前方)
LR_NO_CHECK_LR_MAX_THRESHOLD = 0.07 # 左右判定不可領域閾値(左右)
LR_NO_CHECK_F_MIN_THRESHOLD = 0.04  # 左右判定不可領域閾値(前方)

# 判定結果
WALL_OFF = 0                        # 壁あり
WALL_ON  = 1                        # 壁なし

WALL_NO_NEAR    = 0                 # 壁接近なし
WALL_LEFT_NEAR  = 1                 # 左壁接近
WALL_RIGHT_NEAR = 2                 # 右壁接近

# 壁ありなし情報取得用
RIGHT_BIT   = 0b00000001            # 右壁情報(1bit目)
TOP_BIT     = 0b00000010            # 前壁情報(2bit目)
LEFT_BIT    = 0b00000100            # 左壁情報(3bit目)

# 距離情報取得用
FRONT_DIRECTION     = 0             # 前方
LEFT_DIRECTION      = 1             # 左方
RIGHT_DIRECTION     = 2             # 右方

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
# Function                                                                    #
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
    # print "distance from rcg.check_wall_info:",  tuple(distance)
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
    distance[FRONT_DIRECTION] = (distFL+distFR)/2
    distance[LEFT_DIRECTION] = (-0.043*math.log(1+sensor_value[LEFT_DIRECTION])+0.2976+1.0e-2)
    distance[RIGHT_DIRECTION] = (-0.036*math.log(1+sensor_value[RIGHT_DIRECTION])+0.2713-0.2e-2)
    # 左壁の距離検出なし条件
    if distance[LEFT_DIRECTION] > LR_NO_CHECK_LR_MAX_THRESHOLD or distance[FRONT_DIRECTION] <= LR_NO_CHECK_F_MIN_THRESHOLD:
        distance[LEFT_DIRECTION] = -1
    # 右壁の距離検出なし条件
    if distance[RIGHT_DIRECTION] >LR_NO_CHECK_LR_MAX_THRESHOLD or distance[FRONT_DIRECTION] <= LR_NO_CHECK_F_MIN_THRESHOLD:
        distance[RIGHT_DIRECTION] = -1
    # 前壁の距離検出なし条件
    if distance[FRONT_DIRECTION] > F_NO_CHECK_F_MAX_THRESHOLD:
        distance[FRONT_DIRECTION] = -1
                            
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
        # センサ値がマイナスの場合は0にする
        for sensor_num in range(0, SENSOR_NUM):
            if info[sensor_num] < 0:
                info[sensor_num] = 0.001
        # バッファに格納
        fl_buf.append(info[FRONT_L_SENSOR_NO])
        fr_buf.append(info[FRONT_R_SENSOR_NO])
        l_buf.append(info[LEFT_SENSOR_NO])
        r_buf.append(info[RIGHT_SENSOR_NO])
        num += 1;
    # 中央値取得
    sensor_value[FRONT_L_SENSOR_NO] = np.median(fl_buf)+1
    sensor_value[FRONT_R_SENSOR_NO] = np.median(fr_buf)+1
    sensor_value[LEFT_DIRECTION] = np.median(l_buf)+1
    sensor_value[RIGHT_DIRECTION] = np.median(r_buf)+1

    return sensor_value

def get_switch_state():
    """ スイッチ情報を取得
    """
    switch_state = mw.switchstate()
    return switch_state
    
#-----------------------------------------------------------------------------#
# Test                                                                        #
#-----------------------------------------------------------------------------#
def test_recognition():
    """ 壁あり/なしチェックを実施しLEDを点灯する 
    """
    # 初期化
    led_state = [0,0,0,0]
    num = 0
    # 初期化
    num = 0
    f_buf = []
    l_buf = []
    r_buf = []
    f_buf_d = []
    l_buf_d= []
    r_buf_d = []
    sensor_value_out = [0,0,0]
    distance_out = [0,0,0]
    # センサ値取得
    sensor_value = get_sensor_value()
    # 距離取得
    distance = get_distance()
    # 指定回数データ取得
    while num < GET_SENSOR_NUM:
        # バッファに格納
        f_buf.append(sensor_value[FRONT_DIRECTION])
        l_buf.append(sensor_value[LEFT_DIRECTION] )
        r_buf.append(sensor_value[RIGHT_DIRECTION])
        f_buf_d.append(distance[FRONT_DIRECTION])
        l_buf_d.append(distance[LEFT_DIRECTION] )
        r_buf_d.append(distance[RIGHT_DIRECTION])
        num += 1;
    # 中央値取得
    sensor_value_out[FRONT_DIRECTION] = np.median(f_buf)
    sensor_value_out[LEFT_DIRECTION] = np.median(l_buf)
    sensor_value_out[RIGHT_DIRECTION] = np.median(r_buf)
    distance_out[FRONT_DIRECTION] = np.median(f_buf_d)
    distance_out[LEFT_DIRECTION] = np.median(l_buf_d)
    distance_out[RIGHT_DIRECTION] = np.median(r_buf_d)
    # 出力
    print "Front =", sensor_value_out[FRONT_DIRECTION],"|",distance_out[FRONT_DIRECTION]
    print "Left  =", sensor_value_out[LEFT_DIRECTION],"|",distance_out[LEFT_DIRECTION]
    print "Right =", sensor_value_out[RIGHT_DIRECTION],"|",distance_out[RIGHT_DIRECTION]

    # LED点灯
    led_state[EXEC_LED_NO] = LED_ON
    # 前壁チェック(壁あり:LED点灯)
    if check_wall_front() == WALL_ON:
        led_state[FRONT_LED_NO] = LED_ON
    else:
        led_state[FRONT_LED_NO] = LED_OFF
    # 左壁チェック(壁あり:LED点灯)
    if check_wall_left() == WALL_ON:
        led_state[LEFT_LED_NO] = LED_ON
    else:
        led_state[LEFT_LED_NO] = LED_OFF
    # 右壁チェック(壁あり:LED点灯)
    if check_wall_right() == WALL_ON:
        led_state[RIGHT_LED_NO] = LED_ON
    else:
        led_state[RIGHT_LED_NO] = LED_OFF

if __name__ == '__main__':
    while True:
        print "wall (F, L, R) :",
        print check_wall_info()
        # time.sleep(1)
        sDist = get_distance()
        sDistForPrint = (100*sDist[common.LEFT], 100*sDist[common.FRONT], 100*sDist[common.RIGHT])
        print "distance (L,F,R) : (%.2f, %.2f, %.2f) [cm]" % sDistForPrint
        time.sleep(1)
