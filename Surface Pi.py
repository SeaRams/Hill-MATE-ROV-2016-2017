#Surface Pi is the client

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '169.254.122.176' #eth0 "inet addr" of Sub Pi
port = 9000 #Arbitrary port above 5000 - must be same for sub Pi

sock.connect((host, port))

print "connected"
print(sock.recv(1024))
#sock.send("thank you for serving")
sock.close()
