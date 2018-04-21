from controllMatrix import *
from resolveMatrix import runTask
import os

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

if __name__ == '__main__':
    time.sleep(10)
    while True:
        (status, output) = runTask()
        if status == -1:
            print(output)
            time.sleep(20)
            continue
        else:
            if output == 1:
                msg = 'on'
                print('on')
            else:
                msg = 'off'
                print('off')
        print(sendCommandToDevice(msg))
    
    ctime = getCircleTime()
    time.sleep(ctime)
