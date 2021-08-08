#!/usr/bin/env python3

import RPi.GPIO as GPIO
from hx711 import HX711
import time
import sys


class Backend:

    def __init__(self, dout=5, pd_sck=6, servo_pin=18):
        print("Setup started")
        #HX711 setup
        self.scaleInt = HX711(dout, pd_sck)
        referenceUnit = 390
        self.scaleInt.set_reading_format("MSB", "MSB")
        self.scaleInt.set_reference_unit(referenceUnit)
        self.scaleInt.reset()
        self.scaleInt.tare()

        #Servo setup
        #GPIO.setmode(GPIO.BOARD) # Set GPIO numbering mode
        GPIO.setup(servo_pin,GPIO.OUT) # Set pin 37 as an output, and set servo as pin 37 as PWM
        self.servo = GPIO.PWM(servo_pin,50) # Note 11 is pin, 50 = 50Hz pulse
        print("Setup finished")   

    def cleanAndExit(self):
        print("Cleaning...")
        GPIO.cleanup()    
        print("Bye!")
        sys.exit()

    def setAngle(self, angle):
        duty = angle / 18 + 2
        #GPIO.output(03, True)
        self.servo.ChangeDutyCycle(duty)
        time.sleep(1)
        #GPIO.output(03, False)
        self.servo.ChangeDutyCycle(0)

    def getWeight(self, times=5):
        return self.scaleInt.get_weight(times)

    def dispenseWeight(self, weight):
        print("Starting erogation")
        self.servo.start(0)
        time.sleep(2)
        startVal = self.getWeight()
        currentWeight = startVal
        print("Opening door")
        self.setAngle(0)
        #time.sleep(2)
        self.setAngle(180) #open door

        while currentWeight > startVal - weight: #check food erogation
            currentWeight = self.getWeight(5)
        print("Closing door")
        self.setAngle(0)
        #time.sleep(2)
        self.servo.stop()
        print("Erogation finished")


