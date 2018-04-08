#:coding:utf-8
'''
**********************************************
*         web服务器后台接口                  *
*       程序说明:                            *
*       1. 使用Flask实现的web API接口        *
*       2. 接收前端传进的json数组            *
*       3. 调用控制器传递控制指令            *
*                                            *
*       author: joliu<joliu@s-an.org>        *
*       date:   2018-4-7                     *
**********************************************
'''


from flask import Flask, abort, jsonify
from flask import request
from flask_cors import *

import json
import socket

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/controller/hello/')
def hello():
    return 'hello'

@app.route('/controller/run/', methods=['POST'])
def run():
    nodeList = []
    for i in range(10):
        try:
            nodeData = request.form[str(i)]
            nodeList.append(nodeData)
        except Exception as err_msg:
            print("load data success")
            break
    headNode = getHeadNode(nodeList)
    msgTransPath = getMsgTransPath(headNode, nodeList)
    makeCtrlMsg(nodeList, msgTransPath)
    return 'success'   


def getHeadNode(nodeList):
    # 处理节点数据，获取数据链路
    headNode = {}
    for nodeData in nodeList:
        nodeDict =  json.loads(nodeData)
        if nodeDict["last"] == 'undefined':
            headNode = nodeDict
            return headNode
    return None

def findNodeById(nodeList, nodeId):
    # 通过字典查找对应id的node节点
    for nodeData in nodeList:
        nodeDict = json.loads(nodeData)
        if nodeDict['id'] == nodeId:
            return nodeDict

    return None


@app.route('/controller/clear')
def clear():
    nodePortList = getAllNodePort()
    for port in nodePortList:
        msg = "controller&clear"
        print(sendToController(port, msg))
    return 'success'

def getAllNodePort():
    # 获取全部节点端口号
    return [33333, 33334, 33335]
def findNextNodeById(nodeList, nodeId):
    # 通过字典查找对应id的node节点
    for nodeData in nodeList:
        nodeDict = json.loads(nodeData)
        if nodeDict['id'] == nodeId:
            return nodeDict['next']

    return None


def findThreholdById(nodeList, nodeid):
    # 通过节点id查找对应的阈值   
    for nodeData in nodeList:
        nodeDict = json.loads(nodeData)
        return nodeDict['threhold']
    return None
             
def getMsgTransPath(headNode, nodeList):
    # 通过头节点返回信息传输路径
    msgTransPath = []
    while True:
        if headNode['id'][:8] == "switcher":
            headNode = findNodeById(nodeList, headNode['next'])
            continue
        msgTransPath.append(headNode['id'])
        nextNode = headNode['next']
        if nextNode == 'undefined':
            break
        headNode = findNodeById(nodeList, nextNode)
    return msgTransPath
        

def makeCtrlMsg(nodeList, msgTransPath):
    # 通过消息传递数组生存控制指令，并配置到各个agent节点
    msgTransPathLen = len(msgTransPath)
    for i in range(msgTransPathLen - 1):
        nodeId = msgTransPath[i]
        nodePort = findNodePort(nodeId)
        print(nodePort)
        nextNodeId = msgTransPath[i + 1]
        threhold = findThreholdById(nodeList, nodeId)
        if threhold == 'undefined':
            continue
        else:
            (threhold, method) = threhold.split(';')
        nextNodePort = findNodePort(nextNodeId)
        ipAddr = '192.168.12.19:' + str(nextNodePort)
        ctrlMsg = "controller&add&" + threhold + ';' + ipAddr + ':' + method + '&20'
        print "send to %d" % nodePort
        print ctrlMsg
        print sendToController(nodePort, ctrlMsg) 

def findNodePort(nodeId):
    # 通过nodeid查找到虚拟化模块的端口号
    portDict = {'switch103': 33333, 'dht102': 33334, 'switch104': 33335}
    return portDict[nodeId]
    
def sendToController(port, msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.12.19", port))
    s.sendall(msg.encode())
    response = s.recv(1024).decode()
    return response
        


if __name__ == "__main__":
    app.run(threaded=True, debug=True, host='0.0.0.0', port=36666)

