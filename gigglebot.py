import neopixel
import microbit

GET_FIRMWARE_VERSION = 1
# GET_MANUFACTURER = 2
GET_BOARD = 3
GET_VOLTAGE_BATTERY = 4
GET_LINE_SENSORS = 5
GET_LIGHT_SENSORS = 6
# GET_MOTOR_STATUS_RIGHT = 7
# GET_MOTOR_STATUS_LEFT = 8
# SET_MOTOR_POWER = 9
SET_MOTOR_POWERS = 10
LEFT = 0
RIGHT = 1
BOTH = 2
FORWARD = 1
BACKWARD = -1
DEFAULT_EYE_COLOR = (0, 0, 10)
LOW_VOLTAGE_EYE_COLOR = (10, 0, 0)
motor_power_left = 50
motor_power_right = 50

def _write8(*args, repeat=False):
    buf = bytearray(len(args))
    buf[0] = args[0]
    for i in range(1, len(args)):
        buf[i] = (args[i] & 0xFF)
    microbit.i2c.write(0x04, bytes(buf), repeat) 

def _read8(reg, repeat=False):
    microbit.i2c.write(0x04, bytes([reg]), repeat)
    outbuf = microbit.i2c.read(0x04, 1, repeat)
    return_value = outbuf[0]
    return return_value

def _read16(reg, repeat=False):
    microbit.i2c.write(0x04, bytes([reg]), repeat)
    outbuf = microbit.i2c.read(0x04, 2, repeat)
    return outbuf[0] * 255 + outbuf[1]

def _get_sensors(reg, repeat=False):
    microbit.i2c.write(0x04, bytes([reg]), repeat)
    outbuf = []
    buf = microbit.i2c.read(0x04, 3, repeat)
    outbuf.append(1023 - ( buf[0] << 2 | ((buf[2] & 0xC0) >> 6)))
    outbuf.append(1023 - ( buf[1] << 2 | ((buf[2] & 0x30) >> 4)))
    return outbuf

def volt():
    return (_read16(GET_VOLTAGE_BATTERY)/1000)

def drive(dir=FORWARD, milliseconds=-1):
    _write8(SET_MOTOR_POWERS, motor_power_left*dir, motor_power_right*dir)
    if milliseconds >= 0:
        microbit.sleep(milliseconds)
        stop()

def turn(dir=LEFT, milliseconds=-1):
    if dir==LEFT:
        _write8(SET_MOTOR_POWERS, motor_power_left, 0)
    if dir==RIGHT:
        _write8(SET_MOTOR_POWERS, 0, motor_power_right)
    if milliseconds >= 0:
        microbit.sleep(milliseconds)
        stop()        

def set_speed(power_left, power_right):
    global motor_power_left, motor_power_right
    motor_power_left = power_left
    motor_power_right = power_right

def stop():
        _write8(SET_MOTOR_POWERS, 0, 0)

def set_servo(which, degrees):
    '''
    Will set the left/right servo to a value between 0 and 180
    '''
    us = min(2400, max(600, 600 + (1800 * degrees // 180)))
    duty = round(us * 1024 * 50 // 1000000)
    if which == LEFT or which == BOTH:
        microbit.pin14.set_analog_period(20)
        microbit.pin14.write_analog(duty)
    if which == RIGHT or which == BOTH:
        microbit.pin13.set_analog_period(20)
        microbit.pin13.write_analog(duty)
        
def servo_off(which):
    if which == LEFT or which == BOTH:
        microbit.pin14.write_digital(0)
    if which == RIGHT or which == BOTH:
        microbit.pin13.write_digital(0)
    
def set_smile(R=25,G=0,B=0):
    '''
    Like all neopixel methods, this may return a ValueError if the colors are invalid
    '''
    for i in range(2,9):
        neopixelstrip[i] = (R,G,B)
    neopixelstrip.show()

def set_eyes(which=BOTH, R=0, G=0, B=10):
    '''
    Like all neopixel methods, this may return a ValueError if the colors are invalid
    '''
    if which != LEFT:
        neopixelstrip[0] = (R,G,B)
    if which != RIGHT:
        neopixelstrip[1]= (R,G,B)
    neopixelstrip.show()

def set_eye_color_on_start():
    if _read16(GET_VOLTAGE_BATTERY) < 3400:
        neopixelstrip[0] = LOW_VOLTAGE_EYE_COLOR
        neopixelstrip[1]= LOW_VOLTAGE_EYE_COLOR
    else:
        neopixelstrip[0] = DEFAULT_EYE_COLOR
        neopixelstrip[1]= DEFAULT_EYE_COLOR
    neopixelstrip.show()

def read_sensor(which_sensor, which_side):
    if (which_side == LEFT):
        return _get_sensors(which_sensor)[0]
    elif (which_side == RIGHT):
        return _get_sensors(which_sensor)[1]
    else:
        return _get_sensors(which_sensor)

def pixels_off():
    for i in range(9):
        neopixelstrip[i] = (0,0,0)
    neopixelstrip.show()
  
stop()
neopixelstrip = neopixel.NeoPixel(microbit.pin8, 9)
pixels_off()
eyestrip = neopixel.NeoPixel(microbit.pin8, 2)
set_eye_color_on_start()
