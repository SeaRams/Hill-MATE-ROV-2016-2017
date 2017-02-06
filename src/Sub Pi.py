#Sub Pi is the server
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '0.0.0.0'

port = 9000
sock.bind((host, port))
sock.listen(5)
print "server is ready"

c, addr = sock.accept()
print('Got connection from', addr)
c.send('thank you for connecting')
print(c.recv(1024)) #ensures that the client "closes" first, or the server port will be stuck on TIME_WAIT
c.close()
