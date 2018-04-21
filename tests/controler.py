import socket
import sys
import numpy as np
import json

port = 33335

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


message = 'controller&addOutput&%s&%s&%s&0&2' % (jsnInputTask, jsnInputTypeList, jsnDeviceList)
# 执行逻辑矩阵数据库
#message = 'controller&show&resulovetable'
# 数据缓存数据库
#message = 'controller&show&datacach'
# 数据采集控制数据库
#message = 'controller&show&decidedestination'
#message = 'controller&clear'

# 模拟Device设备发送信息
# message = 'device&dht102&0'
# 输出
# message = 'controller&stop'

#message = 'controller&start'
# 添加轮询查询传感器命令
#message = "controller&addInput&20&192.168.12.19:33335&20"
# 添加缓存数据库内容
data = [["delay1", "dht102", "dht103", "dht104"],[10,1,0,1]]
data_json = json.dumps(data)
message = "controller&addCach&%s" % data_json
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.12.19", port))
s.sendall(message.encode())
response = s.recv(1024).decode()
print(response)
