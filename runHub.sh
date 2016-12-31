#!/bin/bash

cd /home/pi/hub/piHub

COMMAND="python piHubTemp.py >> /media/disk1/logs/piHubPython.log 2>&1 "
$COMMAND &


