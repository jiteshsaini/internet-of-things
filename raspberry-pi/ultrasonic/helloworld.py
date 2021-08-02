auth_token='ed5d1166c007dd2f068cd31636de6912'

sensorType_no="ultrasonic_1"

#======DO NOT MODIFY THE CODE BELOW =======================#
import os, json

os.chdir(os.path.dirname(os.path.abspath(__file__)))
curr_dir=os.path.abspath(os.getcwd())

def upload_data(reading):
	parameters="p="+auth_token+"*"+sensorType_no+"*"+str(reading)
	url_remote="https://helloworld.co.in/iot/data.php?"+parameters
	cmd="curl -s " + url_remote
	#print (cmd)
	try:
	  result=os.popen(cmd).read()
	  xx=json.loads(result)
	  if(xx["settings_flag"]=="1"):
		  f = open(curr_dir+"/util/settings.json", "wb")
		  f.write(result)
		  f.close()
		  print(json.dumps(xx,indent=1))
	  else:
		 print (xx["server_msg"])
		 if(xx["state"]=="error"):
			 f = open(curr_dir+"/util/error_log.txt", "a")
			 f.write(xx["server_time"] + ":" + xx["server_msg"] +"\n")
			 f.close()
	except:
		print("..")
		pass
		

def read_settings():
	f = open(curr_dir+"/util/settings.json")
	settings = json.load(f)
	f.close()
	return settings
