""" 
This file helps you do hardware checks on the Raspberry Pi.
You can check whether the IO pins are working correctly by running this file.
"""

# test lock

import RPi.GPIO as GPIO

lock = 21

# the following lines set up the GPIO pins
GPIO.setwarnings(False) # Ignore warning for now
GPIO.cleanup() # clean up at the end of your script
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
GPIO.setup(lock, GPIO.OUT) # Set pin 21 to be an output pin and set initial value to be low (off)

GPIO.output(lock, True)

print(GPIO.input(lock) == 1) # should be True
