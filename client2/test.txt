import socket
#
# sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sendSocket.bind(('127.0.0.1', 5002))
# sendSocket.connect(('127.0.0.1', 5555))
# sendSocket.send("HELLO")


# arr = [['client', '.py', '20/04/2020', "4485"], ['FT_server', '.py', '20/04/2020', "3175"], ['test_client', '.py', '20/04/2020', "195"], ['server_hw2', '.py', '20/04/2020', "870"]]
#
# print(';'.join(["<" + ','.join(x) + ">" for x in arr]))

def myreceive(client_sock):
    return client_sock.recv(2048).decode()


def mysend(client_sock, msg):
    client_sock.send(msg.encode())


port = 5991
downloadSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = ('127.0.0.1', port)
downloadSocket.bind(addr)
print "BINDED"
downloadSocket.connect(('127.0.0.1', 6666))
mess = "DOWNLOAD: " + "test,.txt,3289"
mysend(downloadSocket, mess)

answer = downloadSocket.recv(4096)

if answer[:4].decode() == "FILE":
    file = answer[6:]
    name = "test.txt"
    f = open(name, 'wb')
    f.write(file)
    f.close()
print "ERROR OCCURED"