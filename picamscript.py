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
from email.MIMEMultipart import MIMEMultipart
from email.Utils import COMMASPACE
from email.MIMEBase import MIMEBase
from email.parser import Parser
from email.MIMEImage import MIMEImage
from email.MIMEText import MIMEText
from email.MIMEAudio import MIMEAudio
# Original code written by brainflakes and modified to exit
# image scanning for loop as soon as the sensitivity value is exceeded.
# this can speed taking of larger photo if motion detected early in scan

# Motion detection settings:
# PGM maded changes to read values dynamically via command line parameters.
# --------------------------
# Threshold      - (how much a pixel has to change by to be marked as "changed")
# Sensitivity    - (how many changed pixels before capturing an image) needs to be higher if noisy view
# ForceCapture   - (whether to force an image to be captured every forceCaptureTime seconds)
# filepath       - location of folder to save photos
# filenamePrefix - string that prefixes the file name for easier identification of files.
threshold = 10
sensitivity = 180
forceCapture = True
forceCaptureTime = 60 * 60 # Once an hour
filepath = "/home/pi/video/"
filenamePrefix = "cic"
fileTypeImage = "jpg"
fileTypeH264 = "h264"
fileTypeVideo = "mp4"
# File photo size settings
saveWidth = 800
saveHeight = 600
# Picture taking setting after motion detection
delayBtCapture = 1 # seconds
captureDuration = 10 #seconds
DurationSetting = (10 / delayBtCapture) - 1
diskSpaceToReserve = 500 * 1024 * 1024 # Keep 500 mb free on disk
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
camera = picamera.PiCamera()
# Email variables
user = 'alanhsu3338@gmail.com'
smtp_host = 'smtp.gmail.com'
smtp_port = 587
# server = smtplib.SMTP()
# server.connect(smtp_host,smtp_port)
# server.ehlo()
# server.starttls()
# server.login(user,'')
fromaddr = 'alanhsu3338@gmail.com'
tolist = 'alanhsu3338@gmail.com'
sub = 'Subject: birdbox activity'
# Capture a small test image (for motion detection)
def captureTestImage():
    imageData = StringIO.StringIO()
    # try:
    camera.capture(imageData, format='bmp', use_video_port=True)
    # command = "raspistill -w %s -h %s -t 1 -n -e bmp -o -" % (100, 75)
    # except:
    #    camera.capture(imageData, format='bmp', use_video_port=True)
    imageData.seek(0)
    im = Image.open(imageData)
    buffer = im.load()
    imageData.close()
    return im, buffer
    # Save a full size image to disk
def saveVideo(width, height, diskSpaceToReserve):
    print "starting video capture"
    keepDiskSpaceFree(diskSpaceToReserve)
    time = datetime.now()
    camera.resolution = (1280, 720)
    camera.framerate = 30
    filename = filenamePrefix + "%04d%02d%02d-%02d%02d%02d" % (time.year, time.month, time.day, time.hour, time.minute, time.second)+ "."
    tempfilename = filepath + filename + fileTypeH264
    fullfilename = filepath + filename + fileTypeVideo
    camera.start_recording(tempfilename, format='h264')
    camera.wait_recording(timeout=captureDuration)
    camera.stop_recording()
    print "end video capture: " + tempfilename
    subprocess.call("MP4Box -add %s %s" % (tempfilename, fullfilename), shell=True)
    print "video converted: " + fullfilename
    subprocess.Popen("/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload %s %s" % (fullfilename, filename+fileTypeVideo), shell=True)
    print "uploading to dropbox: " + filename+fileTypeVideo
    os.remove(tempfilename)
    print "temp file removed"
# def saveImage(width, height, diskSpaceToReserve):
#     keepDiskSpaceFree(diskSpaceToReserve)
#     time = datetime.now()
#     filename = filenamePrefix + "%04d%02d%02d-%02d%02d%02d" % (time.year, time.month, time.day, time.hour, time.minute, time.second)+ "." + fileTypeImage
#     fullfilename = filepath + filename
#     camera.resolution = (saveWidth, saveHeight)
#     camera.capture(fullfilename, format='jpeg', use_video_port=True)
#     # subprocess.call("echo %s > temp.out" % filename, shell=True)
#     subprocess.Popen("/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload %s %s" % (fullfilename, filename), shell=True)
#     # msg = email.MIMEMultipart.MIMEMultipart()
#     # msg['From'] = fromaddr
#     # msg['To'] = tolist
#     # msg['Subject'] = sub
#     # msg.attach(MIMEText('\nsent via python', 'plain'))
#     # server.sendmail(user,tolist,msg.as_string())
#     # print "Captured image: %s" % filename
#     # camera.wait_recording(60)
#     # Keep free space above given level
def keepDiskSpaceFree(bytesToReserve):
    if (getFreeSpace() < bytesToReserve):
        for filename in sorted(os.listdir(filepath)):
            if filename.startswith(filenamePrefix) and filename.endswith("." + fileTypeVideo):
                os.remove(filepath + filename)
                subprocess.Popen("/home/pi/Dropbox-Uploader/dropbox_uploader.sh delete %s" % (filename), shell=True)
                # print "Deleted %s to avoid filling disk" % filename
                if (getFreeSpace() > bytesToReserve):
                    return
                    # Get available disk space
def getFreeSpace():
    st = os.statvfs(filepath)
    du = st.f_bavail * st.f_frsize
    return du
    #---------------------------------------------------------
    # Start capturing video
# camera.resolution = (320, 240)
# camera.framerate = 10
# camera.start_recording(sys.stdout, format='h264')
# camera.capture_continuous(sys.stdout, format='yuv', use_video_port=True, resize=(320x240))
# Get first image
time.sleep(3)
image1, buffer1 = captureTestImage()
# Reset last capture time
lastCapture = time.time()
# added this to give visual feedback of camera motion capture activity.  Can be removed as required
os.system('clear')
f = open('./logfile','w')
f.write('            Motion Detection Started')
f.write('            ------------------------')
# print "Pixel Threshold (How much)   = " + str(threshold)
# print "Sensitivity (changed Pixels) = " + str(sensitivity)
# print "---------- Motion Capture File Activity --------------"
while (True):
    # Get comparison image
    try:
        image2, buffer2 = captureTestImage()
    except Exception:
        # subprocess.call("echo 'timeout' > temp.out", shell=True)
        # f.write(ex)
        pass
            # Count changed pixels
    changedPixels = 0
    takeVideo = False
    for x in xrange(0, 100):
        # Scan one line of image then check sensitivity for movement
        for y in xrange(0, 75):
            # Just check green channel as it's the highest quality channel
            pixdiff = abs(buffer1[x,y][1] - buffer2[x,y][1])
            if pixdiff > threshold:
                changedPixels += 1
        # Changed logic - If movement sensitivity exceeded then
        # Save image and Exit before full image scan complete
            if (changedPixels > sensitivity):
                takeVideo = True
                # lastCapture = time.time()
                # saveVideo(saveWidth, saveHeight, diskSpaceToReserve)
                # saveImage(saveWidth, saveHeight, diskSpaceToReserve)
                # for i in range(10):
                #     time.sleep(1)
                #     saveImage(saveWidth, saveHeight, diskSpaceToReserve)
                break
        if (changedPixels > sensitivity):
            break

    # Check force capture
    if forceCapture:
        if time.time() - lastCapture > forceCaptureTime:
            takeVideo = True
    # take a picture or video
    if takeVideo:
        lastCapture = time.time()
        saveVideo(saveWidth, saveHeight, diskSpaceToReserve)
        # saveImage(saveWidth, saveHeight, diskSpaceToReserve)
        # for i in range(DurationSetting):
        #     time.sleep(delayBtCapture)
        #     saveImage(saveWidth, saveHeight, diskSpaceToReserve)
        try:
            image2, buffer2 = captureTestImage()
        except Exception:
            # subprocess.call("echo 'timeout' > temp.out", shell=True)
            # f.write(ex)
            pass

    # Swap comparison buffers
    image1  = image2
    buffer1 = buffer2
#------------------------------------------------------------
