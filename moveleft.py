import time
import os, sys
import pipan
import memcache

shared = memcache.Client(['127.0.0.1:11211'], debug=0)
x = shared.get('xpos')
p = pipan.PiPan()

if x < 180:
  x += 2
  p.do_pan(int(x))
  time.sleep(0.1)

shared.set('xpos', x)