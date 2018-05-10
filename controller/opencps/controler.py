import socket
import sys
import numpy as np
import json

def execute(port, message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.12.19", port))
    s.sendall(message.encode())
    response = s.recv(1024).decode()
    return json.loads(response)

def Print(data):
    print(format(data, "<20"), end='')

def PrintTitle(title):
    for t in title:
        Print(t)
    print('')



