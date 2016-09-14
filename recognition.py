# coding: UTF-8

import time
import numpy as np
import middleware as mw

#-----------------------------------------------------------------------------#
# Declataion                                                                  #
#-----------------------------------------------------------------------------#
# センサ値取得用
FRONT_L_SENSOR_NO = 3   # 前壁検出センサ(左)
FRONT_R_SENSOR_NO = 0   # 前壁検出センサ(右)
LEFT_SENSOR_NO = 2      # 左壁検出センサ
RIGHT_SENSOR_NO = 1     # 右壁検出センサ

# LED点灯用
EXEC_LED_NO = 0         # 実行中LED
LEFT_LED_NO = 1         # 左壁検出LED
FRONT_LED_NO = 2        # 前壁検出LED
RIGHT_LED_NO = 3        # 右壁検出LED

# フィルタ用
GET_SENSOR_NUM = 10     # センサ値取得回数

# 壁あり/なしの閾値
FRONT_THRESHOLD = 895	# 閾値(前方)
LEFT_THRESHOLD = 800	# 閾値(左方)
RIGHT_THRESHOLD = 800	# 閾値(右方)

#-----------------------------------------------------------------------------#
# Function                                                                    #
#-----------------------------------------------------------------------------#
def check_wall_front():
    """ 距離センサ前方に壁があるかどうかチェックする
    """
    # 初期化
    num = 0
    fl_buf = []
    fr_buf = []
    # 指定回数データ取得
    while num < GET_SENSOR_NUM:
        info = mw.sensorinfo()
        fl_buf.append(info[FRONT_L_SENSOR_NO])
        fr_buf.append(info[FRONT_R_SENSOR_NO])
        num += 1;
    # 平均値取得
    average = (np.mean(fl_buf) + np.mean(fr_buf)) / 2
    print "Front_Ave =", average
    if average > FRONT_THRESHOLD:
        return 1	# 壁あり
    else:
        return 0	# 壁なし

def check_wall_left():
    """ 距離センサ左方に壁があるかどうかチェックする
    """
    # 初期化
    num = 0
    l_buf = []
    # 指定回数データ取得
    while num < GET_SENSOR_NUM:
        info = mw.sensorinfo()
        l_buf.append(info[LEFT_SENSOR_NO])
        num += 1;
    # 平均値取得
    average = np.mean(l_buf)
    print "Left_Ave =", average
    if average > LEFT_THRESHOLD:
        return 1	# 壁あり
    else:
        return 0	# 壁なし

def check_wall_right():
    """ 距離センサより右方に壁があるかどうかチェックする
    """
    # 初期化
    num = 0
    r_buf = []
    # 指定回数データ取得
    while num < GET_SENSOR_NUM:
        info = mw.sensorinfo()
        r_buf.append(info[RIGHT_SENSOR_NO])
        num += 1;
    # 平均値取得
    average = np.mean(r_buf)
    print "Right_Ave =", average
    if average > RIGHT_THRESHOLD:
        return 1	# 壁あり
    else:
        return 0	# 壁なし

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
	# LED点灯
        led_state[EXEC_LED_NO] = 1
	# 前壁チェック(壁あり:LED点灯)
        if check_wall_front() == 1:
            led_state[FRONT_LED_NO] = 1
        else:
            led_state[FRONT_LED_NO] = 0
	# 左壁チェック(壁あり:LED点灯)
        if check_wall_left() == 1:
            led_state[LEFT_LED_NO] = 1
        else:
            led_state[LEFT_LED_NO] = 0
        # 右壁チェック(壁あり:LED点灯)
        if check_wall_right() == 1:
            led_state[RIGHT_LED_NO] = 1
        else:
            led_state[RIGHT_LED_NO] = 0
        # LED設定
        mw.led(led_state)
        time.sleep(1)

if __name__ == '__main__':
    test_recognition()
    
