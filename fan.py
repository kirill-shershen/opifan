# -*- coding: utf-8 -*-

import time
from subprocess import Popen, PIPE
import os

GATE_PIN = 7
CURDIR = os.getcwd()
def cmd(c, cwd = CURDIR, **opts):
    p = None
    try:
        p = Popen(c, cwd=cwd, shell=True, **opts)
        #p.wait()
        return p           
    except Exception as e:
        if not p:
            print 'error: %s' %e
        else:
            print 'error: code %d' % p.returncode

def stop():
    cmd('gpio write %d 0' % GATE_PIN)

def start():
    cmd('gpio write %d 1' % GATE_PIN)

def init():    
    cmd('gpio mode %d out' % GATE_PIN)
    start()
    
def get_temp():
    p = cmd('cat /sys/devices/virtual/thermal/thermal_zone0/temp', stdout=PIPE)
    if p:
        return p.stdout.read()

if __name__ == '__main__':
    cmd('echo $$ > /var/run/opifan.pid')
    init()
    while 1:
        try:
            temp = int(get_temp())
            if temp > 50:
                start()
            if temp <= 40:
                stop()
            time.sleep(60)
        except KeyboardInterrupt:
            stop()
