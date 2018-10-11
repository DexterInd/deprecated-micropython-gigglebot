
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

#: I2C command to read the line sensors.
LINE_SENSOR = 5
#: I2C command to read the light sensors.
LIGHT_SENSOR = 6
#: I2C command to query voltage level of the battery.
_GET_VOLTAGE_BATTERY = 4
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
    
    :returns: the neopixel strip 
    """
    from neopixel import NeoPixel
    global neopixelstrip
    stop()
    neopixelstrip = NeoPixel(microbit.pin8, 9); pixels_off()
    set_eye_color_on_start()
    return neopixelstrip

def drive(dir=FORWARD, milliseconds=-1):
    '''
    This results in the Gigglebot driving FORWARD or BACKWARD. 

    The following snippet of code will see the gigglebot drive forward for a second:

        .. code-block:: python

            from gigglebot import *
            drive(FORWARD, 1000)
    
    And this snippet of code will do the same thing:

        .. code-block:: python

            import gigglebot
            gigglebot.drive(gigglebot.FORWARD, 1000)

    :param int dir = FORWARD: Possible values are FORWARD (1) or BACKWARD (-1). Please note there are no tests done on this value. One could theoretically use 2 to double the speed.
    :param int milliseconds = -1: If this parameter is omitted, or a negative value is supplied, the robot will keep on going until told to do something else, like turning or stopping. If a positive value is supplied, the robot will drive for that quantity of milliseconds.
    '''
    microbit.i2c.write(0x04, bytes([_SET_MOTOR_POWERS, int(motor_power_left*dir) & 0xFF, int(motor_power_right*dir) & 0xFF]), False)
    if milliseconds >= 0:
        microbit.sleep(milliseconds)
        stop()

def turn(dir=LEFT, milliseconds=-1):
    """
    Will get the gigglebot to turn left or right by temporarily removing power to one wheel.

    :param int dir=LEFT: Either LEFT (0) or RIGHT (1) to determine the direction of the turn.
    :param int milliseconds=-1: If this parameter is omitted, or a negative value is supplied, the robot will keep on going until told to do something else, like turning or stopping. If a positive value is supplied, the robot will drive for that quantity of milliseconds.
    """
    if dir==LEFT: microbit.i2c.write(0x04, bytes([_SET_MOTOR_POWERS, int(motor_power_left) & 0xFF, 0]), False)
    if dir==RIGHT: microbit.i2c.write(0x04, bytes([_SET_MOTOR_POWERS, 0, int(motor_power_right) & 0xFF]), False)
    if milliseconds >= 0:
        microbit.sleep(milliseconds)
        stop()        

def set_speed(power_left, power_right):
    """
    Assigns left and right motor powers. If both are the same speed, the GiggleBot will go mostly straight.

    .. note::
       It is possible that the GiggleBot does not go straight by default. If so, you need to adjust the speed of each motor to correct the course of the robot.
    """
    global motor_power_left, motor_power_right
    motor_power_left = power_left
    motor_power_right = power_right

def stop():
    """
    Stops the GiggleBot right away.
    """
    microbit.i2c.write(0x04, bytes([_SET_MOTOR_POWERS, 0, 0]), False)

def set_smile(R=25,G=0,B=0):
    """
    Controls the color of the smile neopixels, all together. 

    :param int R = 25: Red component of the color, from 0 to 254.
    :param int G =  0: Green component of the color, from 0 to 254.
    :param int B =  0: Blue component of the color, from 0 to 254.
    
    """
    neopix = range(2,9)
    for i in neopix: neopixelstrip[i] = (R,G,B)
    neopixelstrip.show()

def set_eyes(which=BOTH, R=0, G=0, B=10):
    """
    Controls the color of the two eyes, each one individually or both together.

    :param int which = BOTH: either LEFT (0), RIGHT (1), or BOTH (2).
    :param int R =  0: Red component of the color, from 0 to 254.
    :param int G =  0: Green component of the color, from 0 to 254.
    :param int B = 10: Blue component of the color, from 0 to 254.
    """
    if which != LEFT: neopixelstrip[0]=(R,G,B)
    if which != RIGHT: neopixelstrip[1]=(R,G,B)
    neopixelstrip.show()

def set_eye_color_on_start():
    """
    Sets the eye color to blue if the batteries are good, to red if the batteries are running low.
    This is called by the :py:meth:`~init()`, usually at the start of the program.
    You are free to call this method whenever you want if you need to keep a closer watch on the voltage level.
    """
    if _read(_GET_VOLTAGE_BATTERY, size=16) < 3400:
        neopixelstrip[0]=(10, 0, 0)
        neopixelstrip[1]=(10, 0, 0)
    else:
        neopixelstrip[0]=(0, 0, 10)
        neopixelstrip[1]=(0, 0, 10)
    neopixelstrip.show()

def pixels_off():
    """
    Turns all neopixels off, both eyes and smile.
    """
    for i in range(9):
        neopixelstrip[i] = (0,0,0)
    neopixelstrip.show()

def set_servo(which=LEFT, degrees=90):
    """
    :param int which: Which servo to control: LEFT (0),  RIGHT (1), or BOTH (2).
    :param int degrees: Position of the servo, from 0 to 180. 

    .. note::

       Moving the servo is not instantaneous. It is possible that you will need to give it time to reach its final position.

       The following is an example that will get the servo moving from 0 to 180 degrees every second.

       .. code::

          from gigglebot import *
          import microbit
          while True:
              set_servo(BOTH, 0)
              microbit.sleep(1000) # sleeps for 1000 milliseconds
              set_servo(BOTH, 180)
              microbit.sleep(1000) # sleeps for 1000 milliseconds
    """
    us = min(2400, max(600, 600 + (1800 * degrees // 180)))
    duty = round(us * 1024 * 50 // 1000000)
    if which == LEFT or which == BOTH:
        microbit.pin14.set_analog_period(20)
        microbit.pin14.write_analog(duty)
    if which == RIGHT or which == BOTH:
        microbit.pin13.set_analog_period(20)
        microbit.pin13.write_analog(duty)
        
def servo_off(which):
    """
    Removes power from the servo.

    :param int which: Determines which servo, LEFT (0), RIGHT (1), BOTH (2).
    """
    if which == LEFT or which == BOTH: microbit.pin14.write_digital(0)
    if which == RIGHT or which == BOTH: microbit.pin13.write_digital(0)
    

def read_sensor(which_sensor, which_side):
    """
    Reads the GiggleBot onboard sensors, light or line sensors.

    :param int which_sensor: Reads the light sensors LIGHT_SENSOR (6), or the line sensors LINE_SENSOR (5). Values are from 0 to 1023.
    :param int which_side: Reads LEFT (0), RIGHT (1), or BOTH (2) sensors. When reading both sensors, an array will be returned.

    :returns: either an integer or an array of integers (left, then right)

    You can read the sensors this way:

    .. code::

       left, right = read_sensor(LIGHT_SENSOR, BOTH)

    """
    right, left = _get_sensors(which_sensor)
    if(which_side==LEFT): return left
    elif(which_side==RIGHT): return right
    else: return (left, right)


def volt():
    """
    Returns the voltage level of the batteries

    :returns: voltage level of the batteries.
    """
    return (_read(_GET_VOLTAGE_BATTERY, size=16)/1000)
