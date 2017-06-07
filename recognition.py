# coding: UTF-8

import time
import math 
import numpy as np
import middleware as mw

#-----------------------------------------------------------------------------#
# Declataion                                                                  #
#-----------------------------------------------------------------------------#
# 壁あり/なしの閾値[m]
FRONT_THRESHOLD = 0.15              # 閾値(前方)
LEFT_THRESHOLD  = 0.05              # 閾値(左方)
RIGHT_THRESHOLD = 0.05              # 閾値(右方)

# 壁接近の閾値[m]
FRONT_NEAR_THRESHOLD    = 0.01      # 閾値(前方)
LEFT_NEAR_THRESHOLD     = 0.01      # 閾値(左方)
RIGHT_NEAR_THRESHOLD    = 0.01      # 閾値(右方)

# 壁距離換算の閾値[m]
F_NO_CHECK_F_MAX_THRESHOLD = 0.18   # 前判定不可領域閾値(前方)
LR_NO_CHECK_LR_MAX_THRESHOLD = 0.06 # 左右判定不可領域閾値(左右)
LR_NO_CHECK_F_MIN_THRESHOLD = 0.05  # 左右判定不可領域閾値(前方)

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
def check_wall_front():
    """ 前方に壁があるかどうかチェックする
    """
    # 初期化
    distance = [0, 0, 0]
    # 距離取得
    distance = get_distance()
    # 壁ありなし判定
    if distance[FRONT_DIRECTION] < FRONT_THRESHOLD and distance[FRONT_DIRECTION] >= 0:
        return WALL_ON  # 壁あり
    else:
        return WALL_OFF # 壁なし

def check_wall_left():
    """ 左方に壁があるかどうかチェックする
    """
    # 初期化
    distance = [0, 0, 0]
    # 距離取得
    distance = get_distance()
    # 壁ありなし判定
    if distance[LEFT_DIRECTION] < LEFT_THRESHOLD and distance[LEFT_DIRECTION] >= 0:
        return WALL_ON  # 壁あり
    else:
        return WALL_OFF # 壁なし

def check_wall_right():
    """ 右方に壁があるかどうかチェックする
    """
    # 初期化
    distance = [0, 0, 0]
    # 距離取得
    distance = get_distance()
    # 壁ありなし判定
    if distance[RIGHT_DIRECTION] < RIGHT_THRESHOLD and distance[RIGHT_DIRECTION] >= 0:
        return WALL_ON  # 壁あり
    else:
        return WALL_OFF # 壁なし

def check_wall():
    """ 壁があるかどうかチェックする
    """
    # 初期化
    distance = [0, 0, 0]
    wall = 0
    # 距離取得
    distance = get_distance()
    # 壁ありなし判定
    if distance[FRONT_DIRECTION] < FRONT_THRESHOLD and distance[FRONT_DIRECTION] >= 0:
        wall |= TOP_BIT
    if distance[RIGHT_DIRECTION] < RIGHT_THRESHOLD and distance[RIGHT_DIRECTION] >= 0:
        wall |= RIGHT_BIT
    if distance[LEFT_DIRECTION] < LEFT_THRESHOLD and distance[LEFT_DIRECTION] >= 0:
        wall |= LEFT_BIT
    return wall         

def check_wall_near():
    """ 左右壁の接近チェックする
    """
    # 初期化
    distance = [0, 0, 0]
    # 距離取得
    distance = get_distance()
    # 壁接近判定
    if distance[LEFT_DIRECTION] < LEFT_NEAR_THRESHOLD:
        return WALL_LEFT_NEAR
    elif distance[RIGHT_DIRECTION] < RIGHT_NEAR_THRESHOLD:
        return WALL_RIGHT_NEAR
    else:
        return WALL_NO_NEAR

def get_distance():
    """ 距離[m]を取得
    """
    # 初期化
    distance = [0, 0, 0]
    sensor_value = get_sensor_value()
    # センサ値->距離
    distance[FRONT_DIRECTION] = (-5.538*math.log(sensor_value[FRONT_DIRECTION])+43.786) / 100
    distance[LEFT_DIRECTION] = (1e-5*sensor_value[LEFT_DIRECTION]**2-0.0173*sensor_value[LEFT_DIRECTION]+8.5815) / 100
    distance[RIGHT_DIRECTION] = (4e-6*sensor_value[RIGHT_DIRECTION]**2-0.0106*sensor_value[RIGHT_DIRECTION]+8.4801) / 100
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
    sensor_value = [0, 0, 0]
    f_buf = []
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
        f_buf.append((info[FRONT_L_SENSOR_NO]+info[FRONT_R_SENSOR_NO])/2)
        l_buf.append(info[LEFT_SENSOR_NO])
        r_buf.append(info[RIGHT_SENSOR_NO])
        num += 1;
    # 平均値取得
    sensor_value[FRONT_DIRECTION] = np.median(f_buf)
    sensor_value[LEFT_DIRECTION] = np.median(l_buf)
    sensor_value[RIGHT_DIRECTION] = np.median(r_buf)

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
    while True:
        num += 1;
        print "----------"
        print "LOOP =",num
        print "----------"
        # センサ値取得
        sensor_value = get_sensor_value()
        # 距離取得
        distance = get_distance()
        print "Front =", sensor_value[FRONT_DIRECTION],"|",distance[FRONT_DIRECTION]
        print "Left  =", sensor_value[LEFT_DIRECTION],"|",distance[LEFT_DIRECTION]
        print "Right =", sensor_value[RIGHT_DIRECTION],"|",distance[RIGHT_DIRECTION]
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
        print "----------"    
        # LED設定
        mw.led(led_state)
        time.sleep(1)

if __name__ == '__main__':
    test_recognition()
    

