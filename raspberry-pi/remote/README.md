### This code is meant for Raspberry Pi (all models)

It works in conjunction with an online remote control created at https://helloworld.co.in/iot/remote/

You can access your online remote by creating an account <a href='https://helloworld.co.in/users/login.php'>here</a>. When you create an account, an Athentication Token (auth_token) is sent to you via email.

### Procedure to use
  
1. Download this code on your Raspberry Pi.
  
2. Open the file 'helloworld.co.in' and paste your Athentication Token (auth_token) in the first line. Save the file and close. Do not modify any other part of code. 
  
3. Run the bash script 'setup_cron.sh' using command 'sh setup_cron.sh'. The script will create a cron task to run the 'helloworld.py' file automatically every minute.

  ### Article
Read the complete article <a href='https://helloworld.co.in/article/online-remote-controlling-raspberry-pi-gpio-and-camera-remotely-iot-project'>here</a>.

### Video

Watch the video https://youtu.be/b1IJfsaedSk
