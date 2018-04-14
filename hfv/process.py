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

import numpy as np

def resolveMatrix(inputTask, inputTypeList, outputNode, inputDeviceData):
    '''
    根据矩阵构建输入输出关系
    inputTask: 输入矩阵;inputTypeList: 节点类型列表，指明各个节点的具体功能;outputNode: 输出节点;
    inputDeviceData: 输入设备节点状态值
    '''
    nodeType = inputTypeList[outputNode]
    lastNode = np.where((inputTask.T[outputNode] == 1))[0]
    if nodeType == 0:
        output = resolveMatrix(inputTask, inputTypeList, lastNode[0], inputDeviceData)
    elif nodeType == 1:
        a = resolveMatrix(inputTask, inputTypeList, lastNode[0], inputDeviceData)
        b = resolveMatrix(inputTask, inputTypeList, lastNode[1], inputDeviceData)
        output =  a & b
    elif nodeType == 2:
        a = resolveMatrix(inputTask, inputTypeList, lastNode[0], inputDeviceData)
        b = resolveMatrix(inputTask, inputTypeList, lastNode[1], inputDeviceData)
        output = a | b
    elif nodeType == 3:
        a = resolveMatrix(inputTask, inputTypeList, lastNode[0], inputDeviceData)
        output = not a
    elif nodeType == 4:
        output = inputDeviceData[outputNode]
    return output


def checkMatrix(inputTask, inputTypeList):    
    # 测试矩阵是否符合要求
    length = inputTask.shape[0]
    zeroList = np.zeros(length)
    outputNode = np.where((inputTask == zeroList).all(1))[0]
    if outputNode.shape[0] != 1:
        print("输出节点不符合单输出要求")
        exit(1)
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


if __name__ == "__main__":
    # 测试程序
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

    if not checkMatrix(inputTask, inputTypeList):
        exit(1)

    # 获取矩阵宽度
    length = inputTask.shape[0]
    # 创建零向量
    zeroList = np.zeros(length)
    # 获取输出节点，即行为零向量
    outputNode = np.where((inputTask == zeroList).all(1))[0]
    # 获取输入节点，即列为零向量
    inputNodes = np.where((inputTask.T == zeroList).all(1))[0]


    print(resolveMatrix(inputTask, inputTypeList, outputNode[0], inputDeviceData))
