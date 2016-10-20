# coding: UTF-8

import time
import numpy as np
import middleware as mw

#-----------------------------------------------------------------------------#
# Declataion                                                                  #
#-----------------------------------------------------------------------------#
# 壁あり/なしの閾値
FRONT_THRESHOLD = 400	    # 閾値(前方)
LEFT_THRESHOLD = 204	    # 閾値(左方)
RIGHT_THRESHOLD = 346	    # 閾値(右方)

# 壁接近の閾値
FRONT_NEAR_THRESHOLD = 800  # 閾値(前方)
LEFT_NEAR_THRESHOLD = 408   # 閾値(左方)
RIGHT_NEAR_THRESHOLD = 692  # 閾値(右方)

# 判定結果
WALL_OFF = 0                # 壁あり
WALL_ON = 1                 # 壁なし

WALL_NO_NEAR = 0            # 壁接近なし
WALL_LEFT_NEAR = 1          # 左壁接近
WALL_RIGHT_NEAR = 2         # 右壁接近


# 距離情報取得用
FRONT_DIRECTION = 0         # 前方
LEFT_DIRECTION = 1          # 左方
RIGHT_DIRECTION = 2         # 右方

# センサ値取得用
FRONT_L_SENSOR_NO = 3       # 前壁検出センサ(左)
FRONT_R_SENSOR_NO = 0       # 前壁検出センサ(右)
LEFT_SENSOR_NO = 2          # 左壁検出センサ
RIGHT_SENSOR_NO = 1         # 右壁検出センサ

# LED点灯用
LED_OFF = 0                 # LED消灯
LED_ON = 1                  # LED点灯
EXEC_LED_NO = 0             # 実行中LED
LEFT_LED_NO = 3             # 左壁検出LED
FRONT_LED_NO = 2            # 前壁検出LED
RIGHT_LED_NO = 1            # 右壁検出LED

# フィルタ用
GET_SENSOR_NUM = 10         # センサ値取得回数

#-----------------------------------------------------------------------------#
# Function                                                                    #
#-----------------------------------------------------------------------------#
def check_wall_front():
    """ 距離センサ前方に壁があるかどうかチェックする
    """
    # 初期化
    value = [0, 0, 0]
    # センサ値取得
    value = get_sensor_value()
    print "Front_Ave =", value[FRONT_DIRECTION]
    # 壁ありなし判定
    if value[FRONT_DIRECTION] > FRONT_THRESHOLD:
        return WALL_ON	# 壁あり
    else:
        return WALL_OFF	# 壁なし

def check_wall_left():
    """ 距離センサ左方に壁があるかどうかチェックする
    """
    # 初期化
    value = [0, 0, 0]
    # センサ値取得
    value = get_sensor_value()
    print "Left_Ave =", value[LEFT_DIRECTION]
    # 壁ありなし判定
    if value[LEFT_DIRECTION] > LEFT_THRESHOLD:
        return WALL_ON	# 壁あり
    else:
        return WALL_OFF	# 壁なし

def check_wall_right():
    """ 距離センサより右方に壁があるかどうかチェックする
    """
    # 初期化
    value = [0, 0, 0]
    # センサ値取得
    value = get_sensor_value()
    print "Right_Ave =", value[RIGHT_DIRECTION]
    # 壁ありなし判定
    if value[RIGHT_DIRECTION] > RIGHT_THRESHOLD:
        return WALL_ON	# 壁あり
    else:
        return WALL_OFF	# 壁なし

def check_wall_near():
    """ 左右壁の接近チェックする
    """
    # 初期化
    value = [0, 0, 0]
    # センサ値取得
    value = get_sensor_value()
    # 壁接近判定
    if value[LEFT_DIRECTION] > LEFT_NEAR_THRESHOLD:
        return WALL_LEFT_NEAR
    elif value[RIGHT_DIRECTION] > RIGHT_NEAR_THRESHOLD:
        return WALL_RIGHT_NEAR
    else:
        return WALL_NO_NEAR
    
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
        f_buf.append((info[FRONT_L_SENSOR_NO]+info[FRONT_R_SENSOR_NO])/2)
        l_buf.append(info[LEFT_SENSOR_NO])
        r_buf.append(info[RIGHT_SENSOR_NO])
        num += 1;
    # 平均値取得
    sensor_value[FRONT_DIRECTION] = np.mean(f_buf)
    sensor_value[LEFT_DIRECTION] = np.mean(l_buf)
    sensor_value[RIGHT_DIRECTION] = np.mean(r_buf)

    return sensor_value

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
        # LED設定
        mw.led(led_state)
        time.sleep(1)

if __name__ == '__main__':
    test_recognition()
    
