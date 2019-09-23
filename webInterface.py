# -  *  - coding:utf-8 -  *  - 
import socket
import sys
import paho.mqtt.client as mqtt

from multiprocessing import Process


MQTTHOST = "procontrol.top"
MQTTPORT = 1883
mqttClient = mqtt.Client()
socketCon = None

#mapCon = [ 
#	['192.168.1.207', 4196, 4017, 'com1718'], 
#	['192.168.1.208', 4196, 4018, 'com1718'], 
#	]




def _revRemote(conn, comStr):
    try:
        cnt = 0
        while True:			
            buff = ""
            buff = conn.recv(0x100)
            if len(buff) == 0:
                print ("remote closed")
                buff = ""
                break
            #else:
                #print('Rev ', comStr, ' '+ buff)
            try:
                ret = mqttClient.publish(comStr, buff, 1)
                if cnt % 30 == 0:
                    print('publish ', comStr,' ', cnt)
                cnt = cnt+1
            except:
                #print "send to Local failed:", len(buff), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                pass            
    except:
        print("_revRemote except while.")
    print("_revRemote closed.")
 
def RevMsg(mapCon):
    global socketCon
    comStr = str(mapCon[2])
    port1 = mapCon[1]
    host = mapCon[0]
    while True:
    	conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	try:
			conn.connect((host, port1))
			socketCon = conn  # 放入本端流对象
			_revRemote(conn, comStr)
			try:
				conn.shutdown(socket.SHUT_RDWR)
				conn.close()
				socketCon = None
			except:
				print ('can not connect %s:%i!' % (host, port1))
				pass
    	except Exception, e:
			print ('can not connect %s:%i!' % (host, port1))			
			time.sleep(5)


""" def TestConProcess():
    listP = []
    for i in range(len(mapCon)):
        p = Process(target = RevMsg, args = (mapCon, ))
        listP.append(p)
        print('new process is called', i)
       
    for p in listP:
        p.start()#向操作系统发送一个请求，操作系统会申请内存空间给，然后把父进程的数据拷贝给子进程，作为子进程的初始数据。
 """
        
# 连接MQTT服务器
def on_mqtt_connect(mapCon):
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)
    mqttClient.loop_start()
    comStr = str(mapCon[2])+'W'
    print('subscribe ', comStr)
    port1 = mapCon[1]
    host = mapCon[0]
    mqttClient.subscribe(comStr)
    mqttClient.on_message = on_message_come

    
# publish 消息
def on_publish(topic, payload, qos):
    mqttClient.publish(topic, payload, qos)
 
# 消息处理函数
def on_message_come(lient, userdata, msg):
    global socketCon
    if socketCon != None:
        try:
            socketCon.send(msg.payload)
        except:
            print ('can not connect ', socketCon)
            pass
    print(msg.topic + " " + ":" + str(msg.payload))
 
 
def startqtt(mapCon):
    on_mqtt_connect(mapCon)    
    RevMsg(mapCon)
    while True:
        pass
 
 
 
if __name__ == '__main__':
    mapCon1 = ['192.168.1.208', 4196, 4018, 'com1718']
    startqtt(mapCon1)
 