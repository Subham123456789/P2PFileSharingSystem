from Tkinter import *
import thread
import socket

import platform
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
        self.FTPORT = '5555'
        self.listenSocket = None
        self.sendSocket = None
        self.initSockets()


    def generatePORT(self):
        return randint(5000, 9000)

    def initSockets(self):
        listen_port = self.generatePORT()
        send_port = self.generatePORT()
        listen_addr = (self.IP, listen_port)
        send_addr = (self.IP, send_port)
        self.listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listenSocket.bind(listen_addr)
        self.sendSocket.bind(send_addr)
        self.listenSocket.listen(5)
        self.listen_clients()


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

        search_frame = Frame(self.root)

        search_label = Label(search_frame, text="File name: ")
        self.search_var = StringVar()
        self.search_var.set("Enter the file name")
        search_field = Entry(search_frame, width=20, textvariable=self.search_var)
        search_button = Button(search_frame, text="Search", width=10, command=self.search)

        search_frame.grid(padx=5, pady=15, sticky=E + W + N + S)
        search_label.grid(row=0, column=0)
        search_field.grid(row=0, column=1)
        search_button.grid(row=0, column=2)
        search_frame.pack()

    def search(self):
        # thread.start_new_thread(self.printing, ())
        self.sendSocket.connect((self.FTIP, self.FTPORT))

        name = self.search_var.get()

        request = "SEARCH: " + name

        self.sendmsg(self.sendSocket, request)


    def sendmsg(self, sock, msg):
        totalsent = 0
        while totalsent < len(msg):
            sent = sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def printing(self):
        print("ffffff")

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