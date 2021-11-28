#!/bin/bash

FILE_NAME="helloworld.py"

crontab -u $USER -l| grep $PWD/$FILE_NAME > /dev/null
if [ $? -eq 0 ]
then
	echo "$FILE_NAME is already running"
else
	crontab -l > mycron
	echo "* * * * * sudo python $PWD/$FILE_NAME &" >> mycron
	crontab mycron
	rm mycron
	sudo chmod 777 -R $PWD
	echo "cron task added. Now $PWD/$FILE_NAME file will run every minute"
fi

