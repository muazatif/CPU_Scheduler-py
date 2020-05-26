singleLayer = True

timer = 0
class Process:
    letter = ''
    timeNeeded = 0
    releaseTime = 0
    runningTime = 0
    sessionTime = 0
    def __init__(self, name, releaseTime, timeNeeded):
        self.time = timeNeeded
        print(name)
        self.letter = name
        self.runningTime = 0
        self.timeNeeded = timeNeeded
        self.releaseTime = releaseTime
    def run(self):
        self.timeNeeded -= 1
        self.runningTime += 1
        self.sessionTime += 1

#processes to be moved to next layer
forNextLayer = []
#processes currently completed
#  printed at the end of execution to show completion order of processes
order = []
switches = []
#number of processes remaining
processCounter = 0
# quanta for round robin in Time Units
quanta = 2
# label of last process that executed (for display purposes)
lastProcess = ''
class Layer:
    #how long it has currently been running
    runningTime = 0
    #how long it can run before it has to switch to next layer/queue
    maxRunTime = 0
    #label for display purposes
    letter = ''
    #how long a process can run in this layer before having to move onto the next
    # this doesn't apply if isLast is set to true
    tolerance = 0
    # record of every switch
    record = ""
    #list of processes in queue
    processes = []
    #list of processes not released yet
    unreleased = []
    whenStart = 0
    #is this 
    isLast = False
    #is Round Robin?
    # if set to false it will simply run a process to completion with no interleaving 
    RR = True

    def __init__ (self, maxRunTime, tolerance, RR, isLast):
        self.RR = RR
        self.isLast = isLast
        self.tolerance = tolerance
        self.maxRunTime = maxRunTime
        self.currentTime = 0
        self.processes = []
        self.unreleased = []

    def addUnreleasedProcess(self, process):
        global processCounter
        processCounter += 1
        self.unreleased.append(process)

    def addProcess(self, process):
        global processCounter
        processCounter += 1
        self.processes.append(process)

    def moveQueue(self):
        newProcess = self.processes[0]
        self.processes.pop(0)
        self.processes.append(newProcess)

    def getProcessAsStr(self, array):
        word = "["
        for process in array:
            word += process.letter
            word += ", "
        word += "]"
        return word

    def getReleasedProcesses(self):
        listP = []
        for process in self.unreleased:
            if self.currentTime == process.releaseTime:
                self.processes.append(process)
            else:
                listP.append(process)
        self.unreleased = listP
    
    def run(self):
        global processCounter, timer, lastProcess
        while((singleLayer or self.currentTime < self.maxRunTime or self.maxRunTime < 0) and processCounter > 0 ):
            display = False
            self.getReleasedProcesses()
            status = ""
            if(len(self.processes) == 0):
             #   print("nothing to run")
                return 0
            self.processes[0].run()
            timer += 1
            t = str(timer)
            tn = str(self.processes[0].timeNeeded)
            if(timer < 10):
                t = " " + t
            if(self.processes[0].timeNeeded < 10):
                tn = " " + tn
            label = self.processes[0].letter
            if label != lastProcess:
                if lastProcess != '':
                    self.record += (lastProcess + "[" + str(whenStart) + "," + str(self.currentTime) + "[; ")
                lastProcess = self.processes[0].letter
                whenStart = self.currentTime
                display = True

            
            #is process complete?
            if(self.processes[0].timeNeeded == 0):
            #    print(self.processes[0].letter, " is done!")
                order.append(str(self.processes[0].letter) + ": " + str(timer))
                self.processes.pop(0)
                processCounter -= 1
            
            else:
                if (int(self.processes[0].runningTime/quanta) == self.tolerance and not self.isLast):
                    #move to new level
                    display = True
                    status = " moved " + self.processes[0].letter + "  to next level from "+ self.letter
                    x = self.processes[0]
                    self.processes.pop(0)
                    x.sessionTime = 0
                    x.runningTime = 0
                    forNextLayer.append(x)
                elif  self.processes[0].sessionTime == quanta and self.RR:
                    self.processes[0].sessionTime = 0
                    self.moveQueue()
            self.currentTime += 1
            status = ' ' * (maxQueueString - (len(self.getProcessAsStr(self.unreleased)))) + "|" + status    
            unrelString =' ' * (maxQueueString - (len(self.getProcessAsStr(self.processes)))) + "| unreleased queue: " + self.getProcessAsStr(self.unreleased)    
            if display:
                print("Time: ", t, "| Queue: ", self.letter, "| process time remaining: ", tn, "| process: ", label, "| current queue: ", self.getProcessAsStr(self.processes), unrelString, status)
        
        if lastProcess != '':
            self.record += (lastProcess + "[" + str(whenStart) + "," + str(self.currentTime) + "[;")
        self.currentTime = 0
            

    def start(self):
        global forNextLayer
        self.processes += forNextLayer
        forNextLayer = []
        self.run()

#output array of processes as strings
def processesToStr(array):
    word = "["
    for process in array:
        word += process.letter
        word += ", "
    word += "]"
    return word

#define each layer:
# this layer h:
#       runs for 6 time units before the next layer starts executing
#       only allows a process to run once before moving it to the next layer
#       does round robin
#       is NOT the last layer
#       is denoted by the letter 'H'
h = Layer(None,None, True, True)
h.letter = 'H'
# this layer m:
#       runs for 4 time units before the next layer starts executing
#       only allows a process to run twice before moving it to the next layer
#       does round robin
#       is NOT the last layer
#       is denoted by the letter 'M'
m = Layer(4,2, True, False)
m.letter = 'M'
# this layer l:
#       runs for 2 time units before the next layer starts executing
#       process never moves to another layer at is it is the last layer
#       does NOT do round robin
#       is the last layer
#       is denoted by the letter 'L'
l = Layer(2,None, False, True)
l.letter = 'L'

#define each process with a symbol and how long their execution time is
a = Process('A', 0, 4)
b = Process('B', 2, 17)
c = Process('C', 14, 6)
d = Process('D', 7, 15)
e = Process('E', 11, 3)

#add each process to the layer that will run first
h.addUnreleasedProcess(a)
h.addUnreleasedProcess(b)
h.addUnreleasedProcess(c)
h.addUnreleasedProcess(d)
h.addUnreleasedProcess(e)

#add each layer to list layers in order of execution
layers = []
layers.append(h)
#layers.append(m)
#layers.append(l)

#loop through each layer until all processes have finished executing
pointer = 0
maxQueueString = len(processesToStr(layers[0].processes)) + len(processesToStr(layers[0].unreleased))
print("initial process queue: ", processesToStr(layers[0].processes))
if(len(layers) > 1):
    singleLayer = False
else:
    singleLayer = True

while(processCounter > 0):
    layers[pointer].start()
    pointer += 1
    
    if pointer > (len(layers) - 1):
        pointer = 0
    
print("\ntotal time taken: ", timer, " time units\n")
print("completion order and time at completion: ", )
for i in order:
    print("                                         ", i)
for l in layers:
    print(l.record)
