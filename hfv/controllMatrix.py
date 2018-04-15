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


# 插入任务到数据库
def insertDB(taskMatrix, inputTypeList, deviceList, status):
    sql = "insert into resulovetable \
               (taskmatrix,inputtype, status, devicelist) values \
               ('%s','%s',%d,'%s')" % (taskMatrix, inputTypeList, status, deviceList)
    print(sendToDB(sql))


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
    return output[0]

def getTaskFromDBByID(id):
    # 从数据库中获取数据
    sql = 'select * from resulovetable where id=%d' % id
    (status, output) = sendToDB(sql)
    return output[0]


def showDB():
    # 打印数据库内容
    sql = "select * from resulovetable"
    print(sendToDB(sql))


def clearDB():
    # 清空数据库
    sql = "delete from resulovetable"
    print(sendToDB(sql))



if __name__ == '__main__':
    inputTask = np.array([[0,0,1,0,0,0,0,0],\
                          [0,0,1,0,0,0,0,0],\
                          [0,0,0,1,0,0,0,0],\
                          [0,0,0,0,1,0,0,0],\
                          [0,0,0,0,0,0,0,0],\
                          [1,0,0,0,0,0,0,0],\
                          [1,0,0,0,0,0,0,0],\
                          [0,1,0,0,0,0,0,0]])
    inputTypeList = np.array([1,3,2,3,0,4,4,4])
    inputDeviceData = np.array([0,0,0,0,0,1,1,0])
    jsnInputTask = json.dumps(inputTask.tolist())
    jsnInputTypeList = json.dumps(inputTypeList.tolist())
    deviceList = [-1,-1,-1,-1,-1,"dht102","dht103","dht104"]
    jsnDeviceList = json.dumps(deviceList)
    # insertDB(jsnInputTask, jsnInputTypeList, jsnDeviceList, 1)
    showDB()
    (id, inputTask, inputTypeList, status, deviceList) = getDataFromDB(8)
    print(inputTask)
    # clearDB()
