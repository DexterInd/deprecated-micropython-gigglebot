Sensors tutorial
================

The GiggleBot comes with a couple of onboard sensors:

#. two light sensors, near the front eyes LEDs,
#. two line sensors, on the underside of the line follower.

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

#. start GiggleBot and wait for sleepy face to appear on the Micro:Bit,
#. press button A to start the Chase the Light game (heart will replace the sleepy face),
#. chase the light as long as you want,
#. press button B to stop the GiggleBot and display sleepy face again.

First, a bit of explanation on the algorithm being used here.

On starting the GiggleBot, the Micro:Bit will:

#. assign a value to the `diff` variable (here it is using 10),
#. display a sleepy face image,
#. resets whatever readings from the buttons it might have had, 
#. then start a forever loop.

This forever loop only waits for one thing: 
for the user to press button A, and that's when the light chasing begins.

As soon as button A is pressed, the Micro:Bit will display a heart as it's 
quite happy to be active! And then it starts a second forever loop! This second 
forever loop is the actual Light Chasing game. It will end when button B is 
pressed by the user.

How to chase a light:

#. take reading from both light sensors,
#. compare the readings, using `diff` to allow for small variations. You will most likely get absolutely identical readings, even if the light is mostly equal. Using a differential value helps stabilize the behavior. You can adapt to your own lighting conditions by changing this value.
#. if the right sensor reads more than the left sensor plus the `diff` value, then we know it's brighter to the right. Turn right.
#. if the left sensor reads more than the right sensor plus the `diff` value, then it's brighter to the left. Turn left.
#. if there isn't that much of a difference between the two sensors, go straight. 
#. if button B gets pressed at any time, stop the robot, change sleepy face, and get out of this internal loop. The code will fall back to the first loop, ready for another game.



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

