# import tkinter
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import time

def convertSecsToTime(secStr):
    secs = float(secStr)
    mins = secs//60
    secs = secs % 60
    if secs >= 10:
        timeStr = str(int(mins))+":"+str(round(secs,3))
    else:
        timeStr = str(int(mins))+":0"+str(round(secs,3))

        
    return timeStr

class Timer:
    def __init__(self, master):
        
        ##################
        ## GUI Elements ##
        ##################

        self.start_run_button = tk.Button(master, text="Start Run", command=self.start, bg="#ADD8E6")
        self.start_run_button.pack()
        
        

class Run:
    def __init__(self, name, pb_time, sob):
        self.name = name
        self.pb_time = pb_time
        self.sob = sob
        
class Segment:
    def __init__(self, name, gold, pb_time, position):
       self.name = name
       self.gold = gold
       self.sub_segments = []
       self.time = 0
       self.pb_time = pb_time
       self.final = False
       self.position = position

        ##################
        ## GUI Elements ##
        ##################

        self.split_label = tk.Label(master, font="Arial 20", width=15, text=self.name, bg="#ADD8E6")
        self.split_time_label = tk.Label(master, font="Arial 20", width=15, text=convertSecsToTime(calculate_time(self.PBSplits, 1, self.position, True)), bg="#ADD8E6")

    def referesh_time(self, first, prev):
        if not self.final:
            cur = time.monotonic()
            total = cur-first
            split = cur-prev
            



if __name__ == "__main__":

    
    root = tk.Tk()

    root.configure(bg="#ADD8E6")
    timer = Timer(root)
    root.bind('<Return>', timer.enter)
    root.mainloop()
