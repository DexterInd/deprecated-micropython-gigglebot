Tutorial for GiggleBot
======================

This is a tutorial on how to control your gigglebot

Take the GiggleBot on a stroll
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This first tutorial will demonstrate how to control the robot's movements. 
The GiggleBot will :

#. set its speed to 75% of its maximum power (default is 50%)
#. go forward for a second, 
#. go backward for a second,
#. wait for a second,
#. turn left for half a second,
#. turn right for half a second.

.. code::

   from gigglebot import *
   set_speed(75,75)
   drive(FORWARD,1000)
   drive(BACKWARD,1000)
   microbit.sleep(1000)
   turn(LEFT,500)
   turn(RIGHT,500)

.. note::

   There is no need to make use of the :py:meth:`~gigglebot.stop()` method here because each of those timed functions will make sure the robot stops at the end of the delay.

.. note::

   :py:meth:`~gigglebot.init()` does not need to be called in this example as we are not making use of the lights on the robot.


Big Smile
^^^^^^^^^

Let's use the Neopixels to turn the smile leds to a nice red, followed by green and then blue.

.. code::

   from gigglebot import *
   init()
   while True:
       set_smile(R=100,G=0,B=0)
       microbit.sleep(500)
       set_smile(R=0,G=100,B=0)
       microbit.sleep(500)
       set_smile(R=0,G=0,B=100)
       microbit.sleep(500)

Rainbow Smile
^^^^^^^^^^^^^

You are not limited to the basic red,green,blue colors as they can be mixed. Let's create a rainbow of colors! 
The :py:meth:`~gigglebot.init()` method returns a variable that lets you control each neopixel individually. 
We'll make use of this to create a rainbow.

.. code::

   from gigglebot import *
   strip=init()
   strip[2]=(255,0,0)
   strip[2]=(248,12,18)
   strip[3]=(255,68,34)
   strip[4]=(255,153,51)
   strip[5]=(208,195,16)
   strip[6]=(34,204,170)
   strip[7]=(51,17,187)
   strip[8]=(68, 34, 153)
   strip.show()


Rainbow Cycle
^^^^^^^^^^^^^

Here is how you can get the smile to cycle through the colours of the rainbow.

.. code::

   from gigglebot import *

   # first define the colors of the rainbow in an array
   colors = []
   colors.append((255,0,0))
   colors.append((248,12,18))
   colors.append((255,68,34))
   colors.append((255,153,51))
   colors.append((208,195,16))
   colors.append((34,204,170))
   colors.append((51,17,187))
   colors.append((68, 34, 153))

   strip=init()

   # offset will let us know which colour is due to be displayed on which LED
   offset = 0

   # Looping forever
   while True:
       offset = offset + 1

       # we might run into an issue of trying to display color 8 - which doesn't exist - on LED 7
       # we need to catch that case before it crashes the code.
       if offset > 7:
           offset = 0
       for i in range(7):
           if i+offset > 7: 
               colind = i+offset-7
           else:
               colind = i+offset
           strip[i+2]=colors[colind]
       # display the colors 
       strip.show()
       # wait a bit for the human eye to catch the colors in question
       microbit.sleep(100)
   # colors were taken from http://colrd.com/palette/22198/?download=css


