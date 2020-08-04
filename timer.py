# import tkinter
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import time

def convertTimeToSecs(timeStr):
    colon = timeStr.find(":")
    mins = int(timeStr[:colon])
    secs = float(timeStr[colon+1:]) + 60*mins
    return secs


def convertSecsToTime(secStr):
    secs = float(secStr)
    mins = secs//60
    secs = secs % 60
    if secs >= 10:
        timeStr = str(int(mins))+":"+str(round(secs,3))
    else:
        timeStr = str(int(mins))+":0"+str(round(secs,3))

        
    return timeStr



                
class Window:
    def __init__(self, master):
        self.time = 0
        self.splits_completed = 0
        self.final = False
        self.started = False
        self.time_label = tk.Label(master, font="Arial 30", width=25, text="Start")
        self.time_label.pack()
        self.splits =  ["Cap", "Caskade", "Sand", "Lake", "Wood", "Cloud", "Lost", "Night Metro", "Day Metro"]
        self.total_splits = len(self.splits)
        #Times for current run
        self.splitResults = []
        #Times in overall PB
        self.PBSplits = []
        #Best ever record for each split
        self.splitRecords = []




    def refresh_time(self):
        cur = time.monotonic()

        total = cur-self.first
        
        self.time_label.configure(text= "Total: " + convertSecsToTime(total))
        if not self.final:
            self.time_label.after(50, self.refresh_time)
        

    def func(self, event):
        if self.started:
            cur = time.monotonic()
            splitTime = cur-self.prev

            self.prev = cur
            total = cur - self.first
            kingdom = self.splits[len(self.splitResults)]
            self.splitResults.append(splitTime)
            print(kingdom + " Split: " + convertSecsToTime(str(splitTime)))
            print("Total: " + convertSecsToTime(total))
            if len(self.splitResults) == self.total_splits:
                splitResults = [convertSecsToTime(split) for split in self.splitResults]
                splitResults.insert(0,convertSecsToTime(total))
                print(splitResults)
                self.final = True
                with open("raw_results.txt", "a+") as f:
                    f.write(str(splitResults)+"\n")

        else:
            self.started = True
            self.prev = time.monotonic()
            self.first = self.prev
            self.time_label.after(500, self.refresh_time)
                
            

        
if __name__ == "__main__":

    
    root = tk.Tk()
    
    splits = ["Cap", "Caskade", "Sand", "Lake", "Wood", "Cloud", "Lost", "Night Metro", "Day Metro"]


    timer = Window(root)
    root.bind('<Return>', timer.func)
    root.mainloop()

    
