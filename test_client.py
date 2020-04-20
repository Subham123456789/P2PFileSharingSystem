import thread
import socket

sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sendSocket.connect(('127.0.0.1', 5555))
sendSocket.send("HELLO")

while 1:


