import os, json

auth_token='754315ccc34a6aadae523175a8e8172c'
#auth_token='12250e6d704116b7fe6822b9e4d80ab9'
sensorType_no="ultrasonic_3"
#sensorType_no="temperature_2"


os.chdir(os.path.dirname(os.path.abspath(__file__)))
curr_dir=os.path.abspath(os.getcwd())

def download_settings():
	parameters="p=get*"+auth_token+"*"+sensorType_no
	url_remote="https://helloworld.co.in/iot/data.php?"+parameters
	cmd="curl -s " + url_remote
	#print (cmd)
	result=os.popen(cmd).read()
	
	f = open(curr_dir+"/util/settings.json", "wb")
	f.write(result)
	f.close()
    
	yy=json.loads(result)
	print(json.dumps(yy,indent=1))
	

def upload_data(reading):
	parameters="p=set*"+auth_token+"*"+sensorType_no+"*"+str(reading)
	url_remote="https://helloworld.co.in/iot/data.php?"+parameters
	cmd="curl -s " + url_remote
	#print (cmd)
	result=os.popen(cmd).read()
	xx=json.loads(result)
	
	print (xx["server_msg"])
	
	if(xx["state"]=="error"):
		f = open(curr_dir+"/util/log.txt", "a")
		f.write(xx["server_time"] + ":" + xx["server_msg"] +"\n")
		f.close()
		
		
	if(xx["settings_flag"]=="1"):
		download_settings()
		
def read_settings():
	f = open(curr_dir+"/util/settings.json")
	settings = json.load(f)
	f.close()
	return settings
