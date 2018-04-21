'''
**************************************************
*               智能体监听模块                   *
*                                                *
*            1. 监听智能体控制器设置请求         *
*            2. 循环处理任务队列中的任务         *
*            3. 接收请求并执行                   *
*            4. 添加新的任务类型                 *
*            5. 拓展输入输出数据库               *
*                                                *
*            author: joliu<joliu@s-an.org>       *
*            date:   2018-3-21                   *
*            modify: 2018-4-16                   *
**************************************************
'''

import socket
import threading
import socketserver
import json
import os
import time
import subprocess
import logging
import sqlite3


from controllMatrix import *

# 两种控制模式，controller:控制器写入控制命令，device：接收其他传感器控制命令
controlModeList = ['controller', 'device']
controlMethodList = ['addInput','addOutput', 'addCach', 'rm', 'clear', 'period', 'show', 'start', 'stop']

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    '''
    消息监听模块
    '''
    def handle(self):
        # 设备忙碌标识
        busyFlag = False
        # 错误标识
        errorFlag = False

        try:
            # 接收socket消息
            data = self.request.recv(1024).decode()
        except socket.error as err_msg:
            # 返回异常信息
            (status, output) = (-1, err_msg)
            # 异常处理
            print("recv error!")
            exit(1)

        message = data.split('&')

        # 检测控制模式
        controlMode = message[0]
        print(message)
        if controlMode in controlModeList:
            if controlMode == "controller":
                # 写入控制命令到任务队
                print(message[1])
                command = message[1]
                # 检测是否是合法操作
                if not command in controlMethodList:
                    print("error: illegal command")
                    errorFlag = True
                    (status, output) = (-1, "illegal controller command: %s" % command)
                else:
                    # 匹配控制指令做出相应操作
                    (status, output) = executeCommand(command, message[2:])
                    print(message[2:])

            # 监听来自device hfv模块的控制请求
            elif controlMode == "device":
                deviceID = message[1]
                data = message[2]
                # 发送控制请求
                # (status, output) = sendCommandToDevice(command)
                (status, output) = updateDataCach(deviceID, int(data))
                print(deviceID, data)
                #(status, output) = (1, "test")
            else:
                pass
        else:
            print("illegal controlMode!")
            (status, output) = (-1, 'illegal controlMode')
            errorFlag = True

        # 返回控制命令执行结果
        jresp = json.dumps((status, str(output)))
        try:
            self.request.sendall(jresp.encode())
        except socket.error as err_msg:
            print("socket failed %s" % err_msg)
            exit(1)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


# 发送控制指令到Device
def sendCommandToDevice(cmd):
    # 通过容器的环境变量HOST获取绑定传感器的IP地址
    ip, port = os.getenv('HOST'), 8085
    return sendBySocket(ip, port, cmd)


# 通过socket发送信息
def sendBySocket(ip, port, cmd):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err_msg:
        print("Error creating socket:%s" % err_msg)
        s.close()
        return (-1, err_msg)
    try:
        s.connect((ip, port))
    except socket.error as err_msg:
        print("Address-related error connecting to server: %s" % err_msg)
        s.close()
        return (-1, err_msg)

    print("****************send:" + cmd)
    try:
        s.sendall(cmd.encode())
    except socket.error as err_msg:
        print("Error sending data: %s" % err_msg)
        s.close()
        return (-1, err_msg)

    try:
        response = s.recv(1024).decode()
        print(response)
    except socket.error as err_msg:
        print("Error receiving data: %s" % err_msg)
        s.close()
        return (-1, err_msg)

    print(str(response))
    s.close()
    # 程序运行正常返回目标传感器返回的数据
    return (1, str(response))


# 执行控制指令
def executeCommand(command, information):
    # comand:input/output, information:将要存入数据库的内容
    if command == 'addInput':
        (data, dstIP, circleTime) = information
        return updateDeviceTask(data, dstIP, int(circleTime))
    elif command == 'addOutput':
        clearDB()
        (taskMatrixJOSN, deviceTypeListJOSN, deviceListJOSN, taskStatus,\
             circleTime) = information
        return insertDB(taskMatrixJOSN, deviceTypeListJOSN, deviceListJOSN,\
                            int(taskStatus), int(circleTime))
        
    elif command == 'addCach':
        data = information[0]
        data = json.loads(data)
        for i in range(len(data[0])):
            (status, output) = insertDataIntoDataCach(data[0][i])
            (status, output) = updateDataCach(data[0][i], data[1][i])
        return (status, output)
    elif command == 'show':
        DBName = information[0]
        return showDatabase(DBName)
    elif command == 'clear':
        return clearDB()
    elif command == 'start':
        return updateTaskStatus(1)
    elif command == 'stop':
        return updateTaskStatus(0)


# 创建数据库
def createDB():
    conn = sqlite3.connect("task.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE if not exists task
                      (cmd text, hashtext text, ctime int(5))
                   """)
    conn.commit()
    cursor.close()
    conn.close()

# 创建输入数据库
def createInputDB():
    conn = sqlite3.connect("task.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE if not exists `decidedestination` (
                     `id` integer primary key autoincrement,
                     `data` tinyint NOT NULL,
                     `dst` varchar(3) NOT NULL,
                     `ctime` tinyint DEFAULT 2)
                   """)
    conn.commit()
    cursor.close()
    conn.close()


# 创建输出数据库
def createOutputDB():
    conn = sqlite3.connect("task.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE if not exists `resulovetable` (
                     `id` integer primary key autoincrement,
                     `taskmatrix` text NOT NULL,
                     `inputtype` text NOT NULL,
                     `status` tinyint DEFAULT 0,
                     `devicelist` text NOT NULL,
                     `ctime` tinyint DEFAULT 2)
                   """)
    conn.commit()
    cursor.close()
    conn.close()


# 创建数据缓存数据库
def createDataCach():
    conn = sqlite3.connect("task.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE if not exists `datacach` (
                      `id` integer primary key autoincrement,
                      `deviceid` varchar(30) NOT NULL,
                      `data` integer default -1,
                      `updatetime` varchar(30) NOT NULL,
                      `groupid` integer NOT NULL)
                   """)
    conn.commit()
    cursor.close()
    conn.close()


# 设置时间周期
def updatePeriod(cTime):
    try:
        sql = 'update task set ctime=' + str(cTime)
        conn = sqlite3.connect("task.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        (status, output) = (1, cTime)
    except sqlite3.Error as err_msg:
        print("Database error: %s", err_msg)
        (status, output) = (-1, err_msg)
    except Exception as err_msg:
        (status, output) = (-1, err_msg)
    finally:
        cursor.close()
        conn.close()
        return (status, output)

# 返回数据库内容
def showDatabase(tableName):
    tableNames = ['resulovetable', 'datacach', 'decidedestination']
    if not tableName in tableNames:
        return (-1, "no this table")
    return showDB(tableName)
if __name__ == "__main__":
    createInputDB()
    createOutputDB()
    createDB()
    createDataCach()
    # 设置host和port
    HOST, PORT = "0.0.0.0", 3000
    logger = logging.getLogger("TCPServer")
    logger.setLevel(logging.INFO)

    # 创建句柄
    fh = logging.FileHandler("1.log")

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -\
        %(message)s')
    # 添加句柄到logger类
    logger.addHandler(fh)

    logger.info("Program started")
    socketserver.TCPServer.allow_reuse_address = True
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # 启动多进程监听服务
    server_thread = threading.Thread(target=server.serve_forever)
    # 当主进程中断时退出程序
    server_thread.daemon = True
    server_thread.start()
    logger.info("Server loop running in thread:" + server_thread.name)
    logger.info("....waiting for connection")

    # 使用control + C 退出程序
    server.serve_forever()
