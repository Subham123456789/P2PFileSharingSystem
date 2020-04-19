import socket
import os


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(('0.0.0.0', 9999))
server.listen(5)

# make request localhost:9999/filename to get file
# Was made by Adilya Yerzhanova and Saddam Asmatullayev

while True:
    conn, address = server.accept()
    data = conn.recv(1024).decode()
    if not data:
        print("hello")
        continue
    filename = data.split('\n')[0].split(' ')[1].split('/')[1]
    path = os.path.join(os.getcwd(), filename)
    if os.path.exists(path) and os.path.isfile(path):
            # file = open(path).read()
            f = open(filename, 'rb')
            conn.send(b'HTTP/1.0 200 OK\r\n\r\n')
            text = f.read()
            conn.send(text)
            f.close()
    else:
        conn.send(b'HTTP/1.0 404 Not Found\r\n\r\n')
        print(path)
    conn.close()

server.close()


