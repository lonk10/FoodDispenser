#!/usr/bin/env python3

import RPi.GPIO as GPIO
from hx711 import HX711
from flask import Flask, render_template
import datetime
import time
import sys
from backend import Backend

app = Flask(__name__)

@app.route("/")
def index():
	# Read Sensors Status
      scaleSts = bk.getWeight()
      templateData = {
            'title' : 'Cat food dispenser!',
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
      bk = Backend()
      try: 
            app.run(host='0.0.0.0', port=80, debug=True)
      finally:
            bk.cleanAndExit()