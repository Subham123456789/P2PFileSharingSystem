from tkinter import *
import thread
import socket
import platform
import os
import time
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
        self.MYPORT = self.generatePORT()
        self.LISTENPORT = self.generatePORT()
        self.listenSocket = self.initSocket(1)
        self.sendSocket = self.initSocket(0)
        thread.start_new_thread(self.listenClients, ())


    def generatePORT(self):
        return randint(5000, 9000)

    def initSocket(self, t):
        port = self.LISTENPORT
        if t == 0:
            port = self.MYPORT
        addr = (self.IP, port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(addr)
            print("BINDED")
        except:
            if t == 0:
                self.MYPORT = self.generatePORT()
                self.sendSocket = self.initSocket(0)
            else:
                self.LISTENPORT = self.generatePORT()
                self.listenSocket = self.initSocket(1)

        if t == 0:
            sock.connect((self.FTIP, self.FTPORT))
        else:
            sock.listen(5)
        return sock

    def listenClients(self):
        while 1:
            client_sock, client_addr = self.listenSocket.accept()
            thread.start_new_thread(self.handleRequest, (client_sock, ))

    def handleRequest(self, client_sock):
        stream = self.myreceive(client_sock)
        if stream[:8] == "DOWNLOAD":
            info = stream[10:].split(',')
            name = info[0]
            type = info[1]
            size = info[2]
            full_name = name+type
            f = open(full_name, 'rb')
            text = f.read()
            protocol = "FILE: "
            client_sock.sendall(protocol.encode() + text)
            f.close()


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
        self.parentFrame = Frame(self.root)
        self.parentFrame.grid(padx=padX, pady=padY, sticky=E+W+N+S)

        self.search_frame = Frame(self.parentFrame)
        self.search_label = Label(self.search_frame, text="File name: ")
        self.search_var = StringVar()
        self.search_var.set("Enter the file name")
        self.search_field = Entry(self.search_frame, width=20, textvariable=self.search_var)
        self.search_button = Button(self.search_frame, text="Search", width=10, command=self.send_search)
        self.connect_button = Button(self.search_frame, text = "Connect", width=10, command=self.send_connect)
        self.list_of_clients = Label(self.parentFrame, text="")
        self.search_frame.grid(padx=110, pady=100, sticky=E + W + N + S)
        self.connect_button.grid(row=0, column=2)
        self.search_label.grid(row=1, column=1)
        self.search_field.grid(row=1, column=2)
        self.search_button.grid(row=1, column=3)

        self.records_list = Listbox(self.search_frame)
        self.records_list.grid(row=2, column=2)
        self.records_list.config(width=32, height=15)

        self.download_button = Button(self.search_frame, text = "Download", width=10, command=self.choose_item)
        self.download_button.grid(row=3, column=2)

    def myreceive(self, client_sock):
        return client_sock.recv(2048).decode()

    def mysend(self, client_sock, msg):
        client_sock.sendall(msg.encode())

    def send_search(self):
        thread.start_new_thread(self.search, ())

    def send_connect(self):
        thread.start_new_thread(self.connect, ())

    def search(self):

        # self.sendSocket = self.initSocket(self.sendSocket)
        # self.sendSocket.connect((self.FTIP, self.FTPORT))
        name = self.search_var.get()

        print(name)

        request = "SEARCH: " + name
        self.mysend(self.sendSocket, request)
        message = self.myreceive(self.sendSocket)

        print(message)
        message = message[7:][1:-1]
        message = message.split(';')
        print(message)

        for el in message:
            self.records_list.insert(END, el)

        # self.list_of_clients.set(message)
        # self.sendSocket.close()

    def connect(self):
        # self.sendSocket = self.initSocket(self.sendSocket)
        # self.sendSocket.connect((self.FTIP, self.FTPORT))

        print("Connecting to Server ")
        greeting_message = "HELLO"
        self.mysend(self.sendSocket, greeting_message)
        reply = self.myreceive(self.sendSocket)
        print(reply)
        path = os.getcwd()
        print(path)
        f_list = os.listdir('.')
        print(f_list)
        list_of_files = [[os.path.splitext(f)[0],self.IP, str(self.LISTENPORT), os.path.splitext(f)[1], time.strftime('%d/%m/%Y', time.localtime(os.path.getmtime(f))), str(os.path.getsize(f))] for f in f_list if os.path.isfile(f)]
        print(list_of_files)
        stream = ';'.join(["<" + ','.join(x) + ">" for x in list_of_files])
        self.mysend(self.sendSocket, stream)

        # self.sendSocket.close()
        # print("CLOSED")


    def download(self, client_host, client_port, info): # depends how Kama will pass info from list
        port = self.generatePORT()
        downloadSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while 1:
            try:
                addr = (self.IP, port)
                downloadSocket.bind(addr)
                print ("BINDED")
                break
            except:
                port = self.generatePORT()
                pass

        downloadSocket.connect((client_host, client_port))
        mess = "DOWNLOAD: " + info
        self.mysend(downloadSocket, mess)

        answer = downloadSocket.recv(4096)

        if answer[:4].decode() == "FILE":
            file = answer[6:]
            name = info.split(',')[0] + info.split(',')[1]
            f = open(name, 'wb')
            f.write(file)
            f.close()
        print ("ERROR OCCURED")

    def choose_item(self):
        choosen_value = []
        choosen_item = self.records_list.get(ACTIVE)
        print(choosen_item)
        choosen_arr = choosen_item.split(',')
        choosen_filename = choosen_arr[0]
        choosen_host = choosen_arr[1]
        choosen_port = int(choosen_arr[2])
        choosen_ext = choosen_arr[3]
        choosen_size = choosen_arr[5]
        choosen_value.append(choosen_filename)
        choosen_value.append(choosen_ext)
        choosen_value.append(choosen_size)
        sending_value = ",".join(choosen_value)
        print(choosen_host)
        print(choosen_port)
        print(sending_value)
        self.download(choosen_host, choosen_port, sending_value)
    

def main():
    root = Tk()
    app = App(root)
    # print(app.generatePORT())
    root.mainloop()
    # print(platform.python_version())

    # root.destroy()


if __name__ == '__main__':
    main()