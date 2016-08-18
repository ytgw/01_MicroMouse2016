#-----------------------------------------------------------------------------#
# Declataion                                                                  #
#-----------------------------------------------------------------------------#
sensor_driver  = "/dev/rtlightsensor0"
switch_driver  = [ "/dev/rtswitch0", "/dev/rtswitch1"]
buzzer_driver  = "/dev/rtbuzzer0"
motor_driver   = [ "/dev/rtmotor_raw_l0", "/dev/rtmotor_raw_r0"]
led_driver     = [ "/dev/rtled0", "/dev/rtled1", "/dev/rtled2", "/dev/rtled3"] 

sensor_data  = [0, 0, 0, 0]
switch_state = [0, 0, 0]

#-----------------------------------------------------------------------------#
# Input system                                                                #
#-----------------------------------------------------------------------------#
def sensorinfo():
    try:
        filename = sensor_driver
        with open(filename,"r") as f:
            # f.readlin() is 8 byte data
            # => (str(value0), " ",str(value1), " ",str(value2), " ",str(value3), "\n"
            val = f.readline()
    except:
        val = ["255", "", "255", "", "255", "", "255"]
    info = [int(val[0]), int(val[2]), int(val[4]), int(val[6])]
    return info

def switchstate():
    try:
        for i, filename in enumerate(switch_driver):
            with open(filename,"r") as f:
                # f.readlin() is 2 byte data => "0\n" or "1\n"
                temp = f.readline()
                switch_state[i] = int(temp[0])
    except:
        switch_state = [-1, -1, -1]
    return switch_state

#-----------------------------------------------------------------------------#
# Output system                                                               #
#-----------------------------------------------------------------------------#
def buzzer(frequency):
    try:
        filename = buzzer_driver
        with open(filename,"w") as f:
            f.write(frequency)
        ret = True
    except:
        ret = False
    return ret

def motor(speed):
    # speed = [ left_speed, right_speed]
    try:
        for i, filename in enumerate(motor_driver):
            with open(filename,"w") as f_r_m:
                f.write(str(speed[i]))
        ret = True
    except:
        ret = False
    return ret

def led(led_state):
    # led_state = [ led_0, led_1, led_2,led_3]
    # "led_X = 0" is Off State, and "led_X = 1" is On State
    try:
        for i,filename in enumerate(led_driver):
            with open(filename,'w') as f: 
                f.write(led_state[i])
        ret = True
    except:
        ret = False
    return ret