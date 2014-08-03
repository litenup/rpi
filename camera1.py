import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (800, 600)
    camera.capture('foo.jpg', use_video_port=True)