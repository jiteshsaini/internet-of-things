import random
import helloworld as hw

def measure_distance():
	d=random.randrange(10, 95)
	return d

def action():
	settings = hw.read_settings()
	print (settings["tank_diameter"])
	
def main():
	
	reading = measure_distance()
	
	hw.upload_data(reading)
	
	action()
	
if __name__ == '__main__':
    main()
