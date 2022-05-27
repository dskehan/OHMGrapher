import pandas as pd, matplotlib.pyplot as plt, time, re 
from tkinter.filedialog import askopenfilename
from tkinter import Tk, messagebox  


def getPandaObject(fileName):
    newFirstLine =""

    with open(fileName, 'r+') as f: #open in read / write mode
        x = f.readline()
        if x[:4:] != "Time": #read the first line and throw it out
            data = f.read() #read the rest
            f.seek(0) #set the cursor to the top of the file
            f.write(data) #write the data back
            f.truncate() #set the file size to the current size

    with open(fileName, 'r+') as f:
        ### find the current line and edit the values based on whats before
        x = f.readline()
        newFirstLine = re.sub("\"CPU Package\"(?=,\"CPU CCD #1\")", "\"CPU Temperature\"", x) #search for old values and replace
        newFirstLine = re.sub("\"CPU Cores\"(?=,\"Memory\")","\"CPU Core Percentage\"", newFirstLine)
        newFirstLine = re.sub("(?<=\"Available Memory\",)\"GPU Core\"", "\"GPU Temperature\"", newFirstLine)
        newFirstLine = re.sub("\"GPU Core\"(?=,\"Temperature\",)", "GPU Percentage", newFirstLine)
        f.read(1)
        firstline = f.readline()
        data = f.read()
        f.seek(0)
        f.write(newFirstLine + data)
        f.truncate()

    return pd.read_csv(fileName, parse_dates=["Time"])

def graphData(fileName):

    graphGPU = False
    MsgBox = messagebox.askquestion('Graph GPU Data','Do you want to graph the GPU data?')

    if MsgBox == 'yes':
        graphGPU = True
    
    ohmData = getPandaObject(fileName)
    date = str(ohmData["Time"][0]).split(" ")[0]

    cpuCoreAbove30 = ohmData[ohmData["CPU Core Percentage"] > 25] 
    
    data = ohmData

    avg = "CPU Above 25% Average: " + str(cpuCoreAbove30["CPU Temperature"].mean()) + "\nCPU Average:  " + str(ohmData["CPU Temperature"].mean())
    highlow = "CPU Highest: " + str(ohmData["CPU Temperature"].max()) + "\nCPU Lowest:  " + str(ohmData["CPU Temperature"].min())

    fig = plt.figure(figsize=(18, 13), dpi=60)
    ax = fig.add_subplot(111)

    if graphGPU:
        gpuCoreAbove30 = cpuCoreAbove30[cpuCoreAbove30["GPU Percentage"] > 25]
        GPUavg = "GPU Above 25% Average: " + str(cpuCoreAbove30["GPU Temperature"].mean()) + "\nGPU Average:  " + str(ohmData["GPU Temperature"].mean())
        GPUhighlow =  "GPU Highest: " + str(ohmData["GPU Temperature"].max()) + "\nGPU Lowest:  " + str(ohmData["GPU Temperature"].min())
        data.plot(x="Time", y=["CPU Temperature","CPU Core Percentage", "GPU Temperature", "GPU Percentage"], ax=ax)
        ax.text(0.35,0.05, GPUavg, transform=fig.transFigure)
        ax.text(0.55,0.05, GPUhighlow, transform=fig.transFigure)
    else: 
        data.plot(x="Time", y=["CPU Temperature","CPU Core Percentage"], ax=ax)

    ax.text(0.35,0.09,avg,transform=fig.transFigure)
    ax.text(0.55,0.09,highlow,transform=fig.transFigure)

    plt.show()

def loadFile():
    Tk().withdraw() #TODO Move this and check if a file is loaded or not... if it is call graphData() else exit.. 
    fileName = askopenfilename()
    if fileName != '':
        graphData(fileName)
    else: 
        quit()

loadFile()
goAgain = True
while goAgain:
    anotherFile = messagebox.askquestion('Load Another File','Do you want to load another file?')
    if anotherFile == 'no':
        goAgain = False
    else: 
        loadFile()