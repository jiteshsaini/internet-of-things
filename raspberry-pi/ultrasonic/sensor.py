
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

# Two output pins, for a pump or a valve. 24 and 23 sit next to each other
# on the header (physical 16 and 18), so a two-relay board wires up neatly.
# This used to be GPIO 14, which is the serial console's TX pin: a relay
# there clicks through every boot, and claiming it kills the console.
PIN_1 = 24
PIN_2 = 23
GPIO.setup(PIN_1,GPIO.OUT)
GPIO.setup(PIN_2,GPIO.OUT)

def measure_distance():
	readings = []
	loop = 10
	for x in range(loop):
		try:
			GPIO.output(TRIG, True)
			time.sleep(0.00001)
			GPIO.output(TRIG, False)

			# An HC-SR04 echo lasts about 24 ms at its 4 m ceiling, so 50 ms is a
			# generous deadline. Without one these loops spin forever whenever no
			# echo arrives at all - sensor unplugged, loose wire, floating pin - and
			# an infinite loop raises nothing, so the except below cannot rescue it.
			# Under a per-minute cron that leaves one hung python3 behind a minute,
			# until the Pi runs out of memory.
			# Seeded before the loop: if the echo is already high on the first
			# poll the body never runs, and the original code then raised
			# NameError on pulse_start - silently swallowed by the except.
			pulse_start = time.time()
			deadline = pulse_start + 0.05
			while GPIO.input(ECHO) == 0:
				pulse_start = time.time()
				if pulse_start > deadline:
					raise TimeoutError("echo never started")

			pulse_end = time.time()
			deadline = pulse_end + 0.05
			while GPIO.input(ECHO) == 1:
				pulse_end = time.time()
				if pulse_end > deadline:
					raise TimeoutError("echo never ended")

			distance = round((pulse_end - pulse_start) * 17150, 3)
			print(x, "distance: ", distance)
			readings.append(distance)

			time.sleep(.1) # 100ms interval between readings

		except Exception as e:
			print(x, "skipped:", e)

	if not readings:
		# Nothing measured. Returning 0 here would read as "tank completely
		# full", so the caller is told there is no reading instead.
		print("no usable reading from the sensor")
		return None

	# Median rather than mean: one spurious echo - a ripple, a wall, a missed
	# pulse - drags an average but barely moves a median. The old code also
	# divided by all 10 attempts even when some failed, which pulled the
	# result toward zero every time a reading was skipped.
	readings.sort()
	mid = len(readings) // 2
	if len(readings) % 2:
		dist = readings[mid]
	else:
		dist = round((readings[mid - 1] + readings[mid]) / 2, 3)
	print("Median distance: ", dist, "from", len(readings), "of", loop, "readings")

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
	if reading is None:
		# Do not invent a number. upload_data would publish it and action()
		# would switch a pump on the strength of it.
		return
	
	hw.upload_data(reading)
	
	action(reading)
	
if __name__ == '__main__':
    main()
