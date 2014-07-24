#!/bin/bash
# Script to start motion detection plus live stream

python picamscript.py | avconv -f h264 -i - -vsync 1 -vcodec mpeg1video -f mpeg1video -b 400k -r 24 -s 320x240 http://10.10.42.16:8082/lighthouse/320/240/
