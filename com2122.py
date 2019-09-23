#!/usr/bin/env python
# coding=utf-8

import socket
import sys
import threading
import time
import os
from testSocket import _mapSocket


import fcntl

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
	tlist = []  # 线程列表，最终存放两个线程对象

	
	
	mapCon =[ 
	['192.168.31.121', 4196, 4021,'com2122'],
	['192.168.31.122', 4196, 4022,'com2122'],
	]

	lockName = "/home/pi/log/"  + str(mapCon[0][3]) +'.lock'
	ApplicationInstance(lockName)


	for i in range(2):
		t = threading.Thread(target=_mapSocket, args=(mapCon[i][0], mapCon[i][1], mapCon[i][2],mapCon[i][3]))
		tlist.append(t);
	
	
	for t in tlist:
		t.start()
	
	for t in tlist:
		t.join()
	
