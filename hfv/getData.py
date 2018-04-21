from controllMatrix import *
from listenSer import sendBySocket
import os
import time
import socket
# 发送控制指令到传感器设备，参数cmd，控制命令
def sendCommandToDevice(cmd):
    response = 'error'
    # 通过容器的环境变量HOST获取绑定传感器的IP地址
    ip, port = os.getenv('HOST'), 8085
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err_msg:
        print("Error creating socket:%s" % err_msg)
        s.close()
        return (-1, err_msg)
    try:
        s.connect((ip, port))
    except socket.gaierror as err_msg:
        print('Address-related error connecting to server: %s' % err_msg)
        s.close()
        return (-1, err_msg)

    try:
        s.sendall(cmd.encode())
    except socket.error as err_msg:
        print("Error sending data: %s" % err_msg)
        s.close()
        return (-1, err_msg)
    try:
        response = s.recv(1024).decode()
    except socket.error as err_msg:
        print('Error receiving data: %s' % err_msg)
        s.close()
        return (-1, err_msg)
    s.close()
    # 程序运行正常，返回传感器传递的值
    return (1, str(response))

while True:
    ctime = 5
    (status, output) = getDeviceTask()
    if status == -1:
        print(output)
        continue
    for data in getDeviceTask()[1]:

        (id, data, dstIP, ctime) = data
        (ip, port) = dstIP.split(':')
        print(data)
        (status, deviceValue) = sendCommandToDevice('on')
        if status == -1:
            print(deviceValue)
            continue
        time.sleep(2)
        try:
            deviceValue = float(deviceValue.split('&')[0])
        except Exception as err:
            print(err,deviceValue)
        if deviceValue > data:
            print('1')
            msg = 'device&%s&1' % os.getenv('HOSTNAME')
            
        else:
            print('0')
            msg = 'device&%s&0' % os.getenv('HOSTNAME')
        
        (status, recvdata) = sendBySocket(ip, int(port), msg)
    time.sleep(ctime)
