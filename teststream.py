import smtplib
import email
import mimetypes
import StringIO
import subprocess
import os
import time
import sys
import time
import picamera
from datetime import datetime
from PIL import Image
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
camera = picamera.PiCamera()
camera.resolution = (320, 240)
camera.framerate = 30
camera.start_recording('foolong.h264', format='h264')
camera.wait_recording(30)
camera.stop_recording()
# camera.start_preview()
# camera.start_recording(sys.stdout, format='yuv')
# os.system('clear')
# camera.resolution = (1024, 768)
# camera.start_preview()
# camera.capture_continous(sys.stdout, format='jpeg')

avconv -f h264 -i foolong.h264 -target ntsc-vcd -vcodec mpeg1video -s 320x240 foolong2.mpg
ffmpeg -i foolong.h264 -target pal-dvd -ps 2000000000 -aspect 16:9 foolong2.mpeg
ffmpeg -i film_sortie_cinelerra.ogm -s 720x576 -vcodec mpeg2video -acodec mp3 film_terminÃ©e.mpg

python picamscript.py | avconv -f h264 -i - -vsync 1 -vcodec mpeg1video -f mpeg1video -b 400k -r 24 -s 320x240 http://10.10.41.243:8082/lighthouse/320/240/