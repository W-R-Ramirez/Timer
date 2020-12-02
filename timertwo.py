# import tkinter
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import time

def convertSecsToTime(secStr):
    secs = float(secStr)
    mins = secs//60
    hours = mins//60
    mins = mins - hours*60
    secs = secs % 60
    if hours ==  0:
        if secs >= 10:
            timeStr = str(int(mins)) + ":" + str(round(secs,3))
        else:
            timeStr = str(int(mins)) + ":0" + str(round(secs,3))
    else:
        if secs >= 10 and mins >= 10:
            timeStr = str(int(hours)) + ":" + str(int(mins)) + ":" + str(round(secs,3))
        elif secs >= 10:
            timeStr = str(int(hours)) + ":0" + str(int(mins)) + ":" + str(round(secs,3))
        else:
            timeStr =  str(int(hours)) + ":0" + str(int(mins)) + ":0" + str(round(secs,3))

        
    return timeStr

def calculate_total_time(splits, start, finish):
    return sum(splits[start:finish+1])

class Timer:
    def __init__(self, master):
        self.time = 0
        self.started = False
        self.final = False
        self.finished = False

        self.cur_run = Run("raw_results.txt", "SMO Any%")

        #Times for current run
        self.splitResults = []
        

        ##################
        ## GUI Elements ##
        ##################
        self.split_elements = {}
        self.split_info = {}
        if self.cur_run.total_splits > 18:
            pass
        else:
            for i in range(self.cur_run.total_splits):
                self.split_info[i] = [self.cur_run.splits[i], convertSecsToTime(calculate_total_time(self.cur_run.PBSplits, 1, i+1))]
                
                self.split_elements[i*3] = tk.Label(master, font="Arial 20", text=self.cur_run.splits[i], bg="#ADD8E6", width=10)
                self.split_elements[i*3].grid(row=i, column=0, sticky=tk.W)
                self.split_elements[i*3+1] = tk.Label(master, font="Arial 15", text="", bg="#ADD8E6", width=10)
                self.split_elements[i*3+1].grid(row=i, column=1)
                self.split_elements[i*3+2] = tk.Label(master, font="Arial 20", text=convertSecsToTime(calculate_total_time(self.cur_run.PBSplits, 1, i+1)),bg="#ADD8E6", width=10)
                self.split_elements[i*3+2].grid(row=i, column=2, sticky=tk.E)

        

        self.total_time_label = tk.Label(master, font="Arial 30", text="Start", width=10,bg="#ADD8E6")
        self.total_time_label.grid(row=self.cur_run.total_splits+1, column=2, sticky=tk.E)

        sumOfBest = convertSecsToTime(self.cur_run.sumOfBest[0])
        self.sum_of_best = tk.Label(master, font="Arial 15", bg="#ADD8E6", text="Sum of Best:")
        self.sum_of_best_time = tk.Label(master, font="Arial 15", bg="#ADD8E6", text=sumOfBest)
        self.best_possible = tk.Label(master, font= "Arial 15", bg="#ADD8E6", text="Best Possible Time:")
        self.best_possible_time = tk.Label(master, font="Arial 15", bg="#ADD8E6", text=sumOfBest)
        self.sum_of_best.grid(row=self.cur_run.total_splits+2, column=1, sticky=tk.E)
        self.sum_of_best_time.grid(row=self.cur_run.total_splits+2, column=2)
        self.best_possible.grid(row=self.cur_run.total_splits+3, column=1, sticky=tk.E)
        self.best_possible_time.grid(row=self.cur_run.total_splits+3, column=2)


        self.cur_seg = tk.Label(master, font="Arial 15", text="Current Segment:", bg="#ADD8E6")
        self.cur_seg_time = tk.Label(master, font="Arial 15", bg="#ADD8E6")
        self.prev_seg = tk.Label(master, font="Arial 15", text="Prev Segment", bg="#ADD8E6")
        self.prev_seg_time = tk.Label(master, font="Arial 15", bg="#ADD8E6")
        self.pb = tk.Label(master, font="Arial 15", bg="#ADD8E6", text="PB:")
        self.pb_time = tk.Label(master, font="Arial 15", bg="#ADD8E6")
        self.gold = tk.Label(master, font="Arial 15",  bg="#ADD8E6", text="Gold: ")
        self.gold_time = tk.Label(master, font="Arial 15", bg="#ADD8E6")
        self.time_save = tk.Label(master, font="Arial 10", text="Time save:", bg="#ADD8E6")
        self.time_save_time = tk.Label(master, font="Arial 10",  bg="#ADD8E6")



        self.undo_button = tk.Button(master, text="Undo", command=self.undo,bg="#ADD8E6")
        self.undo_button.grid(row=self.cur_run.total_splits+1, column=0)
            

    def refresh_time(self):
        if not self.finished and self.started:
            cur = time.monotonic()
            total = cur-self.first
            split = cur-self.prev
            self.cur_seg_time.configure(text=convertSecsToTime(split), bg="#ADD8E6")
            self.total_time_label.configure(text=convertSecsToTime(total), bg="#ADD8E6")
            self.total_time_label.after(75, self.refresh_time)

    def undo(self):
        self.splitResults.pop()
        self.split_elements[len(self.splitResults)*3+2].configure(text=convertSecsToTime(calculate_total_time(self.cur_run.PBSplits, 1, len(self.splitResults)+1)))
        self.split_elements[len(self.splitResults)*3+1].configure(text="")
        
        
        
    def enter(self, event):
        if self.finished:
            pass
        elif self.started:
            cur = time.monotonic()
            splitTime = round(cur-self.prev,3)
            self.prev = cur
            total = round(cur - self.first,3)
            next_diff = self.split_elements[len(self.splitResults)*3+1]

            self.prev_seg.grid(row=self.cur_run.total_splits+8, column=1, sticky=tk.E)
            self.prev_seg_time.grid(row=self.cur_run.total_splits+8, column=2)
            self.split_elements[len(self.splitResults)*3+2].configure(text=convertSecsToTime(total))

            self.splitResults.append(splitTime)
            self.best_possible_time.configure(text=convertSecsToTime(calculate_total_time(self.cur_run.sumOfBest, len(self.splitResults)+1, len(self.cur_run.sumOfBest))+total))
            diff =  total - calculate_total_time(self.cur_run.PBSplits, 1, len(self.splitResults))

       

            if diff > 0:
                next_diff.configure(text="+"+convertSecsToTime(diff))
            else:
                next_diff.configure(text="-"+convertSecsToTime(-diff))

            split_diff = splitTime - self.cur_run.PBSplits[len(self.splitResults)]
            if split_diff > 0:
                self.prev_seg_time.configure(text=convertSecsToTime(splitTime)+" (+"+convertSecsToTime(split_diff)+")")
            else:
                self.prev_seg_time.configure(text=convertSecsToTime(splitTime)+" (-"+convertSecsToTime(-split_diff)+")")

            if splitTime < self.cur_run.sumOfBest[len(self.splitResults)]:
                next_diff.configure(fg="yellow")
            elif splitTime < self.cur_run.PBSplits[len(self.splitResults)]:
                next_diff.configure(fg="#57E964")
            else:
                next_diff.configure(fg="red")

            if self.final:
                self.finished = True
                self.splitResults.insert(0, total)
                with open("raw_results.txt", "a+") as f:
                    f.write(str(self.splitResults)+"\n")
                splitResults = [convertSecsToTime(split) for split in self.splitResults]
                with open("results.txt", "a+") as f:
                    f.write(str(splitResults)+"\n")
            else:
                cur_seg_pb = self.cur_run.PBSplits[len(self.splitResults)+1]
                cur_seg_gold = self.cur_run.sumOfBest[len(self.splitResults)+1]
                self.pb_time.configure(text=convertSecsToTime(cur_seg_pb))
                self.gold_time.configure(text=convertSecsToTime(cur_seg_gold))
                self.time_save_time.configure(text=convertSecsToTime(cur_seg_pb-cur_seg_gold))
            if len(self.splitResults) == self.cur_run.total_splits-1:
                self.final = True
                

        else:
            self.started = True
            self.prev = time.monotonic()
            self.first = self.prev


            self.cur_seg.grid(row=self.cur_run.total_splits+4, column=1, sticky=tk.E)
            self.cur_seg_time.grid(row=self.cur_run.total_splits+4, column=2)
            self.pb.grid(row=self.cur_run.total_splits+5, column=1, sticky=tk.E)
            self.pb_time.grid(row=self.cur_run.total_splits+5, column=2)
            self.gold.grid(row=self.cur_run.total_splits+6, column=1, sticky=tk.E)
            self.gold_time.grid(row=self.cur_run.total_splits+6, column=2)
            self.time_save.grid(row=self.cur_run.total_splits+7, column=1, sticky=tk.E)
            self.time_save_time.grid(row=self.cur_run.total_splits+7, column=2)

            
            cur_seg_pb = self.cur_run.PBSplits[len(self.splitResults)+1]
            cur_seg_gold = self.cur_run.sumOfBest[len(self.splitResults)+1]
            self.pb_time.configure(text=convertSecsToTime(cur_seg_pb))
            self.gold_time.configure(text=convertSecsToTime(cur_seg_gold))
            self.time_save_time.configure(text=convertSecsToTime(cur_seg_pb-cur_seg_gold))
            self.total_time_label.after(50, self.refresh_time)


class Run:
    def __init__(self, prev_runs, name):
        self.name = name
        
        self.splits =  ["Cap", "Caskade", "Sand", "Lake", "Wood", "Cloud", "Lost", "Night Metro", "Day Metro", "Snow", "Beach", "Luncheon", "Ruined", "Bunnies", "Bowsers", "Moon"]
        self.total_splits = len(self.splits)

        self.pb = 9999999999999999999
        #Best ever record for each split
        self.sumOfBest = [self.pb]*(len(self.splits)+1)
        #Times in overall PB
        self.PBSplits = [self.pb]*len(self.splits)

        with open(prev_runs, "r+") as f:
            for splits in f:
                splits = splits[1:-2].split(",")
                total = float(splits[0])
                if total < self.pb:
                    self.pb = total
                    self.PBSplits = [float(split) for split in splits]
                    
                for i in range(len(self.splits)+1):
                    time = float(splits[i])
                    if time  < self.sumOfBest[i]:
                        self.sumOfBest[i] = time


        print(convertSecsToTime(self.pb))
        print([convertSecsToTime(split) for split in self.PBSplits])
        self.sumOfBest[0] = 0
        sumOfBest = sum(self.sumOfBest)
        self.sumOfBest[0] = sumOfBest
        print([convertSecsToTime(split) for split in self.sumOfBest])
        print(self.sumOfBest)

        self.loadSegments()

    def loadSegments(self):
        self.segments = []
        for i in range(self.total_splits):
            self.segments.append(Segment(self.splits[i], self.sumOfBest[i+1], self.PBSplits[i+1]))
        for segment in self.segments:
            print(segment)
        
            
                        
        
class Segment:
    def __init__(self, name, gold, pb_time):
       self.name = name
       self.gold = gold
       self.sub_segments = []
       self.time = 0
       self.pb_time = pb_time
       self.final = False

    def __str__(self):
        return str((self.name, self.gold, self.pb_time))


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#ADD8E6")
    timer = Timer(root)
    root.bind('<Return>', timer.enter)
    root.mainloop()
