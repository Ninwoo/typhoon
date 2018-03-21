import socket
import sys

message = sys.argv[1]

# message = "controller&clear&niubi"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 3000))
s.sendall(message.encode())
response = s.recv(1024).decode()
print(response)
