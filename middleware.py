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
sensor_data  = [0, 0, 0, 0] # [距離センサー0の取得値, 1の値, 2の値, 3の値]  
switch_state = [0, 0, 0]    # [タクトスイッチ0の取得値, 1の値, 2の値]

#-----------------------------------------------------------------------------#
# Input system (入力系)                                                       #
#-----------------------------------------------------------------------------#
def sensorinfo():
    # 距離センサの値を取得する
    # デバイスドライバが見つかった場合 => tryの処理
    # デバイスドライバが見つからなかった場合 => exceptの処理
    try:
        filename = sensor_driver
        with open(filename,"r") as f:
            # f.readlin() の返り値は 8要素の配列データ(すべての要素は文字列)
            # 要素0 = 距離センサ0の取得値(文字列)
            # 要素1 = スペース(文字列)
            # 要素2 = 距離センサ1の取得値(文字列)
            # 要素3 = スペース(文字列)
            # 要素4 = 距離センサ2の取得値(文字列)
            # 要素5 = スペース(文字列)
            # 要素6 = 距離センサ3の取得値(文字列)
            # 要素7 = \n(改行コード)
            temp = f.readline()
            # デバイスドライバから取得できる値は文字列なので数値に変換する
            # 要素1,要素3, 要素5のスペースを削除
            # 要素7の改行コードを削除
            info = [int(temp[0]), int(temp[2]), int(temp[4]), int(temp[6])]
    except:
        # デバイスドライバが見つからない場合は全ての要素に数値の255を代入する
        info = [ 255, 255, 255, 255 ]
    sensor_info = info 
    return sensor_info

def switchstate():
    # タクトスイッチの値を取得する
    # デバイスドライバが見つかった場合 => tryの処理
    # デバイスドライバが見つからなかった場合 => exceptの処理
    try:
        for i, filename in enumerate(switch_driver):
            with open(filename,"r") as f:
                # f.readlin() の返り値は 2要素の配列データ(すべての要素は文字列)
                # 要素0 = "0":押されてない or "1":押されている
                # 要素1 = \n(改行コード)
                temp = f.readline()
                # デバイスドライバから取得できる値は文字列なので数値に変換する
                # 要素1は改行コードなので削除
                state[i] = int(temp[0])
    except:
        # デバイスドライバが見つからない場合は全ての要素に数値の-1を代入する
        state = [ -1, -1, -1 ]
    switch_state = state
    return switch_state

#-----------------------------------------------------------------------------#
# Output system (出力系)                                                      #
#-----------------------------------------------------------------------------#
def buzzer(frequency):
    # ブザーを鳴らす
    # 引数は鳴らす音の周波数(Hz)
    # デバイスドライバが見つかった場合 => tryの処理
    # デバイスドライバが見つからなかった場合 => exceptの処理
    try:
        filename = buzzer_driver
        with open(filename,"w") as f:
            f.write(int(frequency))
        ret = True
    except:
        ret = False
    return ret

def motor(speed):
    # モーターを駆動する
    # 引数は配列データ( speed = [ 左モータの回転数(Hz), 右モータの回転数(Hz) ] )
    # デバイスドライバが見つかった場合 => tryの処理
    # デバイスドライバが見つからなかった場合 => exceptの処理
    try:
        for i, filename in enumerate(motor_driver):
            with open(filename,"w") as f:
                f.write(str(int(speed[i])))
        ret = True
    except:
        ret = False
    return ret

def led(led_state):
    # LEDを駆動する
    # 引数は配列データ( led_state = [ led_0, led_1, led_2,led_3 ] )
    # "led_X = 0" => Off , "led_X = 1" => ON
    # デバイスドライバが見つかった場合 => tryの処理
    # デバイスドライバが見つからなかった場合 => exceptの処理
    try:
        for i,filename in enumerate(led_driver):
            with open(filename,'w') as f: 
                f.write(led_state[i])
        ret = True
    except:
        ret = False
    return ret