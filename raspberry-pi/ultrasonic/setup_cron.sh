#!/bin/bash

FILE_NAME="sensor.py"

crontab -l > mycron
echo "* * * * * sudo python $PWD/$FILE_NAME &" >> mycron
crontab mycron
rm mycron

echo "cron task added. Now $PWD/$FILE_NAME file will run every minute"
