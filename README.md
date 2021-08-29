# FoodDispenser

Web application for an IoT food dispenser using GPIO functionality.

Main features are automatic erogation and schedule managing. 

Made with Flask, Bootstrap, GPIO and pigpio.

### Installation
Simply clone the repository, use `Backend()` to set the pins for the HX711 module and servomotor (defaults are: `GPIO 5 -> HX711 DT` `GPIO 6 -> HX711 SCK` `GPIO 18 -> Servo`)

HX711 calibration is done with the `referenceUnit` parameter, the value needs to be manually adjusted module by module. Refer to HX711py documentation for questions.

Make sure pigpio's deamon is active (use `sudo pigpiod` to start it)

### Usage
`sudo python app.py`

Web service is on `localhost:80`

Erogation scheduling is done on `localhost:80/menu`, simply choose the time and quantity.

## TODO

Popup alerts

## Credits
HX711 library - https://github.com/tatobari/hx711py
