import socket
import sys
import numpy as np
import json

def execute(port, message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.12.19", port))
    s.sendall(message.encode())
    response = s.recv(1024).decode()
    print(response)



