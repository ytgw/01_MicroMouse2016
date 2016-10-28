# -*- coding: utf-8 -*-
'''
ファイル action.py の概要
直進走行関数go_straight，回転走行関数rotate，動作有無取得関数is_runningを実装
それぞれの入出力は各関数のコメントを参照のこと
'''

import time
import math
import numpy as np
import middleware as mw

#--------------------------------------------------------------#
# グローバル定数
#--------------------------------------------------------------#
GLOBAL_BLOCK_LENGTH = 18e-2     # [m] 一区画の長さ
GLOBAL_WHELL_WIDTH = 9.5e-2     # [m] 2つのタイヤの距離(調査済み)
GLOBAL_TIRE_DIAMETER = 4.7e-2   # [m] タイヤの半径(調査済み)
GLOBAL_ACCEL = 6e-2             # [m/s^2] 加減速の大きさ
GLOBAL_MAX_SPEED = 20e-2        # [m/s] 最高速度
GLOBAL_ZERO_SPEED = 0.2e-2      # [m/s] ゼロ速度
GLOBAL_ZERO_DISTANCE = 0.05e-2  # [m] ゼロ距離

#--------------------------------------------------------------#
# グローバル変数
#--------------------------------------------------------------#
global_time = 0                 # [s] 時間
global_old_time = time.time()   # [s] 前回の時間

global_rotation_speed = 0       # [rad/s] 回転速度
global_angle = 0                # [rad] 回転した角度
global_angle_order = 0          # [rad] 指令回転角度

global_speed = 0                # [m/s] 直進速度
global_distance = 0             # [m] 直進した距離
global_distance_order = 0       # [m] 指令距離

global_old_length_L = 0         # [m] 前回の左壁までの距離
global_old_length_R = 0         # [m] 前回の右壁までの距離

global_is_running = False       # 動作フラグ(動作中はTrue，停止中はFalse)

#--------------------------------------------------------------#
# 直進走行関数
#--------------------------------------------------------------#
def go_straight(block_distance,length_F,length_L,length_R):
    '''
    直進走行関数go_straightの概要
    入力:blockごとの距離指令，前壁までの距離，左壁までの距離，右壁までの距離
    出力:動作有無フラグ(Trueのとき動作中，Falseのとき停止中)
    '''
    # グローバル定数と変数
    global GLOBAL_BLOCK_LENGTH
    global GLOBAL_ACCEL, GLOBAL_MAX_SPEED
    global GLOBAL_ZERO_SPEED
    global global_time, global_old_time
    global global_speed
    global global_distance, global_distance_order
    global global_old_length_L, global_old_length_R
    global global_is_running    
    
    # 時間の更新
    time_increment = time.time() - global_old_time
    global_old_time = time.time()
    global_time += time_increment
    # 距離の更新
    distance_increment = global_speed * time_increment
    global_distance += distance_increment
    # センサ差分の更新
    if distance_increment == 0:
        diff_length_L = 0
        diff_length_R = 0
    else:
        diff_length_L = (length_L-global_old_length_L) / distance_increment
        diff_length_R = (length_R-global_old_length_R) / distance_increment
    
    global_old_length_L = length_L
    global_old_length_R = length_R
    
    if not(global_is_running):
        # 初期呼び出し時の処理
        global_time = 0
        global_speed = 0
        global_distance = 0
        global_distance_order = block_distance * GLOBAL_BLOCK_LENGTH
        global_is_running = True
    else:
        # 初期呼び出し以外の処理
        residual_distance = global_distance_order - global_distance
        
        # 台形加速の実装
        global_speed = ramp_speed_control(global_time,global_speed,residual_distance)

        # 終了条件　→　予測停止時間以上かつゼロ速度以下
        abs_distance_order = math.fabs(global_distance_order)
        if abs_distance_order < (GLOBAL_MAX_SPEED**2/GLOBAL_ACCEL):
            # 最高速度に達しない場合の予測停止時間
            predict_stop_time = math.sqrt(abs_distance_order/GLOBAL_ACCEL)
        else:
            # 最高速度に達する場合の予測停止時間
            predict_stop_time = abs_distance_order/GLOBAL_MAX_SPEED - GLOBAL_MAX_SPEED/GLOBAL_ACCEL
        
        if (global_time > predict_stop_time) \
        and (math.fabs(global_speed) < GLOBAL_ZERO_SPEED):
            global_is_running = False
        
    # 直進方向の速度補正
    global_speed = correct_F(global_speed,length_F)
    # 左右方向の速度補正
    control_input = correct_LR(length_L,length_R,diff_length_L,diff_length_R)
    # モータ周波数への変換
    left_Hz = speed_2_frequency( global_speed - control_input )
    right_Hz = speed_2_frequency( global_speed + control_input )
    
    # モータ出力
    mw.motor([left_Hz, right_Hz])
        
    return global_is_running

#--------------------------------------------------------------#
# 回転走行関数
#--------------------------------------------------------------#
def rotate(degree_angle):
    '''
    回転走行関数rotateの概要
    入力:角度指令[°]
    出力:動作有無フラグ(Trueのとき動作中，Falseのとき停止中)
    '''
    # グローバル変数の宣言
    global global_time, global_old_time
    global global_rotation_speed
    global global_angle, global_angle_order
    global global_is_running

    # 時間の更新
    time_increment = time.time() - global_old_time
    global_old_time = time.time()
    global_time += time_increment
    # 距離の更新
    angle_increment = global_rotation_speed * time_increment
    global_angle += angle_increment

    if not(global_is_running):
        # 初期呼び出し時の処理
        global_time = 0
        global_rotation_speed = 0
        speed = 0
        global_angle = 0
        global_angle_order = math.radians(degree_angle)
        global_is_running = True
    else:
        # 初期呼び出し以外の処理
        rotation_radius = GLOBAL_WHELL_WIDTH/2.0
        speed = rotation_radius * global_rotation_speed
        
        residual_angle = global_angle_order - global_angle
        residual_distance = rotation_radius * residual_angle
        
        # 台形加速の実装
        speed = ramp_speed_control(global_time,speed,residual_distance)
        global_rotation_speed = speed / rotation_radius
        
        # 終了条件　→　予測停止時間以上かつゼロ距離以下
        abs_distance_order = math.fabs(rotation_radius * global_angle_order)
        if abs_distance_order < (GLOBAL_MAX_SPEED**2/GLOBAL_ACCEL):
            # 最高速度に達しない場合の予測停止時間
            predict_stop_time = math.sqrt(abs_distance_order/GLOBAL_ACCEL)
        else:
            # 最高速度に達する場合の予測停止時間
            predict_stop_time = abs_distance_order/GLOBAL_MAX_SPEED - GLOBAL_MAX_SPEED/GLOBAL_ACCEL
        
        if (global_time > predict_stop_time) \
        and math.fabs(residual_distance) < GLOBAL_ZERO_DISTANCE:
            global_is_running = False

    # モータ出力
    frequency = speed_2_frequency(speed)
    mw.motor([-frequency, frequency])
        
    return global_is_running

#--------------------------------------------------------------#
# 動作有無取得関数
#--------------------------------------------------------------#
def is_running():
    '''
    動作有無取得関数is_runningの概要
    入力:void
    出力:動作有無フラグ(Trueのとき動作中，Falseのとき停止中)
    '''
    return global_is_running


#--------------------------------------------------------------#
#--------------------------------------------------------------#
# 以下はローカルで使用する目的の関数
#--------------------------------------------------------------#
#--------------------------------------------------------------#

#--------------------------------------------------------------#
# 台形加速関数
#--------------------------------------------------------------#
def ramp_speed_control(time,speed,residual_distance):
    # 台形加速用の関数
    global GLOBAL_ACCEL, GLOBAL_MAX_SPEED
    
    if ( (speed**2)/(2*GLOBAL_ACCEL) ) < residual_distance:
        # 増速
        if (GLOBAL_ACCEL*time) > GLOBAL_MAX_SPEED:
            return_speed = GLOBAL_MAX_SPEED
        else:
            return_speed = GLOBAL_ACCEL*time
    else:
        # 減速
        speed_square = math.fabs(2*GLOBAL_ACCEL*residual_distance)
        return_speed = np.sign(residual_distance) * math.sqrt(speed_square)
        
    return return_speed

#--------------------------------------------------------------#
# 直進方向補正関数
#--------------------------------------------------------------#
def correct_F(speed,length_F):
    # 直進方向の補正→前方センサ値一定を比例制御することで補正
    # 参考:http://mmk.rulez.jp/?page_id=392
    REFERENCE_F = 2e-2  # [m] 前センサの参照値
    THRESHOLD_F = 5e-2  # [m] 前センサの閾値
    KpF = 10**(-2)      # 比例制御の定数
    
    if length_F < THRESHOLD_F:
        # 壁が近い時
        return_speed = KpF * (length_F - REFERENCE_F)
    else:
        # 壁が遠い時
        return_speed = speed
    
    return return_speed

#--------------------------------------------------------------#
# 左右方向補正関数
#--------------------------------------------------------------#
def correct_LR(length_L,length_R,diff_L,diff_R):
    # 左右方向の補正→左右センサ値一定を比例制御することで補正
    # 参考:http://mice.deca.jp/cgi/dokuwiki/doku.php?id=%E5%A3%81%E5%88%B6%E5%BE%A1
    REFERENCE_L = 2e-2          # [m] 左センサの参照値
    THRESHOLD_L = 5e-2          # [m] 左センサの閾値
    THRESHOLD_DIFF_L = 5e-2     # [m/m] 左センサの直進距離変化に対する左右距離変化量の閾値
    REFERENCE_R = 2e-2          # [m] 右センサの参照値
    THRESHOLD_R = 5e-2          # [m] 右センサの閾値
    THRESHOLD_DIFF_R = 5e-2     # [m/m] 右センサの直進距離変化に対する左右距離変化量の閾値
    KpLR = 10**(-2)             # 比例制御の定数
    
    l_error = length_L-REFERENCE_L
    r_error = length_R-REFERENCE_R
    is_L_good = (length_L < THRESHOLD_L) and (diff_L < THRESHOLD_DIFF_L)
    is_R_good = (length_R < THRESHOLD_R) and (diff_R < THRESHOLD_DIFF_R)
    if is_L_good and is_R_good:
        rl_error = l_error - r_error
    elif is_L_good:
        rl_error = 2*l_error
    elif is_R_good:
        rl_error = -2*r_error
    else:
        rl_error = 0
    
    control_input = KpLR * rl_error
    return control_input

#--------------------------------------------------------------#
# 速度[m/s]→モータ入力周波数[Hz]変換関数
#--------------------------------------------------------------#
def speed_2_frequency(speed):
    global GLOBAL_BLOCK_LENGTH, GLOBAL_TIRE_DIAMETER
    FREQUENCY = 400   # [Hz] モータの周波数(400Hzのとき1秒間に一回転)

    tire_radius = GLOBAL_TIRE_DIAMETER/2.0
    omega = speed/tire_radius
    return_frequency = FREQUENCY * omega / (2*math.pi)
        
    return return_frequency

