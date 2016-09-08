# coding: UTF-8

#-----------------------------------------------------------------------------#
# Declation                                                                  #
#-----------------------------------------------------------------------------#
# 各デバイスドライバのパス
sensor_driver  = "/dev/rtlightsensor0"
switch_driver  = [ "/dev/rtswitch0", "/dev/rtswitch1"]
buzzer_driver  = "/dev/rtbuzzer0"
motor_driver   = [ "/dev/rtmotor_raw_l0", "/dev/rtmotor_raw_r0"]
led_driver     = [ "/dev/rtled0", "/dev/rtled1", "/dev/rtled2", "/dev/rtled3"] 
# デバイスドライバから取得した値を格納する配列
sensor_info  = [ 0, 0, 0, 0 ] # [ 距離センサー0の取得値, 1の値, 2の値, 3の値 ]  
switch_state = [ 0, 0, 0 ]    # [ タクトスイッチ0の取得値, 1の値, 2の値 ]

#-----------------------------------------------------------------------------#
# Input system (入力系)                                                       #
#-----------------------------------------------------------------------------#
def sensorinfo():
    # 距離センサの値を取得する
    # デバイスドライバに正常にアクセスできた場合 => tryの処理
    # デバイスドライバにアクセスできなかった場合 => exceptの処理
    # （正確には、tryの処理中にエラーが発生した場合にexceptの処理が実行される）
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
    # タクトスイッチの値を取得する
    # デバイスドライバに正常にアクセスできた場合 => tryの処理
    # デバイスドライバにアクセスできなかった場合 => exceptの処理
    # （正確には、tryの処理中にエラーが発生した場合にexceptの処理が実行される）
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
# Output system (出力系)                                                      #
#-----------------------------------------------------------------------------#
def buzzer( frequency ):
    # ブザーを鳴らす
    # 引数は鳴らす音の周波数(Hz)
    # デバイスドライバに正常にアクセスできた場合 => tryの処理
    # デバイスドライバにアクセスできなかった場合 => exceptの処理
    # （正確には、tryの処理中にエラーが発生した場合にexceptの処理が実行される）
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
    # モーターを駆動する
    # 引数は配列データ( speed = [ 左モータの回転数(Hz), 右モータの回転数(Hz) ] )
    # デバイスドライバに正常にアクセスできた場合 => tryの処理
    # デバイスドライバにアクセスできなかった場合 => exceptの処理
    # （正確には、tryの処理中にエラーが発生した場合にexceptの処理が実行される）
    try:
        for i, filename in enumerate( motor_driver ):
            with open( filename, "w" ) as f:
                f.write( str( int( speed[i] ) ) )
        ret = True
    except:
        # エラー発生時は返値としてFalseを返す
        ret = False
    return ret

def led( led_state ):
    # LEDを駆動する
    # 引数は配列データ( led_state = [ led_0, led_1, led_2,led_3 ] )
    # "led_X = 0" => Off , "led_X = 1" => ON
    # デバイスドライバに正常にアクセスできた場合 => tryの処理
    # デバイスドライバにアクセスできなかった場合 => exceptの処理
    # （正確には、tryの処理中にエラーが発生した場合にexceptの処理が実行される）
    try:
        for i,filename in enumerate( led_driver ):
            with open( filename, 'w' ) as f: 
                f.write( str( led_state[i] ) )
        ret = True
    except:
        # エラー発生時は返値としてFalseを返す
        ret = False
    return ret
