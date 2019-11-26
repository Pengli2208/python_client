#!/usr/bin/env python
# coding=utf-8

import socket
import sys
import threading
import time
import os
import fcntl
from webSerial import funcUartQtt
from webSerial import lockFile
import time


pidfile = 0  
  
def ApplicationInstance(locFile):  
	global pidfile  
	pidfile = open(locFile, "w")  
	try:  
		fcntl.lockf(pidfile, fcntl.LOCK_EX | fcntl.LOCK_NB)  #åˆ›å»ºä¸€ä¸ªæŽ’ä»–é”,å¹¶ä¸”æ‰€è¢«é”ä½å…¶ä»–è¿›ç¨‹ä¸ä¼šé˜»å¡ž  
	except  IOError:  
		print "another instance is running..."  
		sys.exit(0)  

time.sleep(50)
serPort = ['/dev/ttyUSB0', 5100, 5100,"/home/pi/log/serialport/"]
if not os.path.exists(serPort[3]):
    os.mkdir(serPort[3])

lockName = serPort[3]  + str(serPort[1]) +'.lock'
ApplicationInstance(lockName)

print('running')
funcUartQtt(serPort)
