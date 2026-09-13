auth_token="xxxxxx"
board_no="board_1"

#======DO NOT MODIFY THE CODE BELOW =======================#
import os, json, time
from threading import Thread
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

logic = 1

os.chdir(os.path.dirname(os.path.abspath(__file__)))
curr_dir=os.path.abspath(os.getcwd())

site = "https://helloworld.co.in/iot/remote"
parameters="p="+auth_token+"*"+board_no

def fetch_data():
	url =site+"/read_data.php?"+parameters
	cmd="curl -s " + url
	print (cmd)
	try:
	  result=os.popen(cmd).read()
	  if(result=="202"):
		  print("Remote not configured")
		  return
		
	  xx=json.loads(result)
	  yy=read_from_file()
	  
	  if (yy != xx):
		  write_to_file(result)
	
	  print(json.dumps(xx,indent=1))
		
	except Exception as e:
		print(e)
	
	action()

import requests
def camera_picture_upload():
	
	#Raspberry Pi OS Bookworm and later ship rpicam-still, and it needs a camera on
	#the CSI ribbon connector - a USB webcam will not work with it. On an older card
	#the tool is called libcamera-still (Bullseye) or raspistill (Buster); change the
	#line below if you are on one of those.
	cmd = "rpicam-still -o " + curr_dir+"/image.jpg" + " --width 1640 --height 1232"
	#cmd = cmd + " --vflip --hflip" #uncomment if your camera is mounted upside down
	
	print(cmd)
	
	try:
		p=os.system(cmd)
		if(p==0):
			print("uploading camera picture")
			url = site+"/upload.php?"+parameters
			file = {'myfile': open('image.jpg','rb')}
			r = requests.post(url, files=file, headers={"User-Agent": "HW"})
			print (r.status_code)
			
	except Exception as e:
		print(e)
		
def action():
	yy=read_from_file()
	
	for (k, v) in yy.items():
		
		if (k=='99'):
			if(v=='1'):
				thread1 = Thread(target = camera_picture_upload)
				thread1.start()
			continue
			
		if (k=='t' or k=='n'):
			continue
			
		#print(k + " => " + v)
		GPIO.setup(int(k),GPIO.OUT)
		
		if(int(v) == logic):
			print("setting " + k + " High")
			GPIO.output(int(k), True)
			
		else:
			GPIO.output(int(k), False)
			print("setting " + k + " Low")
		#print("Value: " + str(v))
	
def write_to_file(data):
	f = open(curr_dir+"/settings.json", "wb")
	f.write(data.encode())
	f.close()

def read_from_file():
	path=curr_dir+"/settings.json"
	if(os.path.isfile(path)):
		f = open(path)
		data = json.load(f)
		f.close()
		return data
	else:
		return 0

def loop_params():
	yy=read_from_file()
	if (yy == 0):
		t=20
		n=3
	else:
		t=int(yy['t'])
		n=int(yy['n'])
		
	z=[n,t]
	return z
	
def main():

	z=loop_params()
	for x in range(z[0]):
		#print(str(z[0]) + "," + str(z[1]))
		fetch_data()
		# No sleep after the final fetch. cron restarts this script every 60s,
		# and sleeping n times (rather than n-1) made each run last n*t seconds
		# - exactly 60 with the defaults - so every run was still holding the
		# GPIO pins when the next one started. On modern Pi OS the pins are
		# exclusive (rpi-lgpio), so the incoming run died with "GPIO not
		# allocated" after a single fetch. Measured on the server: every other
		# minute saw 1 poll instead of 3.
		if x < z[0] - 1:
			time.sleep(z[1])
	
	
	#fetch_data()
	
if __name__ == '__main__':
    main()
