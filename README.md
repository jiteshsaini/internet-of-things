# Internet of Things

Start here: <a href='https://helloworld.co.in/iot' target='_blank'>
   <img src='https://raw.githubusercontent.com/jiteshsaini/files/main/img/logo3.gif' height='40px'>
</a>

This repo holds the device side of the online widgets at https://helloworld.co.in/iot

The widget runs in your browser, the code here runs on your board, and the two talk
through my server. So you can watch a sensor or flip a GPIO pin from anywhere,
without port forwarding, a static IP, or writing any server code yourself.

### The widgets

| Board | Widget | Folder | What it does |
|---|---|---|---|
| Raspberry Pi | Remote | [raspberry-pi/remote](raspberry-pi/remote) | Switch GPIO pins and take pictures from the browser |
| Raspberry Pi | Water tank | [raspberry-pi/ultrasonic](raspberry-pi/ultrasonic) | Send distance readings from an HC-SR04 to a tank gauge |
| ESP32 | Remote | [esp32/esp_remote](esp32/esp_remote) | Switch ESP32 GPIO pins from the browser |

### Your auth_token

Create an account at <a href='https://helloworld.co.in/iot'>helloworld.co.in/iot</a>.
You get an auth_token, a 32 character string that tells the widgets which board is
which. It is shown on that page when you are signed in, and emailed to you the first
time you log in.

<img src='https://raw.githubusercontent.com/jiteshsaini/files/main/img/token.png'>

Paste it into the first line of the device code, in place of `xxxxxx`. Keep it to
yourself: anyone who has your token can drive your pins and read your sensors.

### GPIO library on a Raspberry Pi

The Python code does `import RPi.GPIO`. On a Pi 5 the original RPi.GPIO will not work
at all, because the GPIO hardware changed and that library still talks to the old
registers. Install rpi-lgpio instead. It provides the same `RPi.GPIO` name, so nothing
in the code changes:

```
sudo apt install python3-rpi-lgpio
```

Both packages cannot be installed together, so remove the old one if you have it:

```
sudo apt remove python3-rpi.gpio
```

If you are coming back to a Pi after a while: `raspi-gpio` is no longer part of
Raspberry Pi OS, `pinctrl` replaced it. To see what a pin is actually doing:

```
pinctrl get 24
```

### How a board talks to the widgets

See [PROTOCOL.md](PROTOCOL.md) if you want to write your own client for a board
that is not covered here.
