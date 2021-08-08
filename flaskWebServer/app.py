#!/usr/bin/env python3

import RPi.GPIO as GPIO
from hx711 import HX711
from flask import Flask, render_template
import datetime
import time
import sys
from backend import Backend



print("Setup started")
#HX711 setup

app = Flask(__name__)
"""
scaleInt = HX711(5,6)
referenceUnit = 390
scaleInt.set_reading_format("MSB", "MSB")
scaleInt.set_reference_unit(referenceUnit)
scaleInt.reset()
scaleInt.tare()
"""

#Servo setup
#GPIO.setmode(GPIO.BOARD) # Set GPIO numbering mode
#GPIO.setup(18,GPIO.OUT) # Set pin 37 as an output, and set servo as pin 37 as PWM
#servo = GPIO.PWM(18,50) # Note 11 is pin, 50 = 50Hz pulse
print("Setup finished")

@app.route("/")
def index():
	# Read Sensors Status
      scaleSts = bk.getWeight()
      templateData = {
            'title' : 'GPIO input Status!',
            'scale'  : scaleSts,
      }
      return render_template('index.html', **templateData)

@app.route("/disp")
def dispenseWeight(weight=20):
      bk.dispenseWeight(weight)
      scaleSts = bk.getWeight()
      templateData = {
            'title' : 'GPIO input Status!',
            'scale'  : scaleSts,
      }
      return render_template('index.html', **templateData)

if __name__ == "__main__":
      try: 
            bk = Backend()
            app.run(host='0.0.0.0', port=80, debug=True)
      finally:
            bk.cleanAndExit()