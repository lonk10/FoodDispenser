#!/usr/bin/env python3

import RPi.GPIO as GPIO
from hx711 import HX711
from flask import Flask, render_template, jsonify, request
import datetime
import time
import sys
import multiprocessing
from backend import Backend
from scheduler import Config

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

@app.route("/menu/req", methods=['POST'])
#updates scheduler json with post request data
def updateScheduler():   
      hour = request.form.get('hour')
      mins = request.form.get('mins')
      weight = request.form.get('weight')
      orario = str(hour) + ":" + str(mins)
      wgt = int(weight)
      jdata.set_entry(orario, wgt)
      glob.d = jdata 
      templateData = {
            'sched' : tableData()
      }
      return render_template('menu.html', **templateData)

def tableData():
      orari = jdata.get_key("orari")
      wgt = jdata.get_key("grammi")
      zipped = zip(orari, wgt)
      ziplist = list(zipped)
      return sorted(ziplist, key=lambda tup: (tup[0]))

#handles automatic erogation
def scheduleLoop():
      while True:
            now = datetime.datetime.now()
            mins = str(now.minute)
            h = str(now.hour) + ":" + mins
            if h in glob.d.get_key("orari"):
                  index = glob.d.get_key("orari").index(h)
                  bk.dispenseWeight(glob.d.get_key("grammi")[index])
            time.sleep(60)

@app.route("/menu")
def menu():
      templateData = {
            'sched' : tableData()
      }
      return render_template('menu.html', **templateData)

@app.route("/update")
def update():
    val = bk.getWeight()
    templateData = {'data' : val}
    return jsonify(templateData), 200

if __name__ == "__main__":
      manager = multiprocessing.Manager()
      jdata = Config("scheduler.json")
      glob = manager.Namespace()
      glob.d = jdata
      bk = Backend()
      proc = multiprocessing.Process(target=scheduleLoop)
      proc.start()
      try: 
            app.run(host='0.0.0.0', port=80, debug=True)
      finally:
            proc.terminate()
            bk.cleanAndExit()
            sys.exit()