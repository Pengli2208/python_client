#!/usr/bin/env python
# coding=utf-8



import socket
import sys
import threading
import time

debug = 0 # 调试状态 0 


def _serialone(num1, num2, fw,streams_map):
	'''
	交换两个流的数据
	num为当前流编号,主要用于调试目的，区分两个回路状态用。
	'''
	try:
		while True:
			
			buff = ""
			buff = streams_map[num1].recv(0x100)
			if num1 == 1:
				print "rev:",len(buff), buff
			try:
				if num1 == 0:
					fw.write(buff)
					print "write:",len(buff), buff
			except:
				print "write failed:",len(buff), buff
				pass			
			
				
			if debug > 0:
				print num1,"recv"
			if len(buff) == 0: #对端关闭连接，读不到数据
				print num1,"one closed"
				buff=""
				break
			try:
				streams_map[num2].sendall(buff)
			except :
				pass
			if num1 == 1:
				print "send:" ,len(buff), buff
			if debug > 0:
				print num1,"sendall"
	except :
		print num1, " except while."
	try:
		streams_map[num1].shutdown(socket.SHUT_RDWR)
		streams_map[num1].close()
	except:
		pass
	
	try:
		if num1 == 0:
			fw.close()
	except:
		pass
	print num1, "CLOSED"


		
def _xstream_map(num, s1, s2, fw):
	'''
	交换两个流的数据
	num为当前流编号,主要用于调试目的，区分两个回路状态用。
	'''
	try:
		while True:
			#注意，recv函数会阻塞，直到对端完全关闭（close后还需要一定时间才能关闭，最快关闭方法是shutdow）
			#s1.settimeout(1.0)
			buff = ""
			buff = s1.recv(0x100)
			if num == 1:
				print "rev:",len(buff), buff
			try:
				if num == 0:
					fw.write(buff)
			except:
				pass			
			
				
		#	else:
		#		print "get:",len(buff), buff
			if debug > 0:
				print num,"recv"
			if len(buff) == 0: #对端关闭连接，读不到数据
				print num,"one closed"
				buff=""
				break
			#s2.settimeout(1.0)
			s2.sendall(buff)
			if num == 1:
				print "send:" ,len(buff), buff
			if debug > 0:
				print num,"sendall"
	except :
		print num, " except while."
	try:
		s1.shutdown(socket.SHUT_RDWR)
		s1.close()
	except:
		pass
	try:
		s2.shutdown(socket.SHUT_RDWR)
		s2.close()
	except:
		pass
	try:
		if num == 0:
			fw.close()
	except:
		pass
	print num, "CLOSED"
	
	
def _mapSocket(host,port1,port2):
	count = 0;
	streams_map = [None, None]  # 存放需要进行数据转发的两个数据流（都是SocketObj对象）
	filename = "/home/pi/log/" + str(port2) + ".log"
	#fo = open(filename,'a+')
	try:
		fo = open(filename,'a+')
	except Exception, e:
		print ('file open failed %s!' % (filename))
		pass
	print ('file open ok %s!' % (filename))
	while True:				
		conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			conn.connect((host, port1))
		except Exception, e:
			print ('can not connect %s:%i-:%i!' % (host, port1, count))
			not_connet_time += 1
			time.sleep(wait_time)
			continue
		print "connected to %s:%i:%i" % (host, port1,count)
#		conn.setblocking(0)
		
		streams_map[0] = conn  # 放入本端流对象
		
		tlist = []  # 线程列表，最终存放两个线程对象

		#t = threading.Thread(target=_serialone, args=(0, streams_map[0], streams_map[1], fo))
		#tlist.append(t)

		srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		srv.bind(('0.0.0.0', port2))
#		srv.setblocking(0)
		
		srv.listen(1)
		conn2, addr = srv.accept()
		print "connected from:", addr
		streams_map[1] = conn2  # 放入本端流对象	
		t = threading.Thread(target=_serialone, args=(0, 1, fo,streams_map))
		#t = threading.Thread(target=_xstream_map, args=(0, streams_map[0], streams_map[1], fo))
		tlist.append(t)
		t = threading.Thread(target=_serialone, args=(1, 0, fo,streams_map))
		#t = threading.Thread(target=_xstream_map, args=(1, streams_map[1], streams_map[0], fo))
		tlist.append(t)
		for t in tlist:
			t.start()
		for t in tlist:
			t.join()
		
		print "Closed all sockets:%i" % (count)
		
		
		
			
	sys.exit(0)
		

if __name__ == '__main__':
	
	if len(sys.argv) != 2:
		print 'error'
		sys.exit(1)
	print 'hello'
	targv = [sys.argv[0], sys.argv[1]]
	s = targv[1] 
	sl = s.split(':')
	if len(sl) == 3:  # host:port:port2
		print sl[0]
		print sl[1]
		print sl[2]
		t = threading.Thread(target=_mapSocket, args=(sl[0], int(sl[1]), int(sl[2])))
		t.start()
		t.join()
	else:
		print 'error argv'
		sys.exit(1)

	sys.exit(0)
