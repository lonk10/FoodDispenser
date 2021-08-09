# FoodDispenser

Web application for an IoT food dispenser using GPIO functionality.

Made with Flask, Bootstrap, GPIO and pigpio

### Installation
Simply clone the repository, use `Backend()` to set the pins for the HX711 module and servomotor (defaults are: `GPIO 5 -> HX711 DT` `GPIO 6 -> HX711 SCK` `GPIO 18 -> Servo`)

Make sure pigpio's deamon is active (use `sudo pigpiod` to start it)

### Usage
`sudo python app.py`

Web service is on `localhost:80`
## Credits
HX711 library - https://github.com/tatobari/hx711py
