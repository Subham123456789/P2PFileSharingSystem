# from Tkinter import *
# from ttk import *
import socket
from threading import Thread

IP = 'localhost'
PORT = 5555
server_soc = None


table = dict()
clients = set()
clients.add(('127.0.0.1', 5002))


def myreceive(client_sock):
    return client_sock.recv(2048).decode()


def mysend(client_sock, msg):
    client_sock.send(msg.encode())

def add_to_table(files_str, host, port):
    count = 0
    try:
        for file_str in files_str:
            data = file_str[1: -1]
            arr = data.split(',')
            name = arr[0]
            arr = arr[1:]
            value = ",".join(arr)
            if name in table:
                table[name].append((host, port, value))
            else:
                table[name] = [(host, port, value)]
            count += 1
        print(table)
    except:
        return False
    if count == 0:
        return False
    return True


def register_client(client_sock):
    host, port = client_sock.getpeername()
    clients.add((host, port))

def unregister(client_sock):
    host, port = client_sock.getpeername()
    clients.remove((host, port))


def handle_client_first_time(client_sock):
    greeting_message = "HI"
    greeting_message = greeting_message.encode()
    hello1 = client_sock.recv(2048)
    hello1 = hello1.decode()
    #hello = myreceive(client_sock)
    if hello1 != "HELLO":
        print("Got %s when should have gotten HELLO!" % hello1)
    else:
        print("it is %s " % hello1)
        client_sock.sendall(greeting_message)
        #mysend(client_sock, "HI")

    data = myreceive(client_sock)
    print(data)
    files_str = data.split(';')
    host, port = client_sock.getpeername()
    is_ok = add_to_table(files_str, host, port)
    if is_ok:
        register_client(client_sock)
    client_sock.close()


def listen_clients():
    while 1:
        client_sock, client_addr = server_soc.accept()
        client_host, client_port = client_sock.getpeername()
        print(client_sock)
        print(client_addr)
        if (client_host, client_port) in clients:
            Thread(target=handle_request, args= (client_sock, client_addr)).start()
        else:
            Thread(target=handle_client_first_time, args=(client_sock, )).start()


def init():
    global server_soc
    server_addr = (IP, PORT)
    server_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_soc.bind(server_addr)
    server_soc.listen(5)
    listen_clients()


def search(name):
    if name in table:
        ans = []
        sources = table[name]
        for source in sources:
            host, port, value = source
            if (host, port) in clients:
                ans.append(value)
        return ans
    return None


def handle_request(client_sock, client_addr):
    request = myreceive(client_sock)
    print(request)
    if request[:6] == "SEARCH":
        name = request[9:]
        sources = search(name)
        print(sources)
        if sources is not None:
            text = ";".join(sources)
            mysend(client_sock, "FOUND: <%s>" % text)
        else:
            mysend(client_sock, "NOT FOUND")

    if request == "BYE":
        unregister(client_sock)

    client_sock.close()



if __name__ == '__main__':
    init()
