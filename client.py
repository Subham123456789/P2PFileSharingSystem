from Tkinter import *
import thread
import socket
import platform
import os
import time


SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555
client_soc = None
from random import seed
from random import randint

class App(Frame):

    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.initUI()
        self.socket = None
        self.IP = '127.0.0.1'
        self.FTIP = '127.0.0.1'
        self.FTPORT = 5555
        self.listenSocket = None
        self.sendSocket = None
        self.listenSocket = self.initSocket(self.listenSocket)
        self.listenSocket.listen(5)
        thread.start_new_thread(self.listenClients, ())


    def generatePORT(self):
        return randint(5000, 9000)

    def initSocket(self, sock):
        port = self.generatePORT()
        addr = (self.IP, port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(addr)
        return sock

    def listenClients(self):
        while 1:
            client_sock, client_addr = self.listenSocket.accept()
            thread.start_new_thread(self.handleRequest, client_sock)

    def listenSockets(self):
        while 1:
            client_sock, client_addr = self.listenSocket.accept()
            thread.start_new_thread(self.handleRequest, client_sock)

    def handleRequest(self, client_sock):
        pass

    def initUI(self):
        self.root.title("P2P File Sharing System")
        ScreenSizeX = self.root.winfo_screenwidth()
        ScreenSizeY = self.root.winfo_screenheight()
        print(ScreenSizeX)
        print(ScreenSizeY)
        self.FrameSizeX = 600
        self.FrameSizeY = 600
        FramePosX = (ScreenSizeX - self.FrameSizeX) / 2
        FramePosY = (ScreenSizeY - self.FrameSizeY) / 2
        self.root.geometry("%sx%s+%s+%s" % (self.FrameSizeX, self.FrameSizeY, FramePosX, FramePosY))
        self.root.resizable(width=False, height=False)

        padX = 10
        padY = 10
        parentFrame = Frame(self.root)
        parentFrame.grid(padx=padX, pady=padY, sticky=E+W+N+S)

        search_frame = Frame(parentFrame)
        search_label = Label(search_frame, text="File name: ")
        self.search_var = StringVar()
        self.search_var.set("Enter the file name")
        search_field = Entry(search_frame, width=20, textvariable=self.search_var)
        search_button = Button(search_frame, text="Search", width=10, command=self.search)
        connect_button = Button(search_frame, text = "Connect", width=10, command=self.connect)
        self.list_of_clients = Label(parentFrame, text="")
        search_frame.grid(padx=130, pady=100, sticky=E + W + N + S)
        connect_button.grid(row=0, column=2)
        search_label.grid(row=1, column=1)
        search_field.grid(row=1, column=2)
        search_button.grid(row=1, column=3)

    def myreceive(self, client_sock):
        return client_sock.recv(2048).decode()

    def mysend(self, client_sock, msg):
        client_sock.sendall(msg.encode())

    def search(self):
        thread.start_new_thread(self.send_search, ())

    def send_search(self):

        # self.sendSocket = self.initSocket(self.sendSocket)
        port = 5002
        addr = (self.IP, port)
        self.sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sendSocket.bind(addr)
        self.sendSocket.connect((self.FTIP, self.FTPORT))

        name = self.search_var.get()

        request = "SEARCH: " + name
        self.mysend(self.sendSocket, request)
        message = self.myreceive(self.sendSocket)
        print(message)
        self.list_of_clients.set(message)
        self.sendSocket.close()

    def connect(self):
        self.sendSocket.connect(('localhost', 5555))
        print("Connecting to Server ")
        greeting_message = "HELLO"
        self.mysend(self.sendSocket, greeting_message)
        reply = self.myreceive(self.sendSocket)
        print(reply)
        path = os.getcwd()
        print(path)
        f_list = os.listdir('.')
        print(f_list)
        list_of_files = [[os.path.splitext(f)[0], os.path.splitext(f)[1], time.strftime('%d/%m/%Y', time.localtime(os.path.getmtime(f))), str(os.path.getsize(f))] for f in f_list if os.path.isfile(f)]
        print(list_of_files)
        stream = ';'.join(["<" + ','.join(x) + ">" for x in list_of_files])
        self.mysend(self.sendSocket, stream)


    def download(self, client_addr, client_port):
        self.sendSocket.connect((client_addr, client_port))
        pass

def main():
    root = Tk()
    app = App(root)
    # print(app.generatePORT())
    root.mainloop()
    # print(platform.python_version())

    # root.destroy()


if __name__ == '__main__':
    main()