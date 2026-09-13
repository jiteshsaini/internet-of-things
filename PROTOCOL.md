# How a board talks to the widgets

Everything here is a plain HTTPS GET, with all the arguments packed into one
parameter called `p`, separated by `*`. There is no session and no login: your
auth_token is the whole identity, which is why it matters that you keep it.

    p=<auth_token>*<field>*<field>...

Your board only ever makes outgoing requests. Nothing connects to your board, so
there is nothing to port forward and no reason for your router to care.

If you want to use these widgets from a board that is not covered in this repo,
this page is what you need.

---

## Remote widget

### Reading the pin state

    GET /iot/remote/read_data.php?p=<token>*<board_no>

`board_no` is `board_1` unless you have more than one board on the account.

The answer depends on who is asking, which is the third field:

| Third field | Who | What comes back |
|---|---|---|
| *(none)* | Raspberry Pi | every pin, plus `n` and `t` |
| `esp` | ESP32 | only the pins that changed since it last asked |
| `web` | the browser | pin state plus camera picture info |

For a Raspberry Pi you get something like:

```json
{"5":"1","10":"0","6":"1","12":"0","99":"0","n":"3","t":"20"}
```

The numbers are BCM pin numbers, and the values are what you should set them to.
Two keys are not pins:

- `99` is the camera button. It reads `1` when somebody pressed the button on the
  web page, and the server sets it back to `0` as soon as you have read it, so you
  get it once.
- `n` and `t` say how to pace yourself: make `n` requests, `t` seconds apart. Today
  the server always answers 3 and 20, and the cron task runs the script every
  minute. Do the sleeping between requests, not after the last one, or your run
  overruns the minute and collides with the next one.

If the widget has not been set up yet, the whole answer is the string `202`. It is
not JSON, so check for it before parsing.

### The ESP32 difference

An ESP32 asks with `*esp` and gets only what changed, to keep packets small. Add a
fourth field to say you have just booted:

    p=<token>*<board_no>*esp*1

`1` means "I just started, send me everything". `0` means "regular check, send me
changes only".

### Uploading a camera picture

    POST /iot/remote/upload.php?p=<token>*<board_no>

Multipart form, with the image in a field called `myfile`.

---

## Water tank widget

### Sending a reading

    GET /iot/sensor_ultrasonic/data.php?p=<token>*<sensor>*<reading>

`sensor` is `ultrasonic_1` through `ultrasonic_4`. `reading` is the distance in cm
from the sensor to the water.

A normal answer:

```json
{"state":"ok","server_msg":"Success: Data (34) uploaded","server_time":"2026-09-13 12:00:00","settings_flag":"0"}
```

Anything rejected comes back the same shape with `"state":"error"` and a
`server_msg` saying why: an unknown token, a sensor name that is not in range, a
widget that has not been configured, or a reading sent too soon after the last one.

### Getting settings back

When you change the tank settings in the browser, the next reading you send is
answered with the settings instead of the usual message:

```json
{"tank_height":"100","tank_diameter":"50","high_level_trigger":"90","low_level_trigger":"10","settings_flag":"1"}
```

Save them. **The server sends them once** and then clears the flag, so if your
client throws the answer away the settings are gone until the user changes
something again.

---

## Things worth knowing

The token travels in the URL. That means it ends up in server logs and in browser
history, so treat a token as something that leaks easily and can be regenerated,
not as a permanent secret.

Use `https://`. The clients in this repo used to pass `-k` to curl, which turns off
certificate checking; that has been removed, and you should not add it back.

One request at a time from one board. The pin state lives in a file on the server
and is rewritten on every read, so two clients sharing a token will confuse each
other.
