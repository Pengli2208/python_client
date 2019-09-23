#!/usr/bin/env python
# coding=utf-8


import socket
import sys
import threading
import time
import serial
import datetime
import fcntl
import os
debug = 0  # 调试状态 0
import socket
import sys
import paho.mqtt.client as mqtt
import traceback
from multiprocessing import Process


MQTTHOST = "procontrol.top"
MQTTPORT = 1883
mqttClient = mqtt.Client()
socketCon = None
comStr4Server = "5100W"#from server,
comStr2Server = "5100"#to server
streams_map = [None, None, ]  # 存放需要进行数据转发的两个数据流（都是SocketObj对象）
sendCounter = 0

filename = "test1.log"
newFileReq = True
# 连接MQTT服务器
def on_mqtt_connect(mapCon):
    #mapCon = ['/dev/ttyUSB0', 5100, 5100],
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)    
    mqttClient.on_message = on_message_come
    mqttClient.loop_start()
    comStr2Server = str(mapCon[2])
    comStr4Server = comStr = str(mapCon[2])+'W'
    print('subscribe ', comStr)
    
    mqttClient.subscribe(comStr)

    
# publish 消息
def on_publish(topic, payload, qos):
    mqttClient.publish(topic, payload, qos)
 
# 消息处理函数
def on_message_come(client, userdata, msg):
    send2local(msg.payload)
    print(msg.topic + " " + ":" + str(msg.payload))
 
 
def startqtt(mapCon):
    on_mqtt_connect(mapCon)    
    
    while True:
        time.sleep(1)
 
 
 
def send2local(buff):
	'''
	交换两个流的数据
	num为当前流编号,主要用于调试目的，区分两个回路状态用。
	'''
	if len(buff) > 0:
		try:
			#	print streams_map[0]
			streams_map[0].write(buff)
			print("seri write: ", len(buff), buff, time.strftime(
				"%Y-%m-%d %H:%M:%S", time.localtime()))  # buff
		except:
			print("send failed:", len(buff), buff, 
				time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
			pass

def send2Server(buff,port2):
	try:
		global sendCounter
		comStr = str(port2)
		ret = mqttClient.publish(comStr, buff, 1)
	except Exception, e:
		print("send to Local failed:", len(buff), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		print("exception,", e)
		pass 

	print('publish ', comStr,' ', sendCounter)
	if sendCounter % 30 == 0:
		print('publish ', comStr,' ', sendCounter)
	sendCounter = sendCounter+1

def WriteToFile(path1, port2, buff):
	global newFileReq
	global filename
	if newFileReq:
		filename = path1 + \
			str(port2) + '__'+time.strftime("%Y-%m-%d %H-%M-%S",
										time.localtime()) + ".log"
		newFileReq = False
	try:
		fw = open(filename, 'a+')
		fw.write(buff)
		fw.close()
	except Exception, e:
		print('file open failed !', (filename))
		pass
	try:
		fsize = os.path.getsize(filename)
		print(fsize)
		if fsize > 1024*1024*10:			
			newFileReq = True
	except Exception, e:
		print("exception,", e)
		pass
	




def serialThread(path1,port2,seriDesp):
	length = 0
	count = 0
	'''
	交换两个流的数据
	num为当前流编号,主要用于调试目的，区分两个回路状态用。
	'''

	while True:
		try:
			ser = serial.Serial(seriDesp, 115200, timeout=0.5)
		except:
			break
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
			print('serial port:%s -> failed to open!' % (seriDesp))
			ser.close()
			sys.exit(1)
		streams_map[0] = ser
		print("connected to %s:%i" % (seriDesp, count))
		newFileReq = True
		try:
			while True:
				buff = ""
				buff = streams_map[0].read(500)
				if len(buff) > 0:
					length += len(buff)
					WriteToFile(path1,port2,buff)
					send2Server(buff,port2)                
		except:
			print("_serialone except while.")
	print("Serial CLOSED")




def funcUartQtt(serPort):
	#serPort = ['/dev/ttyUSB0', 5100, 5100],
	path1 = serPort[3]
	if not os.path.exists(path1):
		os.mkdir(path1)	
	t1 = threading.Thread(target=serialThread, args=(path1,serPort[1],serPort[0]))
	p1 = threading.Thread(target=startqtt,args=(serPort,))
	t1.start()
	p1.start()
	p1.join()	
	t1.join()	
	sys.exit(0)
		

def lockFile(lockfile):  
	fp = open(lockfile, 'w')  
	try:  
		fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)  
		
	except IOError:  
		print ("exception" )
		print lockfile
		return False  
	print ("no exception")
	print lockfile	
	return True 


if __name__ == '__main__':
	
	if len(sys.argv) != 2:
		print('error')
		sys.exit(1)
	print('hello')
	targv = [sys.argv[0], sys.argv[1]]
	s = targv[1] 
	sl = s.split(':')
	_serialCon(targv[0],targv[1])
	sys.exit(0)
