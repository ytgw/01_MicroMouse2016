# coding: UTF-8

import time 
import middleware as mw 

#-----------------------------------------------------------------------------# 
# Declataion                                                                  # 
#-----------------------------------------------------------------------------# 

FRONT_THRESHOLD = 895	# 閾値(前方)
LEFT_THRESHOLD = 800	# 閾値(左方) 
RIGHT_THRESHOLD = 800	# 閾値(右方)

#-----------------------------------------------------------------------------# 
# Function                                                                    # 
#-----------------------------------------------------------------------------# 
def check_wall_front(): 
 """ 距離センサ1,2より前方に壁があるかどうかチェックする 
 """ 
 info = mw.sensorinfo()
 average = (info[0] + info[3]) / 2 
 if average > FRONT_THRESHOLD: 
     return 1	# 壁あり 
 else: 
     return 0	# 壁なし 

def check_wall_left(): 
 """ 距離センサ0より左方に壁があるかどうかチェックする 
 """ 
 info = mw.sensorinfo() 
 if info[2] > LEFT_THRESHOLD: 
     return 1	# 壁あり
 else: 
     return 0	# 壁なし 

def check_wall_right(): 
 """ 距離センサ3より右方に壁があるかどうかチェックする 
 """ 
 info = mw.sensorinfo() 
 if info[1] > RIGHT_THRESHOLD: 
     return 1	# 壁あり
 else: 
     return 0	# 壁なし

#-----------------------------------------------------------------------------# 
# Test                                                                        # 
#-----------------------------------------------------------------------------# 
def test_recognition(): 
 """ 壁あり/なしチェックを実施しLEDを点灯する  
 """	 
 # LED初期化
 led_state = [0,0,0,0] 
 info_min = [10000,10000,10000,10000]
 info_max = [0,0,0,0]

 while True: 
     # LED_0点灯
     led_state[0] = 1 
     # 前方壁チェック(壁あり:LED_1点灯)
     if check_wall_front() == 1: 
         led_state[2] = 1 
     else: 
         led_state[2] = 0 
     # 左方壁チェック(壁あり:LED_2点灯)
     if check_wall_left() == 1: 
         led_state[3] = 1 
     else: 
         led_state[3] = 0 
     # 右方壁チェック(壁あり:LED_3点灯)
     if check_wall_right() == 1: 
         led_state[1] = 1 
     else: 
         led_state[1] = 0 
     # LED設定 
     mw.led(led_state) 

     info = mw.sensorinfo()
     if info[3] > info_max[3]:
         info_max[3] = info[3]

     if info[3] < info_min[3]:
         info_min[3] = info[3]
     
     if info[0] > info_max[0]:
         info_max[0] = info[0]

     if info[0] < info_min[0]:
         info_min[0] = info[0]

     print info[3],info[2],info[1],info[0] 
     print info_min[3],info_max[3]    
     print info_min[0],info_max[0]    

     time.sleep(0.2) 

if __name__ == '__main__': 
 test_recognition() 
