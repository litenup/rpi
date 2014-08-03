import pdb
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
camera.framerate = 24
camera.start_recording('mjpegmovie', format='mjpeg')
camera.wait_recording(10)
camera.stop_recording()