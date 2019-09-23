#!/usr/bin/env python
# coding=utf-8

import socket
import sys
import threading
import time
import os
import fcntl
from testUart import _serialCon
from testUart import lockFile

pidfile = 0  
  
def ApplicationInstance(locFile):  
	global pidfile  
	pidfile = open(locFile, "w")  
	try:  
		fcntl.lockf(pidfile, fcntl.LOCK_EX | fcntl.LOCK_NB)  #创建一个排他锁,并且所被锁住其他进程不会阻塞  
	except  IOError:  
		print "another instance is running..."  
		sys.exit(0)  

if __name__ == '__main__':
	
	
	mapCon =[ 
	['/dev/ttyUSB2', 5102],
	]

	lockName = "/home/pi/log/serialport/"  + str(mapCon[0][1]) +'.lock'
	ApplicationInstance(lockName)
	print 'running'	
	_serialCon(mapCon[0][0], mapCon[0][1])

	sys.exit(0)

	
