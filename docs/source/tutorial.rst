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

