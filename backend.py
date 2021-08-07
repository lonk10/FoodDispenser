#!/usr/bin/env python3

import RPi.GPIO as GPIO
from hx711 import HX711
import time
import sys



print("Setup started")
#HX711 setup
scaleInt = HX711(5,6)
referenceUnit = 390
scaleInt.set_reading_format("MSB", "MSB")
scaleInt.set_reference_unit(referenceUnit)
scaleInt.reset()
scaleInt.tare()

#Servo setup
#GPIO.setmode(GPIO.BOARD) # Set GPIO numbering mode
GPIO.setup(18,GPIO.OUT) # Set pin 37 as an output, and set servo as pin 37 as PWM
servo = GPIO.PWM(18,50) # Note 11 is pin, 50 = 50Hz pulse
print("Setup finished")   

def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()    
    print("Bye!")
    sys.exit()

def setAngle(angle):
	duty = angle / 18 + 2
	#GPIO.output(03, True)
	servo.ChangeDutyCycle(duty)
	time.sleep(1)
	#GPIO.output(03, False)
	servo.ChangeDutyCycle(0)

def dispenseWeight(weight):
    print("Starting erogation")
    servo.start(0)
    time.sleep(2)
    startVal = scaleInt.get_weight(5)
    currentWeight = startVal
    print("Opening door")
    setAngle(0)
    #time.sleep(2)
    setAngle(180) #open door

    while currentWeight > startVal - weight: #check food erogation
        currentWeight = scaleInt.get_weight(5)
    print("Closing door")
    setAngle(0)
    #time.sleep(2)
    servo.stop()
    print("Erogation finished")

def main():   

    dispenseWeight(20)
    cleanAndExit()

if __name__ == "__main__":
    main()


