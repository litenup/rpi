import json
import urllib2

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

# data = json.load(urllib2.urlopen('https://api.github.com/search/users?q=alanhsu@litenvoice.com+in:email'))
# print data

ret = subprocess.call("/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/foolong2.mpg foolong2.mpg", shell=True)
print ret
ret = subprocess.call("/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/whatever foolong2.mpg", shell=True)
print ret