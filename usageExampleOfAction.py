# -*- coding: utf-8 -*-
'''
ファイル usageExampleOfAction の概要
action.pyでは直進走行関数go_straight，回転走行関数rotate，動作有無取得関数is_runningを実装
各関数の使用例はテスト関数を参照のこと
go_straightの使用例　test_for_ramp_control()およびtest_for_correct()は
rotateの使用例　test_for_rotate()
動作有無取得関数の使用例　test_for_ramp_control()およびtest_for_rotate()
'''

import action
import recognition
import random

GLOBAL_DEFAULT_MODE = 0
GLOBAL_FRONT_MODE = 1
GLOBAL_LEFT_MODE = 2
GLOBAL_RIGHT_MODE = 3
GLOBAL_BACK_MODE = 4

global_order_is_running = False

def test_for_ramp_control():
    '''
    台形加速テスト関数
    '''
    block_distance_order = 3    # [block] ブロック距離指令
    length_F = 1                # [m] 前壁までの距離
    length_L = 2e-2             # [m] 左壁までの距離
    length_R = 2e-2             # [m] 右壁までの距離
    action.go_straight(block_distance_order,length_F,length_L,length_R)
    while True:
        action.go_straight(block_distance_order,length_F,length_L,length_R)
        print 'time: %.3f speed: %.3f distance: %.3f' \
        % (action.global_time, action.global_speed, action.global_distance)
        if not(action.is_running()):
            break

def test_for_correct():
    '''
    直進方向補正と左右方向補正のテスト関数
    '''
    block_distance_order = 0    # [block] ブロック距離指令
    length_F = 2e-2             # [m] 前壁までの距離
    length_L = 2e-2             # [m] 左壁までの距離
    length_R = 2e-2             # [m] 右壁までの距離
    while True:
        fwall = recognition.check_wall_front()
        lwall = recognition.check_wall_left()
        rwall = recognition.check_wall_right()

        if fwall == 1:
            length_F = 1e-2
        else:
            length_F = 3e-2
        
        if lwall == 1:
            length_L = 1e-2
        else:
            length_L = 3e-2
    
        if rwall == 1:
            length_R = 1e-2
        else:
            length_R = 3e-2
        
        action.go_straight(block_distance_order,length_F,length_L,length_R)

def test_for_rotate():
    '''
    回転走行関数のテスト関数
    '''
    degree_angle_order = 90     # [°] 回転角度指令
    action.rotate(degree_angle_order)
    while True:
        action.rotate(degree_angle_order)
        print 'time: %.5f angle: %.5f' \
        % (action.global_time, action.global_angle)
        if not(action.is_running()):
            break

def tmp_function_for_group_meeting():
    WALL = 1
    while True:
        length_F = 1
        near_wall = recognition.check_wall_near()
        if near_wall == recognition.WALL_LEFT_NEAR:
            length_L = 1.5e-2
            length_R = 2.5e-2
        elif near_wall == recognition.WALL_RIGHT_NEAR:
            length_L = 2.5e-2
            length_R = 1.5e-2
        else:
            length_L = 1
            length_R = 1
        
        if action.is_running():
            action.keep_order(length_F,length_L,length_R)
        else:
            fwall = recognition.check_wall_front()
#            fwall = random.randint(0,1)
            print fwall
            if fwall == WALL:
                action.rotate(90)
                print 'rotate'
            else:
                action.go_straight(1,length_F,length_L,length_R)
                print 'straight'



def test():
    global global_order_is_running
    
    if global_order_is_running:
        # 指令処理の続行
        keep_order()
    else:
        # 経路判断処理
        left_hand()

def keep_order():
    

def left_hand():
    global GLOBAL_DEFAULT_MODE, GLOBAL_FRONT_MODE
    global GLOBAL_LEFT_MODE, GLOBAL_RIGHT_MODE
    global GLOBAL_BACK_MODE
    
    mode = GLOBAL_DEFAULT_MODE
    
    fwall = recognition.check_wall_front()
    lwall = recognition.check_wall_left()
    rwall = recognition.check_wall_right()
    
    if lwall == 0:
        mode = GLOBAL_LEFT_MODE
    elif lwall == 1 and fwall == 0:
        mode = GLOBAL_FRONT_MODE
    elif (lwall == 1 and fwall == 1) and rwall == 0:
        mode = GLOBAL_RIGHT_MODE
    elif (lwall == 1 and fwall == 1) and rwall == 1:
        mode = GLOBAL_BACK_MODE
    
    run_order(mode)

def run_order(mode)
#--------------------------------------------------------------#
# 実行内容
#--------------------------------------------------------------#
if __name__ == '__main__':
#    test_for_ramp_control()
#    test_for_correct()
#    test_for_rotate()
    tmp_function_for_group_meeting()
    print 'Test finished'

