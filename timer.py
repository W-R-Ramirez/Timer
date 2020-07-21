import time
def convertTimeToSecs(timeStr):
    colon = timeStr.find(":")
    mins = int(timeStr[:colon])
    secs = int(timeStr[colon+1:]) + 60*mins
    return secs

def convertSecstoTime(secStr):
    secs = float(secStr)
    mins = secs//60
    secs = secs % 60
    if secs >= 10:
        timeStr = str(int(mins))+":"+str(round(secs,3))
    else:
        timeStr = str(int(mins))+":0"+str(round(secs,3))
    return timeStr

splits = ["Cap", "Caskade", "Sand", "Lake", "Wood"]
f = open("results.txt", "r+")
PB = f.readline()

PBsecs = int(convertTimeToSecs(PB))
print("PB: " + PB.strip())
print(PBsecs)
#Times for current run
splitResults = []
#Times in overall PB
PBSplits = []
#Best ever record for each split
splitRecords = []
input("Start")
prev = time.monotonic()
first = prev

for kingdom in splits:
    input(kingdom)
    section = f.readline().strip()
    if section != kingdom:
         break
    #time in overall PB for split
    PBSectionTime = f.readline().strip()
    #fastest ever time for split
    splitPB = f.readline().strip()

    PBSplits.append(PBSectionTime)
    splitRecords.append(splitPB)
    cur = time.monotonic()
    splitTime = cur-prev
    splitResults.append(splitTime)
    print(kingdom + " Split: " + convertSecstoTime(str(splitTime)))
    total = cur-first
    print("Total: " + convertSecstoTime(total))
    
    prev = cur
record = False
if int(total) < PBsecs:
    record = True

    

splitResults = [convertSecstoTime(split) for split in splitResults]
print(total)
print(splitResults)
print(PBSplits)
print(splitRecords)

with open("raw_results.txt", "a+") as f:
    f.write(str(splitResults)+"\n")
