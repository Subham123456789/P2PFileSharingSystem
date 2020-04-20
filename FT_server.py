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
            data = file_str[1:-1]
            arr = data.split(',')
            name = arr[0]
            arr = arr[1:]
            value = ",".join(arr)
            if name in table:
                table[name].append((host, port, value))
            else:
                table[name] = [(host, port, value)]
            count += 1
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
    client_sock.close()


def handle_client_first_time(client_sock):
    pass
    # greeting_message = greeting_message.encode()
    # hello1 = client_sock.recv(2048)
    # hello1 = hello1.decode()
    # #hello = myreceive(client_sock)



def listen_clients():
    while 1:
        client_sock, client_addr = server_soc.accept()
        print(client_sock)
        print(client_addr)
        Thread(target=handle, args=(client_sock, client_addr)).start()




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
    print(table)
    print("NOT IN TABLE")
    return None


def handle(client_sock, client_addr):
    chunk = myreceive(client_sock)
    while chunk:
        handle_request(chunk, client_sock)
        try:
            chunk = myreceive(client_sock)
        except:
            chunk = None
    client_sock.close()

def handle_request(request, client_sock):
    client_host, client_port = client_sock.getpeername()
    greeting_message = "HI"
    print(request)
    if request == "HELLO":
        print("it is %s " % request)
        mysend(client_sock, greeting_message)

        data = myreceive(client_sock)
        print(data)
        files_str = data.split(';')
        host, port = client_sock.getpeername()
        is_ok = add_to_table(files_str, host, port)
        if is_ok:
            register_client(client_sock)
        return

    if request[:6] == "SEARCH":
        if (client_host, client_port) not in clients:
            mysend(client_sock, "UNREGISTERED")
        else:
            name = request[8:]
            sources = search(name)
            print(sources)
            if sources is not None:
                text = ";".join(sources)
                mysend(client_sock, "FOUND: <%s>" % text)
            else:
                mysend(client_sock, "NOT FOUND")
        return

    if request == "BYE":
        unregister(client_sock)



if __name__ == '__main__':
    init()
