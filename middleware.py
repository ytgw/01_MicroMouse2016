# coding: UTF-8
import time
import numpy as np
#-----------------------------------------------------------------------------#
# Declation                                                                  #
#-----------------------------------------------------------------------------#

# 各デバイスドライバのパス
sensor_driver  = "/dev/rtlightsensor0"
switch_driver  = [ "/dev/rtswitch0", "/dev/rtswitch1", "/dev/rtswitch2"]
buzzer_driver  = "/dev/rtbuzzer0"
motor_driver   = [ "/dev/rtmotor_raw_l0", "/dev/rtmotor_raw_r0"]
led_driver     = [ "/dev/rtled0", "/dev/rtled1", "/dev/rtled2", "/dev/rtled3"]
# デバイスドライバから取得した値を格納するリスト
sensor_info  = [ 0, 0, 0, 0 ] # [ 距離センサー0の取得値, 1の値, 2の値, 3の値 ]
switch_state = [ 0, 0, 0 ]    # [ タクトスイッチ0の取得値, 1の値, 2の値 ]

#-----------------------------------------------------------------------------#
# Input system (入力系)                                                       #
#-----------------------------------------------------------------------------#

def sensorinfo():
    '''
    概要：
    　距離センサの値を取得する
    　デバイスドライバに正常にアクセスできた場合 => tryの処理
    　デバイスドライバにアクセスできなかった場合 => exceptの処理
    　（正確には、tryの処理中にエラーが発生した場合にexceptの処理が実行される）
    入力：
    　なし
    出力：
    　距離センサー0～3の値を格納したリスト
    '''
    try:
        filename = sensor_driver
        with open( filename, "r" ) as f:
            # f.readlin() の返り値は文字列
            # "距離センサー0の値" + " " + "1の値" + " " + "2の値" + " " + "3の値" + "\n"
            temp = f.readline()
            # 取得した文字列をスペース区切りで分割する
            temp = temp.split(" ")
            # デバイスドライバから取得できる値は文字列なので数値に変換する
            info = [ int( temp[0] ), int( temp[1] ), int( temp[2] ), int( temp[3] ) ]
    except:
        # エラー発生時は全ての要素に数値の255を代入する
        info = [ 255, 255, 255, 255 ]
    sensor_info = info
    return sensor_info

def switchstate():
    '''
    概要：
    　タクトスイッチの値を取得する
    　デバイスドライバに正常にアクセスできた場合 => tryの処理
    　デバイスドライバにアクセスできなかった場合 => exceptの処理
    　（正確には、tryの処理中にエラーが発生した場合にexceptの処理が実行される）
    入力：
    　なし
    出力：
    　タクトスイッチ0～2の値を格納したリスト
    '''
    state = [ 0, 0, 0 ]
    try:
        for i, filename in enumerate( switch_driver ):
            with open( filename, "r" ) as f:
                # f.readlin() の返り値は文字列)
                # "0\n":押されてない or "1\n":押されている
                temp = f.readline()
                # デバイスドライバから取得できる値は文字列なので数値に変換する
                state[i] = int( temp[0] )
    except:
        # エラー発生時は全ての要素に数値の-1を代入する
        state = [ -1, -1, -1 ]
    switch_state = state
    return switch_state

#-----------------------------------------------------------------------------#
# Output system (出力系)                                                       #
#-----------------------------------------------------------------------------#

def buzzer( frequency ):
    '''
    概要：
    　ブザーを鳴らす
    　デバイスドライバに正常にアクセスできた場合 => tryの処理
    　デバイスドライバにアクセスできなかった場合 => exceptの処理
    　（正確には、tryの処理中にエラーが発生した場合にexceptの処理が実行される）
    入力：
    　ブザー音の周波数(Hz)
    出力：
    　正常にブザー音がなった => 返値 True
    　ブザー音がならなかった => 返値 False
    '''
    try:
        filename = buzzer_driver
        with open( filename, "w" ) as f:
            f.write( str( int( frequency ) ) )
        ret = True
    except:
        # エラー発生時は返値としてFalseを返す
        ret = False
    return ret

def motor( speed ):
    '''
    概要：
    　モーターを駆動する
    　デバイスドライバに正常にアクセスできた場合 => tryの処理
    　デバイスドライバにアクセスできなかった場合 => exceptの処理
    　（正確には、tryの処理中にエラーが発生した場合にexceptの処理が実行される）
    入力：
    　speed = [ 左モータの回転数(Hz), 右モータの回転数(Hz) ]
    出力：
    　正常にモーターを駆動できた => 返値 True
    　モーターを駆動できなかった => 返値 False
    '''
    try:
        for i, filename in enumerate( motor_driver ):
            with open( filename, "w" ) as f:
                f.write( str( int( speed[i] ) ) )
        ret = True
    except:
        # エラー発生時は返値としてFalseを返す
        ret = False
    if ret == False:
        print "---------------------mw.motor : ", ret
    # print ret
    return ret

def led( led_state ):
    '''
    概要：
    　LEDを駆動する
    　デバイスドライバに正常にアクセスできた場合 => tryの処理
    　デバイスドライバにアクセスできなかった場合 => exceptの処理
    　（正確には、tryの処理中にエラーが発生した場合にexceptの処理が実行される）
    入力：
    　led_state = [ led_0, led_1, led_2,led_3 ]
    　( "led_X = 0" => Off , "led_X = 1" => ON )
    出力：
    　正常にLEDを駆動できた => 返値 True
    　LEDを駆動できなかった => 返値 False
    '''
    try:
        for i,filename in enumerate( led_driver ):
            with open( filename, 'w' ) as f:
                f.write( str( led_state[i] ) )
        ret = True
    except:
        # エラー発生時は返値としてFalseを返す
        ret = False
    return ret

if __name__ == '__main__':
    while True:
        list0 = []
        list1 = []
        list2 = []
        list3 = []
        for i in range(0,30):
            aValue = sensorinfo()
            list0.append(aValue[0])
            list1.append(aValue[1])
            list2.append(aValue[2])
            list3.append(aValue[3])
            
        print "list0Mid : ", np.median(list0)
        print "list1Mid : ", np.median(list1)
        print "list2Mid : ", np.median(list2)
        print "list3Mid : ", np.median(list3)
        time.sleep(1)
