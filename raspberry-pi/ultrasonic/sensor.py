import random
import helloworld as hw

def measure_distance():
	d=random.randrange(10, 95)
	return d

def action(reading):
	settings = hw.read_settings()
	print (reading)
	print (settings["high_level_trigger"])
	
	if (reading>int(settings["high_level_trigger"])):
		str1=str(reading) + " is above high_level_trigger - " + settings["high_level_trigger"] + "\n"
		print(str1)
		f = open(hw.curr_dir+"/util/alarm.txt", "a")
		f.write(str1)
		f.close()
	else:
		str1=str(reading) + " is below high_level_trigger - " + settings["high_level_trigger"] + "\n"
		print(str1)
	
def main():
	
	reading = measure_distance()
	
	hw.upload_data(reading)
	
	action(reading)
	
if __name__ == '__main__':
    main()
