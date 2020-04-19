# from Tkinter import *
# from ttk import *
import socket
from threading import Thread

IP = "127.0.0.1"
PORT = 5555
server_soc = None


table = dict()
clients = set()


def myreceive(client_sock):
    chunks = []
    while 1:
        chunk = client_sock.recv(2048)
        chunks.append(chunk)
        if len(chunk) == 0:
            break
    return ''.join(chunks)


def mysend(client_sock, msg):
    totalsent = 0
    while totalsent < len(msg):
        sent = client_sock.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent


def add_to_table(files_str, host, port):
    count = 0
    try:
        for file_str in files_str:
            data = file_str[1, -1]
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


def handle_client_first_time(client_sock):
    hello = myreceive(client_sock)
    if hello != "HELLO":
        print("Got %s when should have gotten HELLO!" % hello)
    else:
        mysend(client_sock, "HI")

    data = myreceive(client_sock)
    files_str = data.split(';')
    host, port = client_sock.getpeername()
    is_ok = add_to_table(files_str, host, port)
    if is_ok:
        register_client(client_sock)
    client_sock.close()


def listen_clients():
    print("1")
    while 1:
        client_sock, client_addr = server_soc.accept()
        client_host, client_port = client_sock.getpeername()
        if (client_host, client_port) in clients:
            Thread(target=handle_request, args= (client_sock, client_addr))
        else:
            Thread(target=handle_client_first_time(), args=client_sock).start()


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
    if request[:7] == "SEARCH":
        name = request[9:]
        sources = search(name)
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
