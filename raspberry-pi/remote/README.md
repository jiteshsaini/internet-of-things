### This code is meant for Raspberry Pi (all models)

It works with the online remote at https://helloworld.co.in/iot/remote/

Create an account <a href='https://helloworld.co.in/iot'>here</a> to get your remote
and your auth_token. See the [main README](../../README.md) for the token and for the
GPIO library you need on a Pi 5.

### Procedure to use

1. Download this code on your Raspberry Pi.

2. Open `helloworld.py` and paste your auth_token into the first line, in place of
   `xxxxxx`. Save and close. Do not modify any other part of the code.

3. Run `bash setup_cron.sh`. It adds a cron task that runs `helloworld.py` every
   minute, so the board keeps checking in on its own after a reboot.

### Choosing pins in the widget

You pick which GPIOs to control from the browser. A few are best left alone unless
you know you want them: 14 and 15 carry the serial console, 2 and 3 are I2C, and
7 to 11 are SPI. Anything else on the header is fair game.

### The camera

The picture button uses the Pi's own camera tool, whichever one your OS has
(`rpicam-still`, `libcamera-still` or `raspistill`). It needs a camera on the CSI
ribbon connector. A USB webcam will not work with it.

  ### Article
Read the complete article <a href='https://helloworld.co.in/article/online-remote-controlling-raspberry-pi-gpio-and-camera-remotely-iot-project'>here</a>.

### Video

Watch the video https://youtu.be/b1IJfsaedSk
