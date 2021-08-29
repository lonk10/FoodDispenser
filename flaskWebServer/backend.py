import RPi.GPIO as GPIO
from hx711 import HX711
import time
import sys
import pigpio


class Backend:

    ### Initializes backend object
    # dout = HX711 dt pin, pd_sck = HX711 sck pin, servo_pin = servo motor GPIO pin 
    def __init__(self, dout=5, pd_sck=6, servo_pin=18, referenceUnit=390):
        print("Setup started")
        #HX711 setup
        self.scaleInt = HX711(dout, pd_sck)
        #referenceUnit = 390 # reference unit for HX711, manually adjusted
        self.scaleInt.set_reading_format("MSB", "MSB")
        self.scaleInt.set_reference_unit(referenceUnit)
        self.scaleInt.reset()
        self.scaleInt.tare()
 
        #Servo setup, uses pigpio library as GPIO.PWM resulted in unwanted behaviour
        self.servo = pigpio.pi()
        self.servo.set_mode(servo_pin, pigpio.OUTPUT)
        self.servo.set_PWM_frequency(servo_pin, 50)
        self.servo_pin = servo_pin
        print("Setup finished")   


    ### Safe cleanup
    def cleanAndExit(self):
        print("Cleaning...")
        self.servo.stop()
        GPIO.cleanup()    
        print("Bye!")
        sys.exit()

    ### Sets angle for servomotor
    def setAngle(self, angle):
        duty = (angle / 0.09) + 500 # set_servo_pulsewidth uses values ranging 500-2500
        self.servo.set_servo_pulsewidth(self.servo_pin, duty)
        time.sleep(1 + angle/180) # gives enough time for servo to turn

    ### Sets angle to default position
    def resetAngle(self):
        self.setAngle(0) 
    
    ### Turns off servomotor
    def turnOffServo(self):
        self.servo.set_servo_pulsewidth(self.servo_pin, 0)

    ### Reads weight from the scale
    def getWeight(self, times=5):
        return self.scaleInt.get_weight(times)

    ### Erogates {weight} grams from the dispenser
    def dispenseWeight(self, weight):
        print("Starting erogation")
        startVal = self.getWeight()
        currentWeight = startVal #get starting weight
        print("Opening door")
        self.setAngle(180) #opens door
        while currentWeight > startVal - weight: #check food erogation
            currentWeight = self.getWeight(5)
        print("Closing door")
        self.resetAngle() #closes door
        self.turnOffServo()
        print("Erogation finished")


