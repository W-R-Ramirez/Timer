# import tkinter
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import time

def convertTimeToSecs(timeStr):
    colon = timeStr.find(":")
    mins = int(timeStr[:colon].replace("'", ""))
    secs = float(timeStr[colon+1:].replace("'", "")) + 60*mins
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

def calculate_time(splits, start, finish):
    return sum([convertTimeToSecs(times) for times in splits[start: finish+1]])

                
class Timer:
    def __init__(self, master):
        self.time = 0
        self.splits_completed = 0
        self.final = False
        self.started = False

        self.splits =  ["Cap", "Caskade", "Sand", "Lake", "Wood", "Cloud", "Lost", "Night Metro", "Day Metro", "Snow", "Beach", "Luncheon", "Ruined", "Bunnies", "Bowsers", "Moon"]
        self.total_splits = len(self.splits)
        #Times for current run
        self.splitResults = []

        
        self.pb = 9999999999999999999
        #Best ever record for each split
        self.sumOfBest = [self.pb]*(len(self.splits)+1)
        #Times in overall PB
        self.PBSplits = [self.pb]*len(self.splits)
        with open("results.txt", "r+") as f:
            for splits in f:
                splits = splits[1:-2].split(",")
                time = convertTimeToSecs(splits[0])
                if time < self.pb:
                    self.pb = time
                    self.PBSplits = [split.replace("'","") for split in splits]
                for i in range(len(self.splits)+1):
                    time = convertTimeToSecs(splits[i])
                    if time < self.sumOfBest[i]:
                        self.sumOfBest[i] = time

        

        print(self.pb)
        print(self.PBSplits)
        self.sumOfBest[0] = 0
        sumOfBest = sum(self.sumOfBest)
        self.sumOfBest[0] = sumOfBest
        self.sumOfBest = [convertSecsToTime(split) for split in self.sumOfBest]
        print(self.sumOfBest)
        
        ##################
        ## GUI Elements ##
        ##################
        
        self.split_time_label = tk.Label(master, font="Arial 20", width=15)
        self.total_time_label = tk.Label(master, font="Arial 30", text="Start", width=15)
        self.cur_split_pb_time = tk.Label(master, font="Arial 15", text="PB: ")
        self.cur_split_gold_time = tk.Label(master, font="Arial 15", text="Gold: ")
        self.undo_button = tk.Button(master, text="Undo", command=self.undo)
        
        self.prev_split_label = tk.Label(master, font="Arial 20", width=15, text=self.splits[0])
        self.prev_split_time_label = tk.Label(master, font="Arial 20", width=15, text=self.PBSplits[1])
        self.prev_split_diff = tk.Label(master, font="Arial 15", width=20)
        
        self.cur_split_label = tk.Label(master, font="Arial 20", width=15, text=self.splits[1])
        self.cur_split_time_label = tk.Label(master, font="Arial 20", width=15, text=convertSecsToTime(calculate_time(self.PBSplits, 1, 2)))
        self.cur_split_diff = tk.Label(master, font="Arial 15", width=20)
        
        self.final_split_label = tk.Label(master, font="Arial 20", width=15, text="Done")
        self.split_pb = tk.Label(master, font="Arial 20", width=15, text="Split PB: ")
        self.total_pb = tk.Label(master, font= "Arial 20", width=15, text=self.PBSplits[0])
        
        self.prev_split_label.grid(row=0, column=0)
        self.prev_split_time_label.grid(row=1, column=0)
        self.cur_split_label.grid(row=0, column=1)
        self.cur_split_time_label.grid(row=1, column=1)
        self.final_split_label.grid(row=0, column=2)
        self.split_time_label.grid(row=1,column=4)
        self.total_time_label.grid(row=0,column=4)
        self.total_pb.grid(row=1, column=2)
        self.cur_split_pb_time.grid(row=2, column=3)
        self.cur_split_gold_time.grid(row=1, column=3)
        self.undo_button.grid(column=1)
    def refresh_time(self):
        if not self.final:
            cur = time.monotonic()

            total = cur-self.first
            split = cur-self.prev
            kingdom = self.splits[len(self.splitResults)]
            self.split_time_label.configure(text=kingdom+": " + convertSecsToTime(split))
            self.total_time_label.configure(text= "Total: " + convertSecsToTime(total))
            self.total_time_label.after(75, self.refresh_time)
        

    def enter(self, event):
        if self.started:
            cur = time.monotonic()
            splitTime = cur-self.prev

            self.prev = cur
            total = cur - self.first
            kingdom = self.splits[len(self.splitResults)]
            self.splitResults.append(splitTime)
            if len(self.splitResults) > 1:
                diff = total - calculate_time(self.PBSplits, 1, len(self.splitResults))
                if diff < 0:
                    final_diff = "-"+convertSecsToTime(-diff)
                else:
                    final_diff = "+"+convertSecsToTime(diff)

                self.prev_split_label.configure(text=self.cur_split_label.cget("text"))
                if len(self.splitResults) < self.total_splits:
                    self.cur_split_label.configure(text=self.splits[len(self.splitResults)])
                if len(self.splitResults) == self.total_splits:
                    splitResults = [convertSecsToTime(split) for split in self.splitResults]
                    splitResults.insert(0,convertSecsToTime(total))
                    print(splitResults)
                    self.final = True
                    with open("raw_results.txt", "a+") as f:
                        f.write(str(splitResults)+"\n")
                    with open("results.txt", "a+") as f:
                        f.write(str(splitResults)+"\n")
                else:
                    self.cur_split_time_label.configure(text=convertSecsToTime(calculate_time(self.PBSplits, 1, len(self.splitResults)+1)))
            else:
                print(total)
                print(calculate_time(self.PBSplits, 1, 1))
                diff = total - calculate_time(self.PBSplits, 1, 1)
                final_diff = 0
                if diff < 0:
                    final_diff = "-"+convertSecsToTime(-diff)
                else:
                    final_diff = convertSecsToTime(diff)

                print(final_diff)
            
            self.prev_split_time_label.configure(text=convertSecsToTime(str(total)))
            self.prev_split_diff.configure(text=final_diff)
            self.prev_split_diff.grid(row=2, column=0)

            print(kingdom + " Split: " + convertSecsToTime(str(splitTime)))
            print("Total: " + convertSecsToTime(total))


        else:
            self.started = True
            self.prev = time.monotonic()
            self.first = self.prev
            self.total_time_label.after(50, self.refresh_time)

        
        self.cur_split_gold_time.configure(text="Gold: " + self.sumOfBest[len(self.splitResults)+1])
        self.cur_split_pb_time.configure(text="PB: " + self.PBSplits[len(self.splitResults)+1])


    def undo(self):
        self.splitResults.pop()
        self.prev = self.first + sum(self.splitResults)

                
            

        
if __name__ == "__main__":

    
    root = tk.Tk()


    timer = Timer(root)
    root.bind('<Return>', timer.enter)
    root.mainloop()

    
