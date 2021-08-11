# Internet of Things

<p align="left">
Start here: <a href='https://helloworld.co.in/iot' target='_blank'>
   <img src='https://github.com/jiteshsaini/files/blob/main/img/logo3.gif' height='40px'>
</a> Watch the video on Yotube: 
<a href=''>
   <img src='https://github.com/jiteshsaini/files/blob/main/img/btn_youtube.png' height='40px'>
</a>
</p>

This repo will be populated with projects for connecting your your IOT boards such as Raspberry Pi, ESP 32 and Arduino to the Web Application running at https://helloworld.co.in/iot and make use of the online widgets there to to visualise your sensor data online.

<img src='https://github.com/jiteshsaini/files/blob/main/img/iot_working.png'>

You need to create an account <a href='https://helloworld.co.in/iot/'>here</a> to access your online widgets. Once logged in, you will see simple instructions to setup your device and start uploading your sensor data to your online widgets.

When you create an account, you will receive an Authentication Token on your email. The token is 32 byte long alphanumeric string as shown in the example below.

<img src='https://github.com/jiteshsaini/files/blob/main/img/token.png'>

It is required to be pasted once in the code provided here to get the things going.

## Raspberry Pi
Presently, sample code for Raspberry pi has been added to this repo to communicate with "Water Tank" online widget. 

The code folder contains an API 'helloworld.py' that does the job of communicating with the remote server hosted at www.helloworld.co.in/iot. You need to personalise it by pasting your Authentication Code in it. You need not change / modify any other part in this file.

This file is imported in other Python files so that you can send the data to your online widget in just one line of code. 

The same is demonstrated by following files in the folder:-

### 'sample.py'
This is a test file which can be used for testing communication between your Raspberry Pi and the online widget. To run this file, you do not require any additional hardware. This file simply generates a random value and sends it to the online widget. When the data is received by the widget, the water level fluctuates as per the received data. 

### 'sensor.py'
Once you have successfully establised communication with your online widget, it is time to upload the actual sensor data. This file calculates the distance reading from the actual sensor (HC-SR04 ultrasonic distance sensor) and uploads it to the online widget. You need to interface the sensor to Raspberry Pi before you run this file.
The file also demonstrates how to make use of the settings (made on online widget) to actuate the GPIO pins. You can modify this file as per your requirement.

## Other IOT boards
Sample codes for other IOT boards such as ESP 32, Arduino Nano etc will be added in the future.




