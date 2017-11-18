# -*- coding: utf-8 -*-
'''
ファイル action.py の概要
マシン出力系の関数を実装
'''

import time
import math
import numpy as np
import middleware as mw

#--------------------------------------------------------------#
# グローバル定数
#--------------------------------------------------------------#
GLOBAL_BLOCK_LENGTH = 18e-2     # [m] 一区画の長さ
GLOBAL_ZERO_DISTANCE = 1e-3     # [m] ゼロ距離
GLOBAL_STOP_MODE = 0            # [-] 停止状態
GLOBAL_STRAIGHT_MODE = 1        # [-] 直進状態
GLOBAL_ROTATE_MODE = 2          # [-] 回転状態
GLOBAL_CHECK_TIME_INCREMENT = 0.5 # [sec]

#--------------------------------------------------------------#
# グローバル変数
#--------------------------------------------------------------#
global_abs_time_for_straight = time.time()  # [s] 直進用の前回時間
global_abs_time_for_rotation = time.time()  # [s] 回転用の前回時間

global_rotation_speed = 0       # [rad/s] 回転速度
global_angle = 0                # [rad] 回転した角度
global_angle_order = 0          # [rad] 指令回転角度

global_speed = 0                # [m/s] 直進速度
global_distance = 0             # [m] 直進した距離
global_distance_order = 0       # [m] 指令距離

global_old_length_L = 0         # [m] 前回の左壁までの距離
global_old_length_R = 0         # [m] 前回の右壁までの距離

global_mode = GLOBAL_STOP_MODE  # 動作状態(停止，直進，回転)


#--------------------------------------------------------------#
# LED出力関数とブザー出力関数
#--------------------------------------------------------------#
def led(led_state):
    '''
    LED出力関数
    入力：
    　led_state = [ led_0, led_1, led_2,led_3 ]
    　( "led_X = 0" => Off , "led_X = 1" => ON )
    出力：
    　正常にLEDを駆動できた => 返値 True
    　LEDを駆動できなかった => 返値 False
    '''
    error_state = mw.led(led_state)
    return error_state

def buzzer(frequency):
    '''
    ブザー出力関数
    入力：
    　ブザー音の周波数(Hz)
    出力：
    　正常にブザー音がなった => 返値 True
    　ブザー音がならなかった => 返値 False
    '''
    error_state = mw.buzzer(frequency)
    return error_state

def buzzerWithTime(frequency,sleepTime):
    '''
    ブザー出力関数
    入力：
    　ブザー音の周波数(Hz)
    　ブザー音の鳴動時間(sec)
    出力：
    　正常にブザー音がなった => 返値 True
    　ブザー音がならなかった => 返値 False
    '''
    error_state1 = mw.buzzer(frequency)
    time.sleep(sleepTime)
    error_state2 = mw.buzzer(0)
    error_state = error_state1 & error_state2
    return error_state


#--------------------------------------------------------------#
# 直進走行開始関数
#--------------------------------------------------------------#
def startStraight(distOrder):
    '''
    直進走行開始関数の概要
    入力:距離命令[block]
    出力:残り距離[block]
    '''
    global global_distance, global_distance_order

    # 距離センサ情報を無効に設定
    distF = -1
    distL = -1
    distR = -1
    go_straight(distOrder,distF,distL,distR)
    resDist = (global_distance_order - global_distance) /  GLOBAL_BLOCK_LENGTH

    # print "distOrder from startStraight : %d[block]" % distOrder

    return resDist


#--------------------------------------------------------------#
# 直進指令距離追加関数
#--------------------------------------------------------------#
def addDistanceOrder(addDist):
    '''
    直進指令距離追加関数の概要
    入力:追加距離[block]
    出力:残り距離[block]
    '''
    global global_distance, global_distance_order

    global_distance_order += (addDist * GLOBAL_BLOCK_LENGTH)
    resDist = (global_distance_order - global_distance) /  GLOBAL_BLOCK_LENGTH

    # print "addDistOrder from addDistanceOrder : %d[block]" % addDist

    return resDist


#--------------------------------------------------------------#
# 直進指令維持関数
#--------------------------------------------------------------#
def keepStraight(distF,distL,distR):
    '''
    直進指令維持関数の概要
    入力:前壁までの距離，左壁までの距離，右壁までの距離
    出力:残り距離[block]
    '''
    global global_distance, global_distance_order

    if global_mode == GLOBAL_STRAIGHT_MODE:
        resDist = go_straight(0,distF,distL,distR)
    else:
        print "An error occurs in action.keepStraight function"

    return resDist


#--------------------------------------------------------------#
# 回転走行関数
#--------------------------------------------------------------#
def rotateUntilLast(angleOrder):
    '''
    回転走行関数の概要
    入力:命令角度[degree]
    出力:残り角度[degree]
    '''
    global global_angle, global_angle_order

    rotate(angleOrder)
    while is_running():
        resAngle = rotate(0)

    # print "angleOrder from rotateUntilLast : %d[degree]" % angleOrder

    return resAngle


def back(mDist):
    SPEED = 10e-2                      # [m/s] 速度
    sleepTime = mDist / SPEED

    freq = speed_2_frequency( SPEED )
    mw.motor([-freq, -freq])
    time.sleep(sleepTime)
    mw.motor([0,0])


#--------------------------------------------------------------#
# 動作有無取得関数
#--------------------------------------------------------------#
def is_running():
    '''
    動作有無取得関数is_runningの概要
    入力:void
    出力:動作有無フラグ(Trueのとき動作中，Falseのとき停止中)
    '''
    if (global_mode == GLOBAL_STRAIGHT_MODE) or (global_mode == GLOBAL_ROTATE_MODE):
        output = True
    elif global_mode == GLOBAL_STOP_MODE:
        output = False
    else:
        print "An error occurs in action.is_running function"

    return output

def reset():
    global global_mode
    mw.motor([0,0])
    global_mode = GLOBAL_STOP_MODE


#--------------------------------------------------------------#
#--------------------------------------------------------------#
# 以下はローカルで使用する目的の関数
#--------------------------------------------------------------#
#--------------------------------------------------------------#

#--------------------------------------------------------------#
# 直進走行関数
#--------------------------------------------------------------#
def go_straight(block_distance,length_F,length_L,length_R):
    '''
    直進走行関数go_straightの概要
    入力:距離指令[block]，前壁までの距離[m]，左壁までの距離[m]，右壁までの距離[m]
    出力:残り距離[block]
    '''
    # 定数
    ACCELERATION = 0.12     # [m/s**2] 加速度
    DECELERATION = 0.12     # [m/s**2] 減速度
    # グローバル変数
    global global_abs_time_for_straight
    global global_speed
    global global_distance, global_distance_order
    global global_old_length_L, global_old_length_R
    global global_mode


    #----------------------#
    # 状態ごとの処理切り替え
    #----------------------#
    if global_mode == GLOBAL_STOP_MODE:
        # 停止時呼び出しの処理
        global_abs_time_for_straight = time.time()
        time_increment = 0
        global_speed = 0
        global_distance = 0
        global_distance_order = block_distance * GLOBAL_BLOCK_LENGTH
        global_mode = GLOBAL_STRAIGHT_MODE
    elif global_mode == GLOBAL_STRAIGHT_MODE:
        # 直進状態時呼び出しの処理
        old_abs_time = global_abs_time_for_straight
        global_abs_time_for_straight = time.time()
        time_increment = global_abs_time_for_straight - old_abs_time
        distance_increment = global_speed * time_increment
        global_distance += distance_increment
    else:
        print "An error occurs in action.go_straight function"

    if (time_increment > GLOBAL_CHECK_TIME_INCREMENT) or (time_increment < 0):
        print "An warning occurs in action.go_straight function"
        print "    Please check time_increment"
        print "    time_increment : %.3f [sec]" % time_increment


    #----------------------#
    # 台形加速による速度指令算出
    #----------------------#
    residual_distance = global_distance_order - global_distance
    global_speed = ramp_speed_control(time_increment,global_speed,residual_distance,ACCELERATION,DECELERATION)


    #----------------------#
    # 距離センサによる速度補正
    #----------------------#
    # 直進方向の速度補正
    # (residual_distance, global_speed) = correct_F(residual_distance,global_speed,length_F)

    # 左右方向の速度補正の準備
    # センサ差分の更新
    diff_length_L = length_L-global_old_length_L
    diff_length_R = length_R-global_old_length_R
    global_old_length_L = length_L
    global_old_length_R = length_R
    # 左右方向の速度補正
    control_input = correct_LR(length_L,length_R,diff_length_L,diff_length_R)


    #----------------------#
    # モータ指令の算出
    #----------------------#
    # モータ周波数への変換
    left_Hz  = speed_2_frequency( global_speed - control_input )
    right_Hz = speed_2_frequency( global_speed + control_input )
    # print "(length_L,length_R) :  (%.3f, %.3f)" % (length_L,length_R)
    # print "(speed, adjustLR) : (%.2f, %.2f)" % (global_speed, control_input)
    # print "(freqL, freqR) : (%.1f, %.1f)" % (left_Hz, right_Hz)
    # モータ出力
    mw.motor([left_Hz, right_Hz])


    #----------------------#
    # 停止状態移行条件　→　残り距離の絶対値がゼロ距離未満
    #----------------------#
    if abs(residual_distance) < GLOBAL_ZERO_DISTANCE:
        global_mode = GLOBAL_STOP_MODE
        residual_distance = 0
        mw.motor([0,0])


    blockResDist = residual_distance / GLOBAL_BLOCK_LENGTH

    return blockResDist


#--------------------------------------------------------------#
# 回転走行関数
#--------------------------------------------------------------#
def rotate(degree_angle):
    '''
    回転走行関数rotateの概要
    入力:角度指令[°]
    出力:残り角度[°]
    '''
    # 定数
    ACCELERATION = 0.12     # [m/s**2] 加速度
    DECELERATION = 0.12     # [m/s**2] 減速度
    WHELL_WIDTH = 9.7e-2    # [m] 2つのタイヤの距離(調査済み)
    # グローバル変数
    global global_abs_time_for_rotation
    global global_rotation_speed
    global global_angle, global_angle_order
    global global_mode


    #----------------------#
    # 状態ごとの処理切り替え
    #----------------------#
    if global_mode == GLOBAL_STOP_MODE:
        # 停止時呼び出しの処理
        global_abs_time_for_rotation = time.time()
        time_increment = 0
        global_rotation_speed = 0
        global_angle = 0
        global_angle_order = math.radians(degree_angle)
        global_mode = GLOBAL_ROTATE_MODE
    elif global_mode == GLOBAL_ROTATE_MODE:
        # 直進状態時呼び出しの処理
        old_abs_time = global_abs_time_for_rotation
        global_abs_time_for_rotation = time.time()
        time_increment = global_abs_time_for_rotation - old_abs_time
        angle_increment = global_rotation_speed * time_increment
        global_angle += angle_increment
    else:
        print "An error occurs in action.rotate function"

    if (time_increment > GLOBAL_CHECK_TIME_INCREMENT) or (time_increment < 0):
        print "An error occurs in action.rotate function"
        print "    Please check time_increment"
        print "    time_increment : %.3f [sec]" % time_increment


    #----------------------#
    # 台形加速による速度指令算出
    #----------------------#
    rotation_radius = WHELL_WIDTH/2.0
    speed = rotation_radius * global_rotation_speed
    residual_angle = global_angle_order - global_angle
    residual_distance = rotation_radius * residual_angle
    speed = ramp_speed_control(time_increment,speed,residual_distance,ACCELERATION,DECELERATION)
    global_rotation_speed = speed / rotation_radius


    #----------------------#
    # モータ指令の算出
    #----------------------#
    # モータ周波数への変換
    frequency = speed_2_frequency(speed)
    # モータ出力
    mw.motor([-frequency, frequency])


    #----------------------#
    # 停止状態移行条件　→　残り距離の絶対値がゼロ距離未満
    #----------------------#
    if abs(residual_distance) < GLOBAL_ZERO_DISTANCE:
        global_mode = GLOBAL_STOP_MODE
        residual_angle = 0
        mw.motor([0,0])


    degreeResAngle = math.degrees(residual_angle)

    return degreeResAngle


#--------------------------------------------------------------#
# 台形加速関数
#--------------------------------------------------------------#
def ramp_speed_control(time_increment,speed,residual_distance,acceleration,deceleration):
    MAX_SPEED = 32e-2                       # [m/s] 最高速度
    MIN_SPEED = 10e-2                       # [m/s] 最低速度
    MAX_DIFF_SPEED = 100e-3 * acceleration  # [m/s]

    # 台形加速用の関数
    speed_sq = 2*deceleration*abs(residual_distance) + MIN_SPEED**2
    if speed**2 < speed_sq:
        # 加速
        abs_return_speed = abs(speed) + acceleration*time_increment
#        print "accel"
    else:
        # 減速
        abs_return_speed = math.sqrt(speed_sq)

    # 速度変化の制限
    diff_speed = np.sign(residual_distance)*abs_return_speed - speed
    if abs(diff_speed) > MAX_DIFF_SPEED:
        abs_return_speed = abs(speed + np.sign(diff_speed)*MAX_DIFF_SPEED)

    # 速度制限
    if abs_return_speed > MAX_SPEED:
        abs_return_speed = MAX_SPEED
    elif abs_return_speed < MIN_SPEED:
        abs_return_speed = MIN_SPEED

    return_speed = np.sign(residual_distance) * abs_return_speed

    return return_speed


#--------------------------------------------------------------#
# 直進方向補正関数
#--------------------------------------------------------------#
def correct_F(residual_distance,speed,length_F):
    # 直進方向の補正→前方センサ値一定を比例制御することで補正
    # 参考:http://mmk.rulez.jp/?page_id=392
    ERROR = -1          # [m] センサ値のエラー値用
    REFERENCE_F = 2e-2  # [m] 前センサの参照値
    THRESHOLD_F = 5e-2  # [m] 前センサの閾値
    KpF = 1.5           # 比例制御の定数

    if (length_F != ERROR) and (length_F < THRESHOLD_F):
        # 壁が近い時
        return_distance = length_F - REFERENCE_F
        return_speed = KpF * return_distance
    else:
        # 壁が遠い時
        return_distance = residual_distance
        return_speed = speed

    return (return_distance, return_speed)


#--------------------------------------------------------------#
# 左右方向補正関数
#--------------------------------------------------------------#
def correct_LR(length_L,length_R,diff_L,diff_R):
    # 左右方向の補正→左右センサ値一定を比例制御することで補正
    # 参考:http://mice.deca.jp/cgi/dokuwiki/doku.php?id=%E5%A3%81%E5%88%B6%E5%BE%A1
    ERROR = -1                  # [m] センサ値のエラー値用
    REFERENCE_L = 3.4e-2        # [m] 左センサの参照値
    REFERENCE_R = 3.4e-2        # [m] 右センサの参照値
    THRESHOLD_L = 6e-2          # [m] 左センサの閾値
    THRESHOLD_R = 6e-2          # [m] 右センサの閾値
    THRESHOLD_DIFF_L = 5e-3     # [m] 左距離変化量の閾値
    THRESHOLD_DIFF_R = 5e-3     # [m] 右距離変化量の閾値
    KpLR = 0.8                  # 比例制御の定数
    MAXIMUM_RL_ERROR = 3e-2     # [m]

    l_error = length_L-REFERENCE_L
    r_error = length_R-REFERENCE_R
    is_L_good = (length_L != ERROR) and (length_L < THRESHOLD_L) and (abs(diff_L) < THRESHOLD_DIFF_L)
    is_R_good = (length_R != ERROR) and (length_R < THRESHOLD_R) and (abs(diff_R) < THRESHOLD_DIFF_R)
    if is_L_good and is_R_good:
        rl_error = l_error - r_error
    elif is_L_good:
        rl_error = 2*l_error
    elif is_R_good:
        rl_error = -2*r_error
    else:
        rl_error = 0

    if abs(rl_error) > MAXIMUM_RL_ERROR:
        rl_error = np.sign(rl_error) * MAXIMUM_RL_ERROR

    control_input = KpLR * rl_error
    return control_input

#--------------------------------------------------------------#
# 速度[m/s]→モータ入力周波数[Hz]変換関数
#--------------------------------------------------------------#
def speed_2_frequency(speed):
    TIRE_DIAMETER = 4.80e-2  # [m] タイヤの半径
    FREQUENCY = 400          # [Hz] モータの周波数(400Hzのとき1秒間に一回転)

    tire_radius = TIRE_DIAMETER/2.0
    omega = speed/tire_radius
    return_frequency = FREQUENCY * omega / (2*math.pi)

    return return_frequency


if __name__ == '__main__':
    degreeAngle = -180
    buzzer(2093)
    time.sleep(1)
    for i in range(0,4):
        rotateUntilLast(degreeAngle)
    buzzer(0)
