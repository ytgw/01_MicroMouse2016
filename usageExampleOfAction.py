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

#--------------------------------------------------------------#
# 実行内容
#--------------------------------------------------------------#
if __name__ == '__main__':
    test_for_ramp_control()
#    test_for_correct()
#    test_for_rotate()
    print 'Test finished'

