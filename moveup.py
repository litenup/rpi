import time
import os, sys
import pipan
import memcache

shared = memcache.Client(['127.0.0.1:11211'], debug=0)
y = shared.get('ypos')
p = pipan.PiPan()

if y > 110:
  y -= 2
  p.do_tilt(int(y))
  time.sleep(0.1)

shared.set('ypos', y)