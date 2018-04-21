'''
*************************************************
*       任务流解析程序                          *
*       程序说明：                              *
*       1. 输入任务流矩阵                       *
*       1. 解析任务工作流                       *
*                                               *
*              author: joliu<joliu@s-an.org>    *
*              date: 2018-4-13                  *
*************************************************
'''
import json
import numpy as np
from controllMatrix import *


inputDeviceData = np.array([])

def resolveMatrix(inputTask, inputTypeList, outputNode):
    '''
    根据矩阵构建输入输出关系
    inputTask: 输入矩阵;inputTypeList: 节点类型列表，指明各个节点的具体功能;outputNode: 输出节点;
    inputDeviceData: 输入设备节点状态值
    更改获取实时的传感器数据
    '''
    nodeType = inputTypeList[outputNode]
    lastNode = np.where((inputTask.T[outputNode] == 1))[0]
    if nodeType == 0:
        output = resolveMatrix(inputTask, inputTypeList, lastNode[0])
    elif nodeType == 1:
        a = resolveMatrix(inputTask, inputTypeList, lastNode[0])
        b = resolveMatrix(inputTask, inputTypeList, lastNode[1])
        output =  a & b
    elif nodeType == 2:
        a = resolveMatrix(inputTask, inputTypeList, lastNode[0])
        b = resolveMatrix(inputTask, inputTypeList, lastNode[1])
        output = a | b
    elif nodeType == 3:
        a = resolveMatrix(inputTask, inputTypeList, lastNode[0])
        output = not a
    elif nodeType == 5:
        # 延时器
        sleepTime = getValueByNodeID(outputNode)[1]
        output = resolveMatrix(inputTask, inputTypeList, lastNode[0])
        time.sleep(sleepTime)
    elif nodeType == 4:
        print(outputNode)
        output = getValueByNodeID(outputNode)[1]
        print(output)
    return output


def checkMatrix(inputTask, inputTypeList): 
    # 验证数据数据库数据是否否和规定
    (status, output) = getDeviceListFromDB()
    if status == -1:
        print(output)
        return False
    (getTaskStatusStatus, taskStatus) = getTaskStatus()
    if getTaskStatusStatus == -1:
        print(taskStatus)
    if taskStatus == 0:
        print("Task has been stopped!")
        return False
    
    deviceList = json.loads(output)
    for device in deviceList:
        if device == -1:
            continue
        if device[:5] == 'delay':
            continue
        if device[:6] == 'switch':
            # 临时解决方案，把switch都作为输出屏蔽掉
            continue
        (runStatus, deviceStatus) = existDevice(device)
        if runStatus == -1:
            print(deviceStatus)
            return False
        if not deviceStatus:
            print("need to set datacach database")
            return False
        
    # 测试矩阵是否符合要求
    length = inputTask.shape[0]
    zeroList = np.zeros(length)
    outputNode = np.where((inputTask == zeroList).all(1))[0]
    if outputNode.shape[0] != 1:
        print("输出节点不符合单输出要求")
        return False
    # 验证inputTypeList与inputTask矩阵是否匹配，主要验证输入与类型是否一致
    for i in range(length):
        countInput = np.sum(inputTask.T[i] == 1)
        if inputTypeList[i] in [0,3]:
            if countInput == 1:
                continue
            else:
                print("请检查%d行" % i)
                return False
        elif inputTypeList[i] in [1,2]:
            if countInput == 2:
                continue
            else:
                print("请检查%d行" % i)
                return False
        elif inputTypeList[i] in [4]:
            if countInput == 0:
                continue
            else:
                print("请检查%d行" % i)
                return False
    return True


def runTask():
    # 输入各个节点的状态信息
    data = getTaskFromDB()
    if data == []:
        return (-1, 'No Task')
    (id, inputTask, inputTypeList, status, deviceList, ctime) = data[0]

    inputTask = np.array(json.loads(inputTask))
    inputTypeList = np.array(json.loads(inputTypeList))
    
    if not checkMatrix(inputTask, inputTypeList):
        return (-1, '矩阵检查不通过')

    # 获取矩阵宽度
    length = inputTask.shape[0]
    # 创建零向量
    zeroList = np.zeros(length)
    # 获取输出节点，即行为零向量
    outputNode = np.where((inputTask == zeroList).all(1))[0]
    # 获取输入节点，即列为零向量
    inputNodes = np.where((inputTask.T == zeroList).all(1))[0]


    return (1, resolveMatrix(inputTask, inputTypeList, outputNode[0]))


if __name__ == "__main__":
    inputData = [0,0,0,0,0,1,0,1]
    print(runTask())
    
