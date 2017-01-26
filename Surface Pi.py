#Surface Pi is the client

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#host = "10.0.2.51"
host = '10.0.2.51'
port = 9000

sock.connect((host, port))
print "connected"
#print(s.recv(1024))
s.close()
