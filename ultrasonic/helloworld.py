import os, json

auth_token='754315ccc34a6aadae523175a8e8172c'
#auth_token='12250e6d704116b7fe6822b9e4d80ab9'
sensorType_no="ultrasonic_3"
#sensorType_no="temperature_2"

#curr_dir=os.path.abspath(os.getcwd())
curr_dir="/home/pi/Desktop/iot"

def download_settings():
	parameters="p=get*"+auth_token+"*"+sensorType_no
	url_remote="https://helloworld.co.in/iot/data.php?"+parameters
	cmd="curl -s " + url_remote
	#print (cmd)
	result=os.popen(cmd).read()
	f = open(curr_dir+"/settings.json", "wb")
	#f = open("/home/pi/Desktop/iot/settings.json", "wb")
	f.write(result)
	f.close()
    
	yy=json.loads(result)
	print ("High Level Trigger")
	print (yy["high_level_trigger"])
	print ("Low Level Trigger")
	print (yy["low_level_trigger"])
	

def upload_data(reading):
	parameters="p=set*"+auth_token+"*"+sensorType_no+"*"+str(reading)
	url_remote="https://helloworld.co.in/iot/data.php?"+parameters
	cmd="curl -s " + url_remote
	#print (cmd)
	result=os.popen(cmd).read()
	xx=json.loads(result)
	
	print (xx["server_msg"])
	
	if(xx["state"]=="error"):
		f = open("/home/pi/Desktop/iot/log.txt", "a")
		f.write(xx["server_time"] + ":" + xx["server_msg"] +"\n")
		f.close()
		
	if(xx["settings_flag"]=="1"):
		download_settings()
		
def read_settings():
	f = open(curr_dir+"/settings.json")
	settings = json.load(f)
	f.close()
	return settings
