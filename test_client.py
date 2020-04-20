# import socket
#
# sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sendSocket.bind(('127.0.0.1', 5002))
# sendSocket.connect(('127.0.0.1', 5555))
# sendSocket.send("HELLO")


arr = [['client', '.py', '20/04/2020', "4485"], ['FT_server', '.py', '20/04/2020', "3175"], ['test_client', '.py', '20/04/2020', "195"], ['server_hw2', '.py', '20/04/2020', "870"]]

print(';'.join(["<" + ','.join(x) + ">" for x in arr]))

