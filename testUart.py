#!/usr/bin/env python
# coding=utf-8



import socket
import sys
import threading
import time
import serial
import datetime
import fcntl

debug = 0 # 调试状态 0 




def _serialone(streams_map,fw,seriDesp):
	length = 0
	count = 0
	'''
	交换两个流的数据
	num为当前流编号,主要用于调试目的，区分两个回路状态用。
	'''
	
	datenow=datetime.datetime.now()
	while True:
		try:
			ser = serial.Serial(seriDesp,115200,timeout=0.5) 
		except:
			sys.exit(1)
		ser.parity = serial.PARITY_NONE
		ser.stopbits = 1
		ser.timeout = 0.5
		ser.writeTimeout = 0.5
		ser.xonxoff = 0
		ser.rtscts = 0
		ser.dsrdtr = 0
		ser.interCharTimeout = 0.01
		count = count+1

		try:
			if ser.isOpen():
				ser.close()
			ser.open()
		except:
			print('serial port:%s -> failed to open!'%(seriDesp))
			ser.close()
			sys.exit(1)
		streams_map[0] = ser
		print( "connected to %s:%i" % (seriDesp,count))
		#print streams_map[0]
		try:
			while True:
			
				buff = ""
				buff = streams_map[0].read(100)
			
				if len(buff) > 0:
					length += len(buff)
					try:
						fw.write(buff)
						print( "read: ", seriDesp,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) #, len(buff), buff
					except:
						print( "write failed:",len(buff), buff)
						pass					
			
			
					try:
						streams_map[1].sendall(buff)
					except :
						pass
				try:
					if length > 0:
					
						if length > 1000 or (datetime.datetime.now() - datenow).seconds > 120 :
							length = 0
							fw.flush()
							datenow = datetime.datetime.now()
				except :
					print( 'flushed failed')
					pass
		except :
			print ("_serialone except while.")

	

	print( "Serial CLOSED")


def _socketone(streams_map):
	'''
	交换两个流的数据
	num为当前流编号,主要用于调试目的，区分两个回路状态用。
	'''
	try:
		while True:
			
			buff = ""
			buff = streams_map[1].recv(0x100)
			if len(buff) > 0:
				try:
				#	print streams_map[0]
					streams_map[0].write(buff)
					print("seri write: ",len(buff), buff, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))  #buff
				except:
					print("send failed:",len(buff), buff,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
					pass					
			else:
				print( "closed when not recv len < 1")
				break
			
	except :
		print ("_socketone except while.")
	try:
		streams_map[1].shutdown(socket.SHUT_RDWR)
		streams_map[1].close()

	except:
		pass
	
	
	print ("Socket CLOSED")


	
	
def _mapSocketUart(serPort,port2):
	count = 0;
	streams_map = [None, None,]  # 存放需要进行数据转发的两个数据流（都是SocketObj对象）
	filename = "/home/pi/log/serialport/" + str(port2) + '__'+time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()) +".log"
	
	try:
		fo = open(filename,'a+')
	except Exception, e:
		print ('file open failed %s!' % (filename))
		pass
	print ('file open ok %s!' % (filename))
	
	
	
	t1 = threading.Thread(target=_serialone, args=( streams_map,fo,serPort))
	t1.start()
	while True:		
		srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		srv.bind(('0.0.0.0', port2))
		
		srv.listen(1)
		conn2, addr = srv.accept()
		print "connected from:", addr
		streams_map[1] = conn2  # 放入本端流对象	
		
		_socketone(streams_map)
		
		
		print "Closed sockets:%i" % (count)
		
	t1.join()	
	try:
		fw.close()
	except:
		pass	
	sys.exit(0)
		
def _serialCon(arg1,arg2):
	tlist = []  # 线程列表，最终存放两个线程对象
	for i in range(1):
		t = threading.Thread(target=_mapSocketUart, args=(arg1, arg2))
		tlist.append(t);
	for t in tlist:
		t.start()	
	for t in tlist:
		t.join()

def lockFile(lockfile):  
	fp = open(lockfile, 'w')  
	try:  
		fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)  
		
	except IOError:  
		print "exception" 
		print lockfile
		return False  
	print "no exception"
	print lockfile	
	return True 


if __name__ == '__main__':
	
	if len(sys.argv) != 2:
		print 'error'
		sys.exit(1)
	print 'hello'
	targv = [sys.argv[0], sys.argv[1]]
	s = targv[1] 
	sl = s.split(':')
	_serialCon(targv[0],targv[1])
	sys.exit(0)
