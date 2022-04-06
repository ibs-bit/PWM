from importlib import import_module
import os
import RPi.GPIO as GPIO
from flask import Flask, render_template, request, Response


app = Flask(__name__)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


ledYlw = 12

   
GPIO.setup(ledYlw, GPIO.OUT) 



duty = 0
# set up PWM
pwm_led_yellow = GPIO.PWM( ledYlw,100) 

	
@app.route("/")
def index():
	# Read GPIO Status
	duty = float(40)
	try:
		duty = float(request.values.get('brightness'))
	except:
		pass
	
	pwm_led_yellow.start(duty)
	ledstatus = duty

	
	templateData = {

      'led' : ledstatus

      }
	  
	return render_template('index.html', **templateData)


@app.route("/<deviceName>/<action>")
def action(deviceName, action):
	

	duty = 0
	
	
	if deviceName == 'light':
		actuator = pwm_led_yellow
    
	if action == "low":
		duty = float(5)
		actuator.start(duty) 
	if action == "med":
		duty = float(50)
		actuator.start(duty) 
	if action == "high" or action == 'on':
		duty = float(100)
		actuator.start(duty)
	if action == "off":
		duty = 0
		actuator.stop()
		     
	
	ledstatus = duty

    
	templateData = {
	 
      'ledYlw'  : ledstatus,
   
	}
	return render_template('index.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', threaded=True, port=8080, debug=True)