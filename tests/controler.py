import socket
import sys
import numpy as np
import json

port = 3000

inputTask = np.array([[0,0,1,0,0,0,0,0],\
                      [0,0,1,0,0,0,0,0],\
                      [0,0,0,1,0,0,0,0],\
                      [0,0,0,0,1,0,0,0],\
                      [0,0,0,0,0,0,0,0],\
                      [1,0,0,0,0,0,0,0],\
                      [1,0,0,0,0,0,0,0],\
                      [0,1,0,0,0,0,0,0]])
inputTypeList = np.array([1,3,2,5,0,4,4,4])
deviceList = [-1,-1,-1,"delay1","switch103","dht102","dht103","dht104"]

jsnInputTask = json.dumps(inputTask.tolist())
jsnInputTypeList = json.dumps(inputTypeList.tolist())
jsnDeviceList = json.dumps(deviceList)


# message = 'controller&addOutput&%s&%s&%s&0&2' % (jsnInputTask, jsnInputTypeList, jsnDeviceList)
# 执行逻辑矩阵数据库
# message = 'controller&show&resulovetable'
# 数据缓存数据库
# message = 'controller&show&datacach'
# 数据采集控制数据库
# message = 'controller&show&decidedestination'
message = 'controller&clear'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.12.19", port))
s.sendall(message.encode())
response = s.recv(1024).decode()
print(response)
