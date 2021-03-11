#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 19:22:10 2021

@author: Francesco David Nota
"""

import pandas as pd
import os
import math
from jobShopGA import JobShopGA
from multiprocessing import Queue

class TreeGA:
    # two bidimensional arrays representing on the columns the operations and on the rows the jobs
    # the j,z value is in the first array a processing time for job j and operation z
    # while in the second array is the machine where the operation is executed at step z
    processingTimes = None
    machineSequences = None
    
    minimumMakespan = None
    bestSolution = None
    bestMachineSchedules = None
    bestJobTimings = None
    
    jobShopGeneticAlgorithm = None
    
    num_jobs = 0
    
    allProcesses = None
    
    def __init__(self,fileName,populationNumber = 900,iterationNumber = 900,numberThatIsAPowerOfTwo = 128):
        self.populationNumberBase = populationNumber
        self.iterationNumberBase = iterationNumber
        self.numberThatIsAPowerOfTwo = numberThatIsAPowerOfTwo
        
        self.processingTimes = list()
        self.machineSequences = list()
        
        self.allProcesses = list()
        
        with open(fileName,"r") as file:
            firstLineFound = False
            numberOfRowsForMatrices = 0
            for line in file:
                line = line.replace("\n","")
                line = line.replace("  "," ")
                if line[0] == "#":
                    continue
                elif not firstLineFound:
                    firstLineFound = True
                else:
                    #get all operations in an array
                    #
                    lineArray = line.split(" ")
                    
                    if lineArray[0] == "":
                        lineArray.pop(0)
                      
                    self.processingTimes.append([])
                    self.machineSequences.append([])
                    
                    for index in range(len(lineArray)):
                        if index % 2 == 0:
                            self.machineSequences[numberOfRowsForMatrices].append(int(lineArray[index]))
                        else:
                            self.processingTimes[numberOfRowsForMatrices].append(int(lineArray[index]))
                        
                    numberOfRowsForMatrices = numberOfRowsForMatrices + 1
            
            file.close()
        
    def execute(self):
        machineSequencesDf = pd.DataFrame(self.machineSequences)
        processingTimesDf = pd.DataFrame(self.processingTimes)
        
        dfshape = processingTimesDf.shape
        num_machines = dfshape[1] # number of machines
        self.num_jobs = dfshape[0] # number of jobs
        num_genes = num_machines * self.num_jobs # number of genes in a chromosome
        
        self.processingTimes = [list(map(int, processingTimesDf.iloc[i])) for i in range(self.num_jobs)]
        self.machineSequences = [list(map(int,machineSequencesDf.iloc[i])) for i in range(self.num_jobs)]
        
        finalDataframeResult = None
        
        numberOfAlgorithms = self.numberThatIsAPowerOfTwo
        populationArray = list()
        numberOfIterations = int(math.log(self.numberThatIsAPowerOfTwo,2)) + 1
        
        print(["layers","numberOfIterations","numberOfAlgorithms","populationArray"])
        
        
        #for all the layers in the tree
        for i in range(numberOfIterations):
            
            # the population number and the number of iterations must be proportional to the layer number. the lower the number of algorithms the lower the population 
            # and the higher the iterations. the opposite is valid when the number of algorithm is higher (big population, few iterations)
            populationNumber = int(self.populationNumberBase / numberOfAlgorithms) 
            iterationNumber = int(self.iterationNumberBase / numberOfAlgorithms)

            print([i,iterationNumber,numberOfAlgorithms,populationNumber])
            
            # useful for parallel processes communication
            queue = Queue()
            
            localPopulationArray = list()
            
            if numberOfAlgorithms > (os.cpu_count() * 4) or numberOfAlgorithms == 1:
                algorithms = list()
                isProcess = False
              
                for j in range(numberOfAlgorithms):   
                    # JobShopGA extends the class process and therefore is an external forked subprocess of the main one
                    if len(populationArray) == 0:
                        self.jobShopGeneticAlgorithm = JobShopGA(isProcess,queue,populationNumber,iterationNumber,num_genes,self.num_jobs,self.processingTimes,self.machineSequences)
                    else:
                        firstDF = populationArray[j * 2]
                        secondDF = populationArray[(j * 2) + 1]

                        populationDfFromAlgorithms = pd.concat([firstDF,secondDF])
                        populationDfFromAlgorithms = populationDfFromAlgorithms.sort_values(by=["fitness"])
                        # here select only the best results that are the first 'populationNumber' results beacuse the 
                        # dataframe is ordered by fitness value
                        populationDfFromAlgorithms = populationDfFromAlgorithms.iloc[0:populationNumber]

                        self.jobShopGeneticAlgorithm = JobShopGA(isProcess,queue,populationNumber,iterationNumber,num_genes,self.num_jobs,self.processingTimes,self.machineSequences,populationDfFromAlgorithms)

                    self.jobShopGeneticAlgorithm.run()

                    algorithms.append(self.jobShopGeneticAlgorithm)

                for instanceOfAlgorithm in algorithms:
                    localPopulationArray.append(queue.get())
            else:
                processes = list()
                isProcess = True
              
                #for all algorithms in the layer compute and get the best results in terms of makespan
                for j in range(numberOfAlgorithms):   
                    # JobShopGA extends the class process and therefore is an external forked subprocess of the main one
                    if len(populationArray) == 0:
                        self.jobShopGeneticAlgorithm = JobShopGA(isProcess,queue,populationNumber,iterationNumber,num_genes,self.num_jobs,self.processingTimes,self.machineSequences)
                    else:
                        firstDF = populationArray[j * 2]
                        secondDF = populationArray[(j * 2) + 1]

                        populationDfFromAlgorithms = pd.concat([firstDF,secondDF])
                        populationDfFromAlgorithms = populationDfFromAlgorithms.sort_values(by=["fitness"])
                        # here select only the best results that are the first 'populationNumber' results beacuse the 
                        # dataframe is ordered by fitness value
                        populationDfFromAlgorithms = populationDfFromAlgorithms.iloc[0:populationNumber]

                        self.jobShopGeneticAlgorithm = JobShopGA(isProcess,queue,populationNumber,iterationNumber,num_genes,self.num_jobs,self.processingTimes,self.machineSequences,populationDfFromAlgorithms)

                    self.jobShopGeneticAlgorithm.start()

                    processes.append(self.jobShopGeneticAlgorithm)

                for instanceOfAlgorithmProcess in processes:
                    localPopulationArray.append(queue.get())

                for instanceOfAlgorithmProcess in processes:
                    instanceOfAlgorithmProcess.join()
                    self.allProcesses.append(instanceOfAlgorithmProcess)
                
            numberOfAlgorithms = int(numberOfAlgorithms / 2)
            populationArray = localPopulationArray
            
        # GET THE BEST RESULT FROM THE ALL BEST RESULTS ARRAY
        
        finalDataframeResult =  populationArray[0]
        
        finalDataframeResult = finalDataframeResult.reset_index()
        finalDataframeResult = finalDataframeResult.drop(columns=["index"])
        indexOfMin = finalDataframeResult["fitness"].idxmin()
        self.minimumMakespan = finalDataframeResult.loc[indexOfMin]["fitness"]
        self.bestSolution = finalDataframeResult.drop(columns=["fitness"]).iloc[indexOfMin]
        
        bestSolutionArray = self.jobShopGeneticAlgorithm.elaborateIndividualFitness(list(self.bestSolution.values),self.num_jobs,self.machineSequences,self.processingTimes)
        self.bestMachineSchedules = bestSolutionArray[2]
        self.bestJobTimings = bestSolutionArray[3]
    
    def terminateAllProcesses(self):
        for process in self.allProcesses:
            process.terminate()
    
    def getMinimumMakespan(self):
        return self.minimumMakespan
    
    def getBestSolution(self):
        return self.bestSolution
    
    def getBestSolutionMachineSchedules(self):
        return self.bestMachineSchedules
    
    def getBestSolutionJobTimings(self):
        return self.bestJobTimings
    
    def getJobProcessingTimes(self):
        return self.processingTimes
    
    def getMachineSequences(self):
        return self.machineSequences
    
    