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

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/controller/hello/')
def hello():
    return 'hello'

@app.route('/controller/test/', methods=['POST'])
def test():
    nodeList = []
    for i in range(10):
        try:
            nodeData = request.form[str(i)]
            nodeList.append(nodeData)
        except Exception as err_msg:
            print("load data success")
            break
    headNode = getHeadNode(nodeList)
    msgTransPath = getMsgTransPath(headNode)
    return 'success'   


def getHeadNode(nodeList):
    # 处理节点数据，获取数据链路
    headNode = {}
    for nodeData in nodeList:
        nodeDict =  json.loads(nodeData)
        if nodeDict["last"] == 'undefined':
            headNode = nodeDict
            return headNode

def findNodeById(nodeList):
    # 通过字典查找对应id的node节点
    
def getMsgTransPath(headNode, nodeList):
    # 通过头节点返回信息传输路径
    msgTransPath = []
    msgTransPath.append(headNode['id'])
    nextNode = headNode['next']

def makeCtrlMsg(nodeList, msgTransPath):
    # 通过消息传递数组生存控制指令，并配置到各个agent节点
        


if __name__ == "__main__":
    app.run(threaded=True, debug=True, host='0.0.0.0', port=36666)



