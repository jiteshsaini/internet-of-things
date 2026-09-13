#!/bin/bash

FILE_NAME="sensor.py"

crontab -u $USER -l| grep $PWD/$FILE_NAME > /dev/null
if [ $? -eq 0 ]
then
	echo "$FILE_NAME is already running"
else
	crontab -l 2>/dev/null > mycron
	echo "* * * * * python3 $PWD/$FILE_NAME > /dev/null 2>&1 &" >> mycron
	crontab mycron
	rm mycron
	echo "cron task added. Now $PWD/$FILE_NAME file will run every minute"
fi

