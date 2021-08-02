import random
import helloworld as hw

def measure_distance():
	d=random.randrange(5, 70)
	return d

	
def main():
	
	reading = measure_distance()
	
	hw.upload_data(reading)
	
	
if __name__ == '__main__':
    main()
