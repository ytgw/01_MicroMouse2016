# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 14:31:24 2016
@author: ytgw
関数 move(direction, distance) の概要
出力 void
引数 direction:方向 反時計回りが正．単位はdegreeで，基本の使用範囲は-180〜180°
　　 ditance:距離(進む区画の数) 範囲は-∞〜∞
概要
direction[°]分だけ方向転換をした後に，distance[区画]分だけ直進する
"""

import time
import math
import numpy as np
import middleware as mw

#--------------------------------------------------------------#
# 関数本体
#--------------------------------------------------------------#
def move(direction, distance):
    # 定数定義
    BLOCK_LENGTH = 18.0     # [cm] 一区画の一辺の長さ
    MOTOR_FREQUENCY = 400   # [Hz] モータの周波数(400Hzのとき1秒間に一回転)
    MOTOR_REVOLUTION = 0.1  # [rps] モーターの回転回数
    WHEEL_WIDTH = 9.5       # [cm] 2つのタイヤの距離(調査済み)
    TIRE_RADIUS = 4.7/2.0   # [cm] タイヤの半径(調査済み)
    SLIP_RATE = 1.0         # [-] 滑り率 1の時はタイヤは滑らない(調査必要)
    
    
    # [cm/sec] タイヤの並進速度    
    speed = 2*math.pi*TIRE_RADIUS*MOTOR_REVOLUTION
    
    
    # 方向変換
    theta = direction * math.pi/180
    sleepTime = math.fabs(1/SLIP_RATE * (WHEEL_WIDTH/2 * theta) / speed)
    motorInput = np.sign(theta)*MOTOR_REVOLUTION*MOTOR_FREQUENCY
#    print sleepTime
    
    mw.motor([-motorInput, motorInput])
    time.sleep(sleepTime)
    mw.motor([0, 0])
    

    # 直進運動
    sleepTime = math.fabs(1/SLIP_RATE * (distance * BLOCK_LENGTH) / speed)
    motorInput = MOTOR_REVOLUTION*MOTOR_FREQUENCY
#    print sleepTime
    
    mw.motor([motorInput, motorInput])
    time.sleep(sleepTime)
    mw.motor([0, 0])


#--------------------------------------------------------------#
# テスト
#--------------------------------------------------------------#
def moveTest():
    # 方向転換のテスト
    move(90,0)
    time.sleep(1)
    move(-90,0)
    time.sleep(1)
    move(180,0)
    time.sleep(1)
    move(-180,0)
    
    # ブザーを鳴動
    mw.buzzer(440)
    time.sleep(2)
    mw.buzzer(0)
    
    # 直進運動のテスト
    move(0,1)
    time.sleep(1)
    move(0,2)
    time.sleep(1)
    move(0,-1)
    time.sleep(1)
    move(0,-2)
    time.sleep(1)

if __name__ == '__main__':
    moveTest()
