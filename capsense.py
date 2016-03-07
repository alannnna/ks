#!/user/bin/env python

'''
Code from: https://bitbucket.org/boblemarin/raspberrypi-capacitive-sensor/src/1c18fad88ae70ce1d83dee9c43528e27664a150d/CapSense1/CapSenseAndLEDs.py?at=master&fileviewer=file-view-default

Demo here: https://www.youtube.com/watch?v=OoPmEQdDsrs
'''

import RPi.GPIO as GPIO, time

timeout = 10000
total = 0
DEBUG = 1
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def CapRead(inPin,outPin):
    total = 0
    
    # set Send Pin Register low
    GPIO.setup(outPin, GPIO.OUT)
    GPIO.output(outPin, GPIO.LOW)
    
    # set receivePin Register low to make sure pullups are off 
    GPIO.setup(inPin, GPIO.OUT)
    GPIO.output(inPin, GPIO.LOW)
    GPIO.setup(inPin, GPIO.IN)
    
    # set send Pin High
    GPIO.output(outPin, GPIO.HIGH)
    
    # while receive pin is LOW AND total is positive value
    while( GPIO.input(inPin) == GPIO.LOW and total < timeout ):
        total+=1
    
    if ( total > timeout ):
        return -2 # total variable over timeout
        
     # set receive pin HIGH briefly to charge up fully - because the while loop above will exit when pin is ~ 2.5V 
    GPIO.setup( inPin, GPIO.OUT )
    GPIO.output( inPin, GPIO.HIGH )
    GPIO.setup( inPin, GPIO.IN )
    
    # set send Pin LOW
    GPIO.output( outPin, GPIO.LOW ) 

    # while receive pin is HIGH  AND total is less than timeout
    while (GPIO.input(inPin)==GPIO.HIGH and total < timeout) :
        total+=1
    
    if ( total >= timeout ):
        return -2
    else:
        return total


# init LEDs sequence
leds = [27,22,23,24,25,10,8,7]

for i in leds:
    GPIO.setup( i,GPIO.OUT )

for l in range(0,10):
    for i in leds:
        GPIO.output( i,GPIO.HIGH )
    time.sleep(0.1)
    for i in leds:
        GPIO.output( i,GPIO.LOW )
    time.sleep(0.1)

# loop
while True:
    total = 0
    for j in range(0,10):
        total += CapRead(18,17);
    for j in range(len(leds)):
        if ( (total-40) / 16 > j ):
            GPIO.output( leds[j],GPIO.HIGH )
        else:
            GPIO.output( leds[j],GPIO.LOW )

    
# clean before you leave
GPIO.cleanup()
