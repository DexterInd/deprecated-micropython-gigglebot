
# This file contains the documentation for gigglebot

import microbit

#: Left, either a left turn, or the left motor.
LEFT = 0
#: Right, either a right turn, or the right motor.
RIGHT = 1
#: indicates both motors.
BOTH = 2
#: Forward direction if the  motor power is positive. Please note that if the motor power is negative, this forward would become a backward. 
FORWARD = 1
#: Backward direction if the motor power is positive. Please note that if the motor power is negative, this backward would become a forward.
BACKWARD = -1
#: Power to the left motor. From -100 to 100. Negative numbers will end up reversing the movement. Default value is 50%.
motor_power_left = 50
#: Power to the right motor. From -100 to 100. Negative numbers will end up reversing the movement. Default value is 50%.
motor_power_right = 50
#: neopixel variable to control all neopixels. There are 9 neopixels on the Gigglebot. Pixel 0 is the right eye, pixel 1 is the left eye. Pixel 2 is the first of the rainbow pixel, on the right side. In order to control the neopixels, you must call :py:meth:`~init()` beforehand.
neopixelstrip = None

#: I2C command to query voltage level of the battery.
_GET_VOLTAGE_BATTERY = 4
#: I2C command to read the line sensors.
_GET_LINE_SENSORS = 5
#: I2C command to read the light sensors.
_GET_LIGHT_SENSORS = 6
#: I2C command to write new power values to the motor.
_SET_MOTOR_POWERS = 10

def _read(reg, size=8, repeat=False):
    microbit.i2c.write(0x04, bytes([reg]), repeat)
    outbuf = microbit.i2c.read(0x04, 1 if size==8 else 2, repeat)
    return outbuf[0] if size==8 else outbuf[0] * 255 + outbuf[1]

def _get_sensors(reg, repeat=False):
    microbit.i2c.write(0x04, bytes([reg]), repeat)
    outbuf = []
    buf = microbit.i2c.read(0x04, 3, repeat)
    outbuf.append(1023 - ( buf[0] << 2 | ((buf[2] & 0xC0) >> 6)))
    outbuf.append(1023 - ( buf[1] << 2 | ((buf[2] & 0x30) >> 4)))
    return outbuf

def init(): 
    """
    Loads up the neopixel library and sets up the neopixelstrip variable for later use.

    .. important::
        It is possible to use the Gigglebot without calling this method but the leds will not work.
        Should you need more RAM space, you can choose to ignore the neopixels.
    """
    from neopixel import NeoPixel
    global neopixelstrip
    stop()
    neopixelstrip = NeoPixel(microbit.pin8, 9); pixels_off()
    set_eye_color_on_start()

def drive(dir=FORWARD, milliseconds=-1):
    '''
    This results in the Gigglebot driving FORWARD or BACKWARD. 

    :param int dir = FORWARD: Possible values are FORWARD (1) or BACKWARD (-1). Please note there are no tests done on this value. One could theoretically use 2 to double the speed.
    :param int milliseconds = -1: If this parameter is omitted, or a negative value is supplied, the robot will keep on going until told to do something else, like turning or stopping. If a positive value is supplied, the robot will drive for that quantity of milliseconds.
    '''
    microbit.i2c.write(0x04, bytes([_SET_MOTOR_POWERS, motor_power_left*dir, motor_power_right*dir]), False)
    if milliseconds >= 0:
        microbit.sleep(milliseconds)
        stop()

def turn(dir=LEFT, milliseconds=-1):
    if dir==LEFT: microbit.i2c.write(0x04, bytes([_SET_MOTOR_POWERS, motor_power_left, 0]), False)
    if dir==RIGHT: microbit.i2c.write(0x04, bytes([_SET_MOTOR_POWERS, 0, motor_power_right]), False)
    if milliseconds >= 0:
        microbit.sleep(milliseconds)
        stop()        

def set_speed(power_left, power_right):
    global motor_power_left, motor_power_right
    motor_power_left = power_left
    motor_power_right = power_right

def stop():
    microbit.i2c.write(0x04, bytes([_SET_MOTOR_POWERS, 0, 0]), False)

def set_smile(R=25,G=0,B=0):
    """
    Controls the color of the smile neopixels, all together. 

    :param int R = 25: the red component of the color, from 0 to 254
    :param int G =  0: the green component of the color, from 0 to 254
    :param int B =  0: the blue component of the color, from 0 to 254
    
    """
    neopix = range(2,9)
    for i in neopix: neopixelstrip[i] = (R,G,B)
    neopixelstrip.show()

def set_eyes(which=BOTH, R=0, G=0, B=10):
    """
    Controls the color of the two eyes, each one individually or both together.

    :param int which = BOTH: either LEFT (0), RIGHT (1), or BOTH (2)
    :param int R =  0: the red component of the color, from 0 to 254
    :param int G =  0: the green component of the color, from 0 to 254
    :param int B = 10: the blue component of the color, from 0 to 254
    """
    if which != LEFT: neopixelstrip[0]=(R,G,B)
    if which != RIGHT: neopixelstrip[1]=(R,G,B)
    neopixelstrip.show()

def set_eye_color_on_start():
    if _read(_GET_VOLTAGE_BATTERY, size=16) < 3400:
        neopixelstrip[0]=(10, 0, 0)
        neopixelstrip[1]=(10, 0, 0)
    else:
        neopixelstrip[0]=(0, 0, 10)
        neopixelstrip[1]=(0, 0, 10)
    neopixelstrip.show()

def pixels_off():
    """

    """
    for i in range(9):
        neopixelstrip[i] = (0,0,0)
    neopixelstrip.show()

def set_servo(which, degrees):
    us = min(2400, max(600, 600 + (1800 * degrees // 180)))
    duty = round(us * 1024 * 50 // 1000000)
    if which == LEFT or which == BOTH:
        microbit.pin14.set_analog_period(20)
        microbit.pin14.write_analog(duty)
    if which == RIGHT or which == BOTH:
        microbit.pin13.set_analog_period(20)
        microbit.pin13.write_analog(duty)
        
def servo_off(which):
    if which == LEFT or which == BOTH: microbit.pin14.write_digital(0)
    if which == RIGHT or which == BOTH: microbit.pin13.write_digital(0)
    

def read_sensor(which_sensor, which_side):
    if (which_side == LEFT): return _get_sensors(which_sensor)[0]
    elif (which_side == RIGHT): return _get_sensors(which_sensor)[1]
    else: return _get_sensors(which_sensor)


def volt():
    return (_read(_GET_VOLTAGE_BATTERY, size=16)/1000)
