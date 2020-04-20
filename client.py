from tkinter import *
import thread
import socket
import platform

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555
client_soc = None

class App(Frame):

    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root        
        self.initUI()

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

        search_frame.grid(padx=130, pady=100, sticky=E + W + N + S)
        connect_button.grid(row=0, column=2)
        search_label.grid(row=1, column=1)
        search_field.grid(row=1, column=2)
        search_button.grid(row=1, column=3)

    def mysend(self, sock, msg):
        totalsent = 0
        while(totalsent < len(msg)):
            sent = sock.send(msg[totalsent:])
            if sent==0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def search(self):
        thread.start_new_thread(self.printing, ())

    def printing(self):
        print("ffffff")

    def connect(self):
        global client_soc
        client_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Connecting to Server ")
        client_soc.connect(('localhost', 5555))
        greeting_message = "HELLO"
        self.mysend(client_soc, greeting_message)
        #client_soc.close()
        
def main():
    root = Tk()
    app = App(root)
    root.mainloop()
    print(platform.python_version())

    # root.destroy()


if __name__ == '__main__':
    main()