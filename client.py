from tkinter import *
import thread

import platform


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
        thread.start_new_thread(self.printing, ())

    def printing(self):
        print("ffffff")


def main():
    root = Tk()
    app = App(root)
    root.mainloop()
    print(platform.python_version())

    # root.destroy()


if __name__ == '__main__':
    main()