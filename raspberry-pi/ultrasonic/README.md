### This code is meant for Raspberry Pi (all models)

The file 'helloworld.py' does the job of communicating with online widget hosted at https://helloworld.co.in/iot/sensor_ultrasonic. 
You need to personalise it by pasting your Authentication Code in it. 

This file is imported in other Python files so that you can send the data to your online widget in just one line of code. 

The same is demonstrated by following files in the folder:-

### 'sample.py'
This is a test file which can be used for testing communication between your Raspberry Pi and the online widget. 
To run this file, you do not require any additional hardware. This file simply generates a random value and sends it to the online widget. 
When the data is received by the widget, the water level fluctuates as per the received data. 

### 'sensor.py'
Once you have successfully establised communication with your online widget, it is time to upload the actual sensor data. 
This file calculates the distance reading from the actual sensor (HC-SR04 ultrasonic distance sensor) and uploads it to the online widget. 
You need to interface the sensor to Raspberry Pi before you run this file.
The file also demonstrates how to make use of the settings (made on online widget) to actuate the GPIO pins. You can modify this file as per your requirement.

### Watch the video on Yotube 
<a href='https://youtu.be/ETrYPMRdL-E '>
   <img src='https://github.com/jiteshsaini/files/blob/main/img/btn_youtube.png' height='40px'>
</a>
