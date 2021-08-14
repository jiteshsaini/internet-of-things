
import helloworld as hw
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG = 6
ECHO = 5
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)

PIN_1 = 14
PIN_2 = 23
GPIO.setup(PIN_1,GPIO.OUT)
GPIO.setup(PIN_2,GPIO.OUT)

def measure_distance():
	dist_add = 0
	loop=10
	for x in range(loop):
		try:
			GPIO.output(TRIG, True)
			time.sleep(0.00001)
			GPIO.output(TRIG, False)

			while GPIO.input(ECHO)==0:
				pulse_start = time.time()

			while GPIO.input(ECHO)==1:
				pulse_end = time.time()

			pulse_duration = pulse_end - pulse_start
			distance = pulse_duration * 17150
			distance = round(distance, 3)
			print (x, "distance: ", distance)	
			dist_add = dist_add + distance
			
			time.sleep(.1) # 100ms interval between readings
		
		except Exception as e: 
			pass

	avg_dist=dist_add/(loop)
	dist=round(avg_dist,3)
	print ("Avg distance: ", dist)
	
	return dist
	
def action(reading):
	settings = hw.read_settings()
	
	if(settings==0):
		print("file not present")
		return 
	
	low_level_trigger=float(settings["low_level_trigger"])
	high_level_trigger=float(settings["high_level_trigger"])
	tank_height=float(settings["tank_height"])
	
	water_level=tank_height-reading

	if (water_level>=high_level_trigger):
		GPIO.output(PIN_1, True)
		GPIO.output(PIN_2, False)
	
	if (water_level<=low_level_trigger):
		GPIO.output(PIN_2, True)
		GPIO.output(PIN_1, False)
	
	if (water_level>low_level_trigger and water_level<high_level_trigger):
		GPIO.output(PIN_1, False)
		GPIO.output(PIN_2, False)
	
	
def main():
	print ("Waiting For Sensor To Settle")
	time.sleep(0.3) #settling time 
	
	reading = measure_distance()
	
	hw.upload_data(reading)
	
	action(reading)
	
if __name__ == '__main__':
    main()
