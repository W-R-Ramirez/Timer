from os import listdir
from timerClass import *
from typing import List
# import tkinter
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

class Splash:
    def __init__(self, master) -> None:
        self.master = master
        self.chooseRun = tk.Button(master, text="Select Splits",bg="#ADD8E6", command=self.selectRun)
        self.makeNew = tk.Button(master, text="Create New Splits", bg="#ADD8E6", command=self.newRun)
        self.chooseRun.grid()
        self.makeNew.grid()

    def selectRun(self):
        self.chooseRun.grid_forget()
        self.makeNew.grid_forget()
        runs = self.getRuns()
        for i in range(len(runs)):
            self.run = tk.Button(self.master, text=runs[i], bg="#ADD8E6", command=lambda i=i: self.startRun(runs[i]))
            self.run.grid()
    def getRuns(self):
        return listdir("splits")
    def newRun(self):
        pass
    def startRun(self, run):
        for widget in self.master.winfo_children():
            widget.destroy()
        
        timer = Timer(run, self.master)
        self.master.bind('<Return>', timer.enter)

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#ADD8E6", width=100)
    timer = Splash(root)
    root.mainloop()
