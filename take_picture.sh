#!/bin/bash
# Script to take a picture 

NOW=$(date +"%Y%m%d%H%M%S")

echo "Picture: " $NOW

#Take picture
raspistill -o $NOW.jpg

/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/Dropbox-Uploader/$NOW.jpg $NOW.jpg 
