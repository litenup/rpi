import time
import os, sys
import pipan
import memcache

p = pipan.PiPan()
x = 150
y = 150

shared = memcache.Client(['127.0.0.1:11211'], debug=0)
shared.set('xpos', x)
shared.set('ypos', y)

#move down and up
p.do_tilt(80)
time.sleep(0.5)
p.do_tilt(220)
time.sleep(0.5)

#center camera
p.do_tilt(int(x))
p.do_pan(int(x))

