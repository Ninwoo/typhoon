import socket
import sys

port = int(sys.argv[1])
message = sys.argv[2]

# message = "controller&clear&niubi"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", port))
s.sendall(message.encode())
response = s.recv(1024).decode()
print(response)
