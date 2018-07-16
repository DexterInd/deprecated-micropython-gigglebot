import neopixel
import microbit
import time

I2C_GET_FIRMWARE_VERSION = 1
I2C_GET_MANUFACTURER=2
I2C_GET_BOARD=3
I2C_GET_VOLTAGE_BATTERY=4
I2C_GET_LINE_SENSORS=5
I2C_GET_LIGHT_SENSORS=6
I2C_GET_MOTOR_STATUS_RIGHT=7
I2C_GET_MOTOR_STATUS_LEFT=8
I2C_SET_MOTOR_POWER = 9
I2C_SET_MOTOR_POWERS = 10
LEFT = 0
RIGHT = 1
BOTH = 2

DEFAULT_MOTOR_POWER_LEFT = 50
DEFAULT_MOTOR_POWER_RIGHT = 50

motor_power_left = DEFAULT_MOTOR_POWER_LEFT
motor_power_right = DEFAULT_MOTOR_POWER_RIGHT

class GiggleBot():
    def __init__(self):
        self.default_speed_left = 50
        self.default_speed_right = 50
        self.neopixelstrip = neopixel.NeoPixel(microbit.pin8,9)
        self.neopixelstrip[0] = (0,0,10)
        self.neopixelstrip[1]= (0,0,10)
        for i in range(2,9):
            self.neopixelstrip[i] = (10,0,0)
        self.neopixelstrip.show()
        self.stop()

    def _write(self,*args):
        if len(args) == 1: args = args[0]
        microbit.i2c.write(0x04,bytes(args))
        
    def drive(self, seconds=-1):
        self._write(I2C_SET_MOTOR_POWERS, motor_power_left, motor_power_right)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()
            
    def turn(self, dir=LEFT, seconds=-1):
        if dir==LEFT:
            self._write(I2C_SET_MOTOR_POWERS, motor_power_left, 0)
        if dir==RIGHT:
            self._write(I2C_SET_MOTOR_POWERS, 0, motor_power_right)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()        
        
    def speed(self,power_left, power_right):
        motor_power_left = power_left
        motor_power_right = power_right
        self.drive()

    def stop(self):
        self._write(I2C_SET_MOTOR_POWERS, 0, 0)
        
    def smile(self,R=25,G=0,B=0):
        '''
        Like all neopixel methods, this may return a ValueError if the colors are invalid
        '''
        for i in range(2,9):
            self.neopixelstrip[i] = (R,G,B)
        self.neopixelstrip.show()
        
    def eyes(self, which=BOTH, R=0, G=0, B=10):
        '''
        Like all neopixel methods, this may return a ValueError if the colors are invalid
        '''
        if which != LEFT:
            self.neopixelstrip[0] = (R,G,B)
        if which != RIGHT:
            self.neopixelstrip[1]= (R,G,B)
        self.neopixelstrip.show()
        
        
