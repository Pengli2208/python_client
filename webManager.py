# -  *  - coding:utf-8 -  *  - 
import socket
import sys
import paho.mqtt.client as mqtt

from multiprocessing import Process
from webInterface import startqtt
'''
mapCon = [
    ['192.168.1.201', 4196, 4011],
	['192.168.1.202', 4196, 4012],
    ['192.168.1.203', 4196, 4013],
    ['192.168.1.204', 4196, 4014],
    ['192.168.1.205', 4196, 4015],
    ['192.168.1.206', 4196, 4016],
    ['192.168.1.207', 4196, 4017],
    ['192.168.1.208', 4196, 4018],

    ['192.168.1.211', 4196, 4021],
	['192.168.1.212', 4196, 4022],
    ['192.168.1.213', 4196, 4023],
    ['192.168.1.214', 4196, 4024],
    ['192.168.1.215', 4196, 4025],
    ['192.168.1.216', 4196, 4026],
    ['192.168.1.217', 4196, 4027],
    ['192.168.1.218', 4196, 4028],

    ['192.168.1.221', 4196, 4031],
	['192.168.1.222', 4196, 4032],
    ['192.168.1.223', 4196, 4033],
    ['192.168.1.224', 4196, 4034],
    ['192.168.1.225', 4196, 4035],
    ['192.168.1.226', 4196, 4036],
    ['192.168.1.227', 4196, 4037],
    ['192.168.1.228', 4196, 4038],

    ['192.168.1.41', 4196, 4041],
	['192.168.1.42', 4196, 4042],
    ['192.168.1.43', 4196, 4043],
    ['192.168.1.44', 4196, 4044],
    ['192.168.1.45', 4196, 4045],
    ['192.168.1.46', 4196, 4046],
    ['192.168.1.47', 4196, 4047],
    ['192.168.1.48', 4196, 4048],

    ['192.168.1.51', 4196, 4051],
	['192.168.1.52', 4196, 4052],
    ['192.168.1.53', 4196, 4053],
    ['192.168.1.54', 4196, 4054],
    ['192.168.1.55', 4196, 4055],
    ['192.168.1.56', 4196, 4056],
    ['192.168.1.57', 4196, 4057],
    ['192.168.1.58', 4196, 4058],

    ['192.168.1.61', 4196, 4061],
	['192.168.1.62', 4196, 4062],
    ['192.168.1.63', 4196, 4063],
    ['192.168.1.64', 4196, 4064],
    ['192.168.1.65', 4196, 4065],
    ['192.168.1.66', 4196, 4066],
    ['192.168.1.67', 4196, 4067],
    ['192.168.1.68', 4196, 4068],

]
'''
mapCon = [
    ['192.168.1.201', 4196, 4011],
    ['192.168.1.202', 4196, 4012],
    ['192.168.1.203', 4196, 4013],
    ['192.168.1.204', 4196, 4014],
    ['192.168.1.205', 4196, 4015],
    ['192.168.1.206', 4196, 4016],
    ['192.168.1.207', 4196, 4017],
    ['192.168.1.208', 4196, 4018],
]

if __name__ == '__main__':
    listP = []
    for p in mapCon:
        p1 = Process(target=startqtt,args=(p,))
        listP.append(p1)
    for p in listP:
        p.start()
