auth_token='754315ccc34a6aadae523175a8e8172c'
#754315ccc34a6aadae523175a8e8172c
#12250e6d704116b7fe6822b9e4d80ab9
board_no="board_2"

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
	  #print("result : ", result)
	  if(result=="202"):
		  print("Remote not configured")
		  return
		
	  xx=json.loads(result)
	  #print("xx : ",xx)
	   
	  yy=read_from_file()
	  #print("yy : ",yy)
	  
	  if (yy != xx):
		  #print("not a match")
		  write_to_file(result)
	
	  print(json.dumps(xx,indent=1))
	  
	 
	except Exception as e:
		print(e)
	
	action()

import requests
def camera_picture_upload():
	
	f = open("/etc/os-release")
	text = f.readline()
	f.close()
	x = text.index("Linux")
	y = text.index("(")
	ver=int(text[x+6:y])
	
	if(ver>=11):
		cmd= "libcamera-still -o " +  curr_dir+"/image.jpg" + " --width 1640 --height 1232"
		#cmd= "libcamera-still -o " +  curr_dir+"/image.jpg" + " --width 1640 --height 1232 --vflip --hflip"
		print(cmd)
		
	else:
		cmd= "raspistill -o " +  curr_dir+"/image.jpg"  + " -w 1640 -h 1232"
		#cmd= "raspistill -o " +  curr_dir+"/image.jpg"  + " -w 1640 -h 1232 -vf -hf"
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
	#print("setting pins")
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
		time.sleep(z[1])
	
	
	#fetch_data()
	
if __name__ == '__main__':
    main()
