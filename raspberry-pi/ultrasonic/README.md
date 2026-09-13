### This code is meant for Raspberry Pi (all models)

It works with the water tank widget at https://helloworld.co.in/iot/sensor_ultrasonic

Create an account <a href='https://helloworld.co.in/iot'>here</a> to get your widget
and your auth_token. See the [main README](../../README.md) for the token and for the
GPIO library you need on a Pi 5.

`helloworld.py` does the talking to the widget. You personalise it once by pasting
your auth_token into the first line, in place of `xxxxxx`. The other files import it,
so sending a reading is one line of code.

### 'sample.py' — start here, no hardware needed

A test file for checking that your Raspberry Pi can reach your widget. It makes up a
random value and sends it. When the widget receives it, the water level on screen
moves. If this works, your token and your network are fine and anything after this is
wiring.

```
python3 sample.py
```

### 'sensor.py' — the real thing

This reads an HC-SR04 ultrasonic distance sensor and uploads the distance. It also
shows how to act on the settings you made in the widget, by switching two GPIO pins
for a pump or a valve. Modify it to suit what you are building.

Wiring, as the file ships:

| Signal | GPIO (BCM) | Physical pin |
|---|---|---|
| TRIG | 6 | 31 |
| ECHO | 5 | 29 |
| PIN_1 (output) | 24 | 18 |
| PIN_2 (output) | 23 | 16 |

The HC-SR04 echo pin puts out 5 V and the Pi expects 3.3 V, so use a divider or a
level shifter on ECHO.

To have it run by itself every minute:

```
bash setup_cron.sh
```

### A note on the sensor

An HC-SR04 is fine on the bench and for the video below. In a real water tank it has
a hard life: condensation sits on the transducers and the readings wander. If you are
leaving one in a tank, a waterproof JSN-SR04T or AJ-SR04M is the same TRIG/ECHO
interface and survives much better.

### Watch the video on Yotube
<a href='https://youtu.be/ETrYPMRdL-E'>
   <img src='https://raw.githubusercontent.com/jiteshsaini/files/main/img/btn_youtube.png' height='40px'>
</a>
