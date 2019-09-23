#!/usr/bin/env python
# coding=utf-8

import socket
import sys
import threading
import time
import os
from testSocket import _mapSocket


tlist = []  # 线程列表，最终存放两个线程对象

mapCon =[ 
['192.168.31.79', 4196, 4011],
['192.168.31.202', 4196, 4012],
['192.168.31.234', 4196, 4013],
['192.168.31.46', 4196, 4014],
['192.168.31.174', 4196, 4015],
['192.168.31.41', 4196, 4016],
['192.168.31.67', 4196, 4017],
['192.168.31.245', 4196, 4018],
['192.168.31.12', 4196, 4021],
['192.168.31.25', 4196, 4022],
['192.168.31.90', 4196, 4023],
['192.168.31.63', 4196, 4024],
['192.168.31.221', 4196, 4025],
['192.168.31.45', 4196, 4026],
['192.168.31.171', 4196, 4027],
['192.168.31.110', 4196, 4028],
]

for i in range(16):
	t = threading.Thread(target=_mapSocket, args=(mapCon[i][0], mapCon[i][1], mapCon[i][2]))
	tlist.append(t);
	
	
for t in tlist:
	t.start()
	
for t in tlist:
	t.join()
	