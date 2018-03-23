'''
***********************************************
*      智能体控制器函数                       *
*    功能描述：                               *
*    1. 接收应用层的控制指令                  *
*    2. 向智能体传递控制指令                  *
*    3. 执行突发事件请求                      *
*    4. 接收智能体未标识控制指令（暂未开发）  *
*                                             *        
*            author: joliu<joliu@s-an.org>    *
*            date: 2018-3-23                  *
***********************************************
'''

# 通过socket传递信息
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
    except socket.error as err_msg:
        print("Error receiving data: %s" % err_msg)
        s.close()
        return (-1, err_msg)
    try:
        response = s.recv(1024).decode()
    except socket.error as err_msg:
        print("Error receiving data: %s" % err_msg)
        s.close()
        return (-1, err_msg)

    print(str(response))
    s.close()

    return (1, str(response))


# socket实现版本，也可以基于RESTful API实现
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    '''
    监听控制请求
    '''
    def handle(self):
        try:
            # 接受socket消息
            data = self.request.recv(1024).decode()
        except socket.error as err_msg:
            (status, output) = (-1, err_msg)
             print("recv error!")
             exit(1)

        # 根据传递的消息进行操作 
        (status, output) = chooseTask(data)

        # 返回控制结果
        jresp = json.dumps((status, str(output)))
        try:
            self.request.sendall(jresp.encode())
        except socket.error as err_msg:
            print("socket send failed:%s" % err_msg)
            exit(1)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
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

