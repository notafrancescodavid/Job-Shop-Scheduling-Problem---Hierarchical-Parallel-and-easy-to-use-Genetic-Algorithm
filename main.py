#from tree_GA import TreeGA
import os
import time
import json
import pandas as pd
import sys
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches
from treeGA import TreeGA

def printChart(toFile=False,filename="",lang="en"):
    iteration = 0

    jobsForMachines = []
    jobsForMachinesWithJobId = []
    
    for machineSchedule in bestMachineSchedules:
        jobsForMachine = []
        jobsForMachineWithJobId = []
    
        for jobOperationCouple in machineSchedule:
            jobId = jobOperationCouple[0]
            operationNumber = jobOperationCouple[1]
            
            #print("stating time, ending time")
            jobStartAndEndTime = bestJobTimings[jobId][operationNumber]
            jobsForMachine.append((jobStartAndEndTime[0],jobStartAndEndTime[1] - jobStartAndEndTime[0]))
            jobsForMachineWithJobId.append((jobStartAndEndTime[0],jobStartAndEndTime[1],jobId))
            #print([jobStartAndEndTime[0],jobStartAndEndTime[1],jobId])
    
        jobsForMachinesWithJobId.append(jobsForMachineWithJobId)
        jobsForMachines.append(jobsForMachine) 
        iteration = iteration + 1  

    font = {'family' : 'sans-serif',
            'weight' : 'normal',
            'size'   : 22}
    
    plt.rc('font', **font)
    
    chartPatches = []
    
    #colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#000000']
    colors = ["#696969","#8b4513","#808000","#483d8b","#008000","#008b8b","#00008b","#8fbc8f","#800080","#b03060","#ff0000","#ffa500","#ffff00","#00ff00","#8a2be2","#00ff7f","#dc143c","#00ffff","#00bfff","#0000ff","#adff2f","#b0c4de","#ff7f50","#ff00ff","#1e90ff","#90ee90","#ff1493","#ee82ee","#ffe4b5","#ffb6c1"]
    for j in range(len(bestJobTimings)):
        colorHex = colors[j]
        chartPatches.append(mpatches.Patch(color=colorHex, label='Job' + str(j)))
    
    fig, schedule = plt.subplots() 
    
    fig.set_figheight(18)
    fig.set_figwidth(25)
    
    numOfMachines = len(bestMachineSchedules)
    
    # Setting Y-axis limits 
    schedule.set_ylim(0, numOfMachines * 20) 
      
    # Setting X-axis limits 
    schedule.set_xlim(0, minimumMakespan) 
      
    # Setting labels for x-axis and y-axis 
    if lang == "it":
        schedule.set_xlabel("Minuti sin dall'inizio") 
        schedule.set_ylabel('Macchina') 
        machineString = "Macchina"
    else:
        schedule.set_xlabel("Minutes since the start") 
        schedule.set_ylabel('Machine')
        machineString = "Machine"
      
    schedule.grid(True)
    
    # Setting ticks on y-axis 
    ytiks = []
    yticksLabels = []
    verticalOffeset = 20
    for i in range(numOfMachines):
        ytiks.append(i * verticalOffeset)
        yticksLabels.append(machineString + " " + str(i))
        colorsForChart = []
        jobIds = []
        for j in range(len(jobsForMachinesWithJobId[i])):
            jobId = jobsForMachinesWithJobId[i][j][2]
            colorsForChart.append(colors[jobId])
            jobIds.append(jobId)
    
        schedule.broken_barh(jobsForMachines[i], (i * verticalOffeset, verticalOffeset/2), facecolors = tuple(colorsForChart))
    
        for j in range(len(jobsForMachines[i])):
            x1,x2 = jobsForMachines[i][j]
            schedule.text(x=x1 + x2/2, y=(i * verticalOffeset) + 5,s=jobIds[j],ha='center', va='center',color='white',fontsize=18,fontweight="bold")
    
    schedule.set_yticks(ytiks)
    # Labelling tickes of y-axis 
    schedule.set_yticklabels(yticksLabels)
    fig.legend(handles=chartPatches,title='Nomi Job', bbox_to_anchor=(0.9, 0.9), loc='upper left')
    
    if toFile:
        plt.savefig(filename) 
        
    plt.show()


if __name__ == '__main__':
    start_time = time.time()

    fileInstanceName = sys.argv[1]
    populationNumber = int(sys.argv[2])
    iterationNumber = int(sys.argv[3])
    numberThatIsAPowerOfTwo = int(sys.argv[4])

    treeGA = TreeGA(fileName = fileInstanceName,populationNumber = populationNumber,iterationNumber = iterationNumber,numberThatIsAPowerOfTwo = numberThatIsAPowerOfTwo)
    treeGA.execute()

    minimumMakespan = treeGA.getMinimumMakespan()
    bestSolution = treeGA.getBestSolution()
    bestMachineSchedules = treeGA.getBestSolutionMachineSchedules()
    bestJobTimings = treeGA.getBestSolutionJobTimings()

    print("")

    print("Minimum Makespan:")
    print(minimumMakespan)

    print("")

    print("Best solution")
    print(bestSolution.values)

    end_time = time.time()

    print("Execution time in seconds: ")
    print(end_time - start_time)
    
    if sys.argv[5] == "plot":
        printChart()
    elif sys.argv[5] == "plot_to_file":
        printChart(toFile=True,filename=sys.argv[6],lang="it")
