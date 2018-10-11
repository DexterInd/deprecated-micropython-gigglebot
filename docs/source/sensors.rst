Sensors tutorial
================

The GiggleBot comes with a couple of onboard sensors:

#. Two light sensors, near the front eyes LEDs.
#. Two line sensors, on the underside of the line follower.

Light Sensors
-------------

The GiggleBot comes with two light sensors right in front of the LED on each eye. They are very small and easy to miss. 
However, they are more versatile than the Micro:Bit's light sensor as they can be read together to detect which side is receiving more light.

The main method to query the light sensors is :py:meth:`~gigglebot.read_sensor()`.  The same method is used for both light sensors and line sensors. 

Here's how to read both light sensors in one call:

.. code::

   left, right = read_sensor(LIGHT_SENSOR, BOTH)

And here's how to read just one side at a time:

.. code::

   right = read_sensor(LIGHT_SENSOR, RIGHT)


Chase the Light
^^^^^^^^^^^^^^^

This tutorial will turn the GiggleBot into a cat, following a spotlight on the 
floor. Many cats do that when you shine a flashlight in front of them, they will 
try to hunt the light spot. When running this code, you will be able to guide 
your GiggleBot by using a flashlight. 

This is how to use this project:

#. Start GiggleBot and wait for sleepy face to appear on the Micro:Bit.
#. Press button A to start the Chase the Light game (heart will replace the sleepy face).
#. Chase the light as long as you want.
#. Press button B to stop the GiggleBot and display sleepy face again.

First, a bit of explanation on the algorithm being used here.

On starting the GiggleBot, the Micro:Bit will:

#. Assign a value to the `diff` variable (here it is using 10).
#. Display a sleepy face image.
#. Resets whatever readings from the buttons it might have had.
#. Start a forever loop.

This forever loop only waits for one thing: 
for the user to press button A, and that's when the light chasing begins.

As soon as button A is pressed, the Micro:Bit will display a heart as it's 
quite happy to be active! And then it starts a second forever loop! This second 
forever loop is the actual Light Chasing game. It will end when button B is 
pressed by the user.

How to Chase a Light:

#. Take reading from both light sensors.
#. Compare the readings, using `diff` to allow for small variations. You will most likely get absolutely identical readings, even if the light is mostly equal. Using a differential value helps stabilize the behavior. You can adapt to your own lighting conditions by changing this value.
#. If the right sensor reads more than the left sensor plus the `diff` value, then we know it's brighter to the right. Turn right.
#. If the left sensor reads more than the right sensor plus the `diff` value, then it's brighter to the left. Turn left.
#. If there isn't that much of a difference between the two sensors, go straight. 
#. If button B gets pressed at any time, stop the robot, change sleepy face, and get out of this internal loop. The code will fall back to the first loop, ready for another game.



.. code::

   from gigglebot import *
   # value for the differential between the two sensors.
   # you can change this value to make it more or less sensitive.
   diff = 10
   # display sleepy face
   microbit.display.show(microbit.Image.ASLEEP)
   # the following two lines resets the 'was_pressed' info 
   # and discards any previous presses
   microbit.button_a.was_pressed()
   microbit.button_b.was_pressed()

   # start first loop, waiting for user input
   while True:
       # test for user input
       if microbit.button_a.was_pressed():
           # game got started! Display much love
           microbit.display.show(microbit.Image.HEART)

           # start game loop
           while True:
               # read both sensors
               left, right = read_sensor(LIGHT_SENSOR, BOTH)

               # test if it's brighter to the right
               if right > left+diff:
                   turn(RIGHT)

               # test if it's brighter to the left 
               elif left > right+diff:
                   turn(LEFT)

               # both sides being equal, go straight
               else:
                   drive(FORWARD)

               # oh no, the game got interrupted
               if microbit.button_b.is_pressed():
                   stop()
                   microbit.display.show(microbit.Image.ASLEEP)

                   # this line here gets us out of the game loop
                   break

What else can be done with the light sensors?

You could modify this code to turn the GiggleBot into a night insect? Those would 
avoid light instead of chasing it. 

You could detect when it gets dark or bright. Imagine the GiggleBot inside your 
closet. When someone opens the door, the sudden light can be detected. The GiggleBot 
can let you know someone went through your things while you were away.

Line Sensors
------------

In front of GiggleBot, attached to the body, there is a line follower sensor. 
It contains two line sensors. You can spot them from the top of the line 
follower by two white dots. And from the bottom, they are identified as *R* and 
*L* (for *right* and *left*)

.. figure::  _static/images/GigglebotLineFollowingSensors.jpg
   :align:   center
   :alt: sensors underneath the line follower

*photo courtesy of Les Pounder*


The easiest way of reading the sensors is as follow:

.. code::

   from gigglebot import *
   left, right = read_sensor(LINE_SENSOR, BOTH)

The lower the number, the darker it is reading. Values can go from 0 to 1023 
and depend a lot on your environment. If you want to write a line follower 
robot, it is best to take a few readings first, to get a good idea of what
numbers will represent a black line, and what numbers represent a white line.

Calibrating the Line Follower
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Calibrating the line follower means figuring out which numbers get returned
when it's over a black line, so that you can later code an actual line
follower robot. 

The best approach for this is to get readings in various parts of your line, 
from both sensors, for both the black line and the background color.

The following code will display the values onto the microbit leds when you 
press button A, allowing you to manually position your robot around your 
circuit and take readings.

.. code::

   from gigglebot import *
   # reset all previous readings of button_a
   # strictly speaking this is not necessary, it is just a safety thing
   microbit.button_a.was_pressed()
   while True:
       if microbit.button_a.is_pressed():
           left, right = read_sensor(LINE_SENSOR, BOTH)
           microbit.display.scroll(left)
           microbit.display.scroll(right)

Follow the Line
^^^^^^^^^^^^^^^

Once you have gotten readings from the line sensors, you are ready to code
a line follower robot. 

Here we are coding for a line that is thick enough that both sensors can 
potentially be over the line. The robot will stop if it loses track of the line, 
in other words, if both sensors detect they're over the background color.

The logic will be as follow:

#. If both sensors detect a black line, forge straight ahead.
#. If neither sensor detects a black line, give up and stop.
#. If the right sensor detects a black line but not the left sensor, then steer to the right.
#. If the left sensor detects a black line but not the right sensor, then steer to the left.

We are also using the LEDs on the LED smile to indicate what is going on while
we follow the line. 

.. code::

   from gigglebot import *
   # reset all previous readings of button_a, and button_b
   # strictly speaking this is not necessary, it is just a safety thing
   microbit.button_a.was_pressed()
   microbit.buttom_b.was_pressed()
   microbit.display.show(microbit.Image.YES)
   strip=init()
   # speed needs to be set according to your line and battery level.
   # do not go too fast though. 
   set_speed(60, 60)
   # threshold is a little over the highest number you got that indicates a 
   # black line.
   threshold = 90
   while True:
       # if both buttons are pressed, run calibration code
       if microbit.button_a.is_pressed() and microbit.button_b.is_pressed():
           left, right = read_sensor(LINE_SENSOR, BOTH)
           microbit.display.scroll(left)
           microbit.display.scroll(right)
       # if button A is pressed run line following code until button B gets pressed
       # or until we're over white/background
       if microbit.button_a.is_pressed():
           while not microbit.button_b.is_pressed():
               left, right = read_sensor(LINE_SENSOR, BOTH)
               if left < threshold and right < threshold:
                   # both sensors detect the line
                   strip[2]=(0,255,0)
                   strip[8]=(0,255,0)
                   strip.show()
                   drive(FORWARD)
               elif right > threshold and left > threshold:
                   # neither sensor detects the line
                   stop()
                   strip[2]=(255,0,0)
                   strip[8]=(255,0,0)
                   strip.show()
                   break
               elif left > threshold and right < threshold:
                  # only the right sensor detects the line
                   strip[2]=(0,255,0)
                   strip[8]=(0,0,0)
                   strip.show()
                   turn(RIGHT)
               elif right > threshold and left < threshold:
                   # only the left sensor detects the line
                   strip[2]=(0,0,0)
                   strip[8]=(0,255,0)
                   strip.show()
                   turn(LEFT)
           stop()