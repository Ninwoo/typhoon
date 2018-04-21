'''
***********************************************************
*           控制矩阵数据库的相关函数                      *
*           1. resulovetable                              *
*                 author: joliu<joliu@s-an.org>           *
*                 date: 2018-4-14                         *
***********************************************************
'''

import sqlite3
import numpy as np
import json
import time

# ~~~~~~~~~~~~~~~~~~~inputDB操作函数~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 更新任务执行控制表
def updateDeviceTask(data, dstIP, ctime):
    sql = "select * from decidedestination where dst='%s'" % dstIP
    (status, output) = sendToDB(sql)
    print(output)
    print('***********',output)
    if status == -1:
        return (status, output)
    if output == []:
        sql = "insert into decidedestination (data,dst,ctime) values \
                  ('%s','%s',%d)" % (data, dstIP, ctime)
    else:
        sql = "update decidedestination set data='%s',dst='%s',ctime=%d" % \
                  (data, dstIP, ctime)
    return sendToDB(sql)


# 获取任务执行控制表
def getDeviceTask():
    sql = "select * from decidedestination"
    (status, output) = sendToDB(sql)
    if status == -1:
        return (status, output)
    # print(output)
    return (status, output)


# ~~~~~~~~~~~~~~~~~~~dataCach操作函数~~~~~~~~~~~~~~~~~~~~~~~~~~~

# 更新设备输入数据信息
def updateDataCach(device, decideValue):
    # 检查是否存在该设备在预接收的列表中，如果不存在则丢弃
    sql = "select * from datacach where deviceid='%s'" % device
    (status, output) = sendToDB(sql)
    if status == -1:
        return (-1, output)
    if output == []:
        return (-1, "drop this data")
    sql = "update datacach set data='%s', updatetime='%s' where deviceid='%s'" \
                % (decideValue, time.time(), device)
    return sendToDB(sql)


# 插入设备输入节点信息
def insertDataIntoDataCach(device):
    # 检查是否存在当前输入，如果有则插入
    sql = "select * from datacach where deviceid='%s'" % device
    (status, output) = sendToDB(sql)
    if status == -1:
        return (status, output)
    if output != []:
        return (1, 'device has been added') 
    # 在配置输入信息节点时，使用该函数插入
    sql = "insert into datacach (deviceid, updatetime, groupid) values \
              ('%s', '%s', %d)" % (device, time.time(), 1)
    return sendToDB(sql)

# 获取输入数据库的内容
def getDataFromDataCach(device):
    sql = "select data from datacach where deviceid='%s'" % device
    return sendToDB(sql)

# 判断是否存在相应的设备数据缓存信息
def existDevice(device):
    (status, output) = getDataFromDataCach(device)
    print(device, output)
    if status == -1:
        retrun (status, output)
    if output == []:
        return (1, False)
    else:
        return (1, True) 

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 以下都是对output的数据库，即存储任务矩阵的数据库的操作
# 获取设备列表
def getDeviceListFromDB():
    sql = "select devicelist from resulovetable"
    (status, output) = sendToDB(sql)
    if status == -1:
        return (status, output)
    if output == []:
        return (-1, 'no deviceList')
    return (status, output[0][0])


# 获取任务执行状态
def getTaskStatus():
    sql = "select status from resulovetable"
    (status, output) = sendToDB(sql)
    print(output)
    if status == -1:
        return (status, output)
    if output == []:
        return (-1, 'no deviceList')
    return (status, output[0][0])


# 更新任务执行状态
def updateTaskStatus(taskStatus):
    (status, output) = getTaskStatus()
    if status == -1:
        return (status, output)
    sql = 'update resulovetable set status=%d' % taskStatus
    return sendToDB(sql)


# 插入任务到数据库
def insertDB(taskMatrix, inputTypeList, deviceList, status, ctime):
    sql = "insert into resulovetable \
               (taskmatrix,inputtype, status, devicelist, ctime) values \
               ('%s','%s',%d,'%s',%d)" % (taskMatrix, inputTypeList, status, deviceList, ctime)

    return sendToDB(sql)


def sendToDB(sql):
    try:
        conn = sqlite3.connect("task.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        status = 1
        if sql.split(' ')[0] == 'select':
            output = cursor.fetchall()
        else:
            conn.commit()
            output = 'success'
    except sqlite3.Error as err_msg:
        (status, output) = (-1, err_msg)
    except Exception.Error as err_msg:
        (status, output) = (-1, err_msg)
    finally:
        cursor.close()
        conn.close()
        return (status, output)

def getTaskFromDB():
    # 查询最新一条可用任务
    sql = 'select * from resulovetable order by id desc limit 0,1'
    (status, output) = sendToDB(sql)
    return output

def getTaskFromDBByID(id):
    # 从数据库中获取数据
    sql = 'select * from resulovetable where id=%d' % id
    (status, output) = sendToDB(sql)
    return output[0]

def getValueByNodeID(nodeid):
    # 获取devicelist
    (id, inputTask, inputTypeList, status, deviceList, ctime) = getTaskFromDB()[0]
    device = json.loads(deviceList)[nodeid]
    if device == -1:
        return (-1, "not a device")
    data = getDataFromDataCach(device)
    if data[1] == []:
        return (-1, "not found device")
    if data[1][0][0] == '-':
        # 这里将缺省值都默认设置为0
        return (1, 0)
    return (1, int(data[1][0][0]))


# 获取循环时间
def getCircleTime():
    data = getTaskFromDB()[0]
    if data == ():
        return 5
    return data[5]


def showDB(tableName):
    # 打印数据库内容
    sql = "select * from %s" % tableName

    return sendToDB(sql)


def clearDB():
    # 清空数据库
    dbNames = ['resulovetable', 'datacach', 'decidedestination']
    for name in dbNames:
        sql = "delete from %s" % name
        (status, output) = sendToDB(sql)
        if status == -1:
            break
    return (status, output)


if __name__ == '__main__':
    '''
    clearDB()
    inputTask = np.array([[0,0,1,0,0,0,0,0],\
                          [0,0,1,0,0,0,0,0],\
                          [0,0,0,1,0,0,0,0],\
                          [0,0,0,0,1,0,0,0],\
                          [0,0,0,0,0,0,0,0],\
                          [1,0,0,0,0,0,0,0],\
                          [1,0,0,0,0,0,0,0],\
                          [0,1,0,0,0,0,0,0]])
    inputTypeList = np.array([1,3,2,5,0,4,4,4])
    inputDeviceData = np.array([0,0,0,5,0,1,1,0])
    jsnInputTask = json.dumps(inputTask.tolist())
    jsnInputTypeList = json.dumps(inputTypeList.tolist())
    deviceList = [-1,-1,-1,"delay1","switch103","dht102","dht103","dht104"]
    jsnDeviceList = json.dumps(deviceList)
    insertDB(jsnInputTask, jsnInputTypeList, jsnDeviceList, 1, 2)
    '''
    # 添加输入信息到输入信息缓存中
    data = [["delay1", "dht102", "dht103", "dht104"],[10,1,0,1]]
    for i in range(len(data[0])):
        insertDataIntoDataCach(data[0][i])
        updateDataCach(data[0][i], data[1][i])
    #showDB()
    (id, inputTask, inputTypeList, status, deviceList, ctime) = getTaskFromDB()[0]
    #print(inputTask)
    print(getValueByNodeID(6))
