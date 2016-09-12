import time
import middleware as mw

#-----------------------------------------------------------------------------#
# Declataion                                                                  #
#-----------------------------------------------------------------------------#

FRONT_THRESHOLD = 100	# 閾値(前方)
LEFT_THRESHOLD = 100	# 閾値(左方)
RIGHT_THRESHOLD = 100	# 閾値(右方)

#-----------------------------------------------------------------------------#
# Function                                                                    #
#-----------------------------------------------------------------------------#
def check_wall_front():
    """ 距離センサ1,2より前方に壁があるかどうかチェックする
    """
    info = mw.sensorinfo()
    print info[0],info[1],info[2],info[3]
    average = (info[1] + info[2]) / 2
    if average > FRONT_THRESHOLD:
        return 1	# 壁あり
    else:
        return 0	# 壁なし

def check_wall_left():
    """ 距離センサ0より左方に壁があるかどうかチェックする
    """
    info = mw.sensorinfo()
    if info[0] > LEFT_THRESHOLD:
        return 1	# 壁あり
    else:
        return 0	# 壁なし

def check_wall_right():
    """ 距離センサ3より右方に壁があるかどうかチェックする
    """
    info = mw.sensorinfo()
    if info[3] > RIGHT_THRESHOLD:
        return 1	# 壁あり
    else:
        return 0	# 壁なし

#-----------------------------------------------------------------------------#
# Test                                                                        #
#-----------------------------------------------------------------------------#
def test_recognition():
    """ 壁あり/なしチェックを実施しLEDを点灯する 
    """	
    # LED初期化
    led_state = [0,0,0,0]
    while True:
	# LED_0点灯
        led_state[0] = 1
	# 前方壁チェック(壁あり:LED_1点灯)
        if check_wall_front() == 1:
            led_state[1] = 1
        else:
            led_state[1] = 0
	# 左方壁チェック(壁あり:LED_2点灯)
        if check_wall_left() == 1:
            led_state[2] = 1
        else:
            led_state[2] = 0
        # 右方壁チェック(壁あり:LED_3点灯)
        if check_wall_right() == 1:
            led_state[3] = 1
        else:
            led_state[3] = 0
        # LED設定
        mw.led(led_state)
        time.sleep(1)

if __name__ == '__main__':
    test_recognition()
    
