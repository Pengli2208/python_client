#!/usr/bin/env python
# coding=utf-8



import socket
import sys
import threading
import time

debug = 0 # 调试状态 0 
local_id = 1
remote_id = 0

def _revRemote(streams_map,fw,port2):
	try:
		while True:			
			buff = ""
			buff = streams_map[remote_id].recv(0x100)
			
			#print "rev:",len(buff), buff
			try:
				fw.write(buff)
				print "write: ", port2, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
			except:
				print "write failed:",len(buff),buff
				pass			
			
				
		
			if len(buff) == 0: 
				print "remote closed"
				buff=""
				break
			try:
				streams_map[local_id].sendall(buff)
			except :
				#print "send to Local failed:" ,len(buff), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
				pass
			
			#print "send:" ,len(buff), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
			
	except :
		print "_revRemote except while."
	print "_revRemote closed."
	
	
#from remote to loale and file
def _fromRemote(fw,streams_map,host, port1,port2):
	while True:
		conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			conn.connect((host, port1))
			streams_map[remote_id] = conn  # 放入本端流对象
			print streams_map[remote_id] 
			_revRemote(streams_map,fw,port2)
			try:
				conn.shutdown(socket.SHUT_RDWR)
				conn.close()
				streams_map[remote_id] = None
			except:
				pass
		except Exception, e:
			print ('can not connect %s:%i!' % (host, port1))			
			time.sleep(5)

	print " _fromRemote CLOSED"

#from local to remote
def _fromLocal(streams_map):
		
	
	while True:
		try:
			buff = ""
			buff = streams_map[local_id].recv(0x100)
			print "local rev:" ,len(buff), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
			if len(buff) == 0: #对端关闭连接，读不到数据
				print "local closed"
				break
			else:
				try:
					streams_map[remote_id].sendall(buff)
					print "send to Server:" ,len(buff), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
					#test
					#break#test only
				except :
					print "send to remote failed:" ,len(buff), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
					break
		except :
			print  "_fromLocal except while."
			break
	streams_map[local_id].shutdown(socket.SHUT_RDWR)
	streams_map[local_id].close()
	streams_map[local_id] = None	
	print "_fromLocal closed."

	
def _mapSocket(host,port1,port2,folder):
	streams_map = [None, None]  # 存放需要进行数据转发的两个数据流（都是SocketObj对象）
	filename = '/home/pi/log/'+folder +'/'+ str(port2) +'__'+ time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()) +".txt"
	#fo = open(filename,'a+')
	try:
		fo = open(filename,'a+')
	except Exception, e:
		print ('file open failed %s!' % (filename))
		pass
	print ('file open ok %s!' % (filename))
	
	t1 = threading.Thread(target=_fromRemote, args=(fo,streams_map,host,port1,port2))
	t1.start()
	while True:				
		try:
			srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			srv.bind(('0.0.0.0', port2))
			srv.listen(1)
			conn2, addr = srv.accept()
			print "connected from:", addr
			streams_map[local_id] = conn2  # 放入本端流对象	
			_fromLocal( streams_map)
		except:
			pass
		
	t1.join()	
	
	try:
		fw.close()
	except:
		pass
	
	sys.exit(0)
		

if __name__ == '__main__':
	
	if len(sys.argv) != 2:
		print 'error'
		sys.exit(1)
	print 'hello'
	targv = [sys.argv[0], sys.argv[1]]
	s = targv[1] 
	sl = s.split(':')
	if len(sl) == 4:  # host:port:port2
		print sl[0]
		print sl[1]
		print sl[2]
		print sl[3]
		t = threading.Thread(target=_mapSocket, args=(sl[0], int(sl[1]), int(sl[2]), sl[3]))
		t.start()
		t.join()
	else:
		print 'error argv'
		sys.exit(1)

	sys.exit(0)
