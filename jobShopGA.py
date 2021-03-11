#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 19:01:55 2021

@author: Francesco David Nota
"""

'''==========Solving job shop scheduling problem by gentic algorithm in python ======='''

import pandas as pd
import numpy as np
import copy

from multiprocessing import Process
    
class JobShopGA(Process):
    #algorithm configurations

    initial_random_pop_multiplier = 120
    initial_random_population_size = None
    
    population_size = None
    
    crossover_rate = 0.6
    random_population_rate = 0.1
    
    mutation_rate = None
    mutation_selection_rate = 0.1
    
    num_iteration = None
    
    resultPopulationAndFitnessDF = None
    
    processingTimes = None
    machineSequences = None
    populationAndFitnessDF = None
    
    queue = None
    
    def __init__(self,isProcess,queue,populationNumber,iterationNumber,num_genes,num_jobs,processingTimes,machineSequences,populationAndFitnessDF = None):
        if isProcess:
            Process.__init__(self)
            
        self.queue = queue
            
        self.population_size = populationNumber
        self.num_iteration = iterationNumber
        self.num_genes = num_genes
        self.num_jobs = num_jobs
        
        self.initial_random_population_size = self.population_size * self.initial_random_pop_multiplier
        self.mutation_rate = 1 - self.crossover_rate - self.random_population_rate
        
        self.processingTimes = processingTimes
        self.machineSequences = machineSequences
        self.populationAndFitnessDF = populationAndFitnessDF
    
    def run(self):
        self.execute(self.processingTimes,self.machineSequences,self.populationAndFitnessDF)
    
    def getFinalResultPopulationAndFitnessDF(self):
        return self.resultPopulationAndFitnessDF
    
    def execute(self,processingTimes,machineSequences,populationAndFitnessDF = None,showPercentage = False):
        
        if populationAndFitnessDF is None:
            population_list = self.getPopulation(self.initial_random_population_size,self.num_genes,self.num_jobs,machineSequences,processingTimes)
            #elaborateIndividualFitness(population_list[0],num_jobs,machineSequences,processingTimes)
            fitnessValues = self.elaborateFitness(population_list,self.num_jobs,machineSequences,processingTimes)
            
            #select the best elements in the population and then return them back in the right number
            populationAndFitnessDF = pd.DataFrame(population_list)
            populationAndFitnessDF["fitness"] = np.array(fitnessValues)
            populationAndFitnessDF = populationAndFitnessDF.sort_values(by=['fitness']).iloc[0:self.population_size]
        
        #apply SELECTION,CROSSOVER, MUTATION, CALCULATE FITNESS VALUE, APPLY COMPARISON FOR THE BEST
        for n in range(self.num_iteration):
            
            if showPercentage:
                percent = (100 * n) / self.num_iteration
                    
                if percent == 25:
                    print("25%")
                elif percent == 50:
                    print("50%")
                elif percent == 75:
                    print("75%")
            
            populationAndFitnessDF = populationAndFitnessDF.drop(columns=["fitness"])
            population_list_copy = populationAndFitnessDF.values
            
            new_population_list = list()
            tenPercentOfPopulation = int(len(population_list_copy) * 0.1)
            
            for populationTenPercentElement in population_list_copy[0:tenPercentOfPopulation]:
                new_population_list.append(populationTenPercentElement)
            
            reducedPopulationLength = len(population_list_copy) - tenPercentOfPopulation
            
            ''' ---------------- CROSSOVER ----------------'''
            #for the rate of crossover make uniform crossover
            
            new_population_list_for_crossover = population_list_copy[tenPercentOfPopulation:int(reducedPopulationLength * self.crossover_rate) + tenPercentOfPopulation]
            
            lengthOfSolution = len(new_population_list_for_crossover[0])
            lengthOfCrossoverSubset = len(new_population_list_for_crossover)
            
            for i in range(lengthOfCrossoverSubset):
                for z in range(lengthOfSolution):
                    if np.random.rand() > 0.5:
                        # put the element of next solution in the current one denoted by [i,z] indices
                        # this is like swapping a coin and is a uniform crossover
                        new_population_list_for_crossover[i][z] = new_population_list_for_crossover[np.random.randint(lengthOfCrossoverSubset)][z]
                    #else: leave it in the same way. This code is only for understanding why there is no actual else
                        #put value of first index of population
                        #new_population_list_for_crossover[i][z] = new_population_list_for_crossover[i][z]
                        
                new_population_list.append(new_population_list_for_crossover[i])
            
            ''' ---------------- MUTATION ----------------'''
            # for the (1 - crossover_rate) make random (mutation_selection_rate)% genes mutations.
            # The mutations are the mutation_selection_rate of the length of an individual and they are swaps
            
            new_population_list_for_mutation = copy.deepcopy(population_list_copy[0:int(reducedPopulationLength * self.mutation_rate)])
            
            new_pop_for_mutation_lenght = len(new_population_list_for_mutation)
            
            numberOfPopulationElements = 0
            
            for j in range(new_pop_for_mutation_lenght):
                #here do mutations
                #do mutation_selection_rate of swaps of the elements in the sequence
                # the lower the fit value of the solution the higher the swaps
                if j < new_pop_for_mutation_lenght / 4:
                    numberOfSwaps = int(self.num_genes * (self.mutation_selection_rate / 4))
                elif j < new_pop_for_mutation_lenght / 3:
                    numberOfSwaps = int(self.num_genes * (self.mutation_selection_rate / 3))
                elif j < new_pop_for_mutation_lenght / 2:
                    numberOfSwaps = int(self.num_genes * (self.mutation_selection_rate / 2))
                elif j < new_pop_for_mutation_lenght / 1:
                    numberOfSwaps = int(self.num_genes * self.mutation_selection_rate)
                    
                if numberOfSwaps < 1:
                    numberOfSwaps = 1
                        
                for z in range(numberOfSwaps):
                    #get random indices
                    randomIndex1 = np.random.randint(self.num_genes)
                    randomIndex2 = np.random.randint(self.num_genes)
                    #get the values of the selected random indices and swap
                    new_population_list_for_mutation[j][randomIndex1] = new_population_list_for_mutation[j][randomIndex2]
                    new_population_list_for_mutation[j][randomIndex2] = new_population_list_for_mutation[j][randomIndex1]
        
                # add the mutation to the new population.
                new_population_list.append(new_population_list_for_mutation[j])
                numberOfPopulationElements = numberOfPopulationElements + 1
                
            ''' ---------------- ADDING RANDOM POPULATION ---------------- '''
            randomPopulationSize = self.population_size - len(new_population_list)
            random_population = self.getPopulation(randomPopulationSize,self.num_genes,self.num_jobs,machineSequences,processingTimes)
            for populationRandomElement in random_population:
                new_population_list.append(populationRandomElement)
            
            ''' ---------------- FITNESS-AND-REPAIRMENT ELABORATION ----------------'''
            #calculate the fitness of all the new population
            fitnessValues = self.elaborateFitness(new_population_list,self.num_jobs,machineSequences,processingTimes)
            
            # reorder the population in terms of fittest, put the best 5 in dataframe called fittestDf
            populationAndFitnessDF = pd.DataFrame(new_population_list)
            populationAndFitnessDF["fitness"] = np.array(fitnessValues)
            populationAndFitnessDF = populationAndFitnessDF.sort_values(by=['fitness'])
        
        self.queue.put(populationAndFitnessDF)
        
    def getPopulation(self,population_size,num_genes,num_jobs,machineSequences,processingTimes):
        #generate initial random population
        population_list=[]
    
        for i in range(population_size):
            # generate a random permutation of 0 to num_job*num_mc-1
            nxm_random_num = list(np.random.permutation(num_genes)) 
    
            # add to the population_list
            population_list.append(nxm_random_num)
    
            for j in range(num_genes):
                # convert to job number format, every job appears m times
                population_list[i][j] = population_list[i][j] % num_jobs
            
        return population_list
    
    def elaborateFitness(self,population,num_jobs,machineSequences,processingTimes):
        fitnessArray = list()
        population_len = len(population)
        for i in range(population_len):
            individual = population[i]
            result = self.elaborateIndividualFitness(individual,num_jobs,machineSequences,processingTimes)
            fitness = result[0]
            individual = result[1]
            population[i] = individual
            
            fitnessArray.append(fitness)
                
        return fitnessArray
    
    def elaborateIndividualFitness(self,individual,num_jobs,machineSequences,processingTimes,debug = False):            
        fitnessValue = 0
        
        operationNumberArray = np.zeros(num_jobs)
        machineSchedules = list()
        jobTimings = list()
        jobNumberOfOperationsInIndividual = list()
        
        for i in machineSequences[0]:
            machineSchedules.append([])
            
        for j in processingTimes:
            jobTimings.append([])
            jobNumberOfOperationsInIndividual.append(0)
            
        #count the number of operations for each job, and register it
        jobIndex = 0
        listOfLessThan = []
        listOfGreaterThan = []
        for jobTime in processingTimes:
            numberOfOperationsForJob = len(jobTime)
            jobNumberOfOperationsInIndividual[jobIndex] = list(individual).count(jobIndex)
            differenceNumOfOpAndCurrentNumOfOp = abs(numberOfOperationsForJob - jobNumberOfOperationsInIndividual[jobIndex])
            
            if jobNumberOfOperationsInIndividual[jobIndex] < numberOfOperationsForJob:
                for jobIndexOperation in range(differenceNumOfOpAndCurrentNumOfOp):
                    listOfLessThan.append(jobIndex)
            elif jobNumberOfOperationsInIndividual[jobIndex] > numberOfOperationsForJob:
                for jobIndexOperation in range(differenceNumOfOpAndCurrentNumOfOp):
                    listOfGreaterThan.append(jobIndex)
                    
            jobIndex = jobIndex + 1
        
        iterationNumber = 0
        for greaterThanOperation in listOfGreaterThan:
            greaterThanOperationIndex = list(individual).index(greaterThanOperation)
            individual[greaterThanOperationIndex] = listOfLessThan[iterationNumber]
            iterationNumber = iterationNumber + 1
    
        for value in individual:            
            currentJobCounter = int(operationNumberArray[value])
            jobDuration = processingTimes[value][currentJobCounter]
            machineOfOperation = machineSequences[value][currentJobCounter]
            
            # A JOB TIMING ELEMENT IS THE OPERATION END OF EXECUTION TIME
            
            # WE NEED TO CALCULATE THE STARTING TIME OF THE CURRENT JOB.
            
            # THE CURRENT OPERATION START TIME IS THE LAST ELEMENT OPERATION END TIME 
            # IN THE MACHINE WHERE THE JOB IS EXECUTED
            
            # for the machine where the operation (machineOperation) is executed 
            # get the last JOB id ([-1][0]) index 0 is the value of the ID of the job
                    
            if len(machineSchedules[machineOfOperation]) > 0:
                lastJobValueInMachine = machineSchedules[machineOfOperation][-1][0]
                operationNumber = machineSchedules[machineOfOperation][-1][1]
                currentOperationStartingTime = jobTimings[lastJobValueInMachine][operationNumber][1]
            else:
                currentOperationStartingTime = 0
                
            # if the starting time of the new operation belonging to job J is earlier than 
            # the finish time of the last operation on job J the schedule is invalid
            # must be readjusted, in particular the starting time must be postponed
            # by the difference among the finishing time of the last time in the schedule 
            # and the current operation starting time
            
            if len(jobTimings[value]) > 0:
                lastJobFinishingTime = jobTimings[value][-1][1]
                        
                if currentOperationStartingTime < lastJobFinishingTime:
                    lastOpEndMinusCurrJobStartTime = (lastJobFinishingTime - currentOperationStartingTime)
                    currentOperationStartingTime = currentOperationStartingTime + lastOpEndMinusCurrJobStartTime + 1
                
                 
            #IN THIS CASE COMPARE THIS STARTING TIME WITH THE LAST ELEMENT VALUE OF THE JOB TIMINGS ARRAY,
            #IN OTHER WORDS IS THE STARTING TIME OF THE NEW OPERATION IN THE JOB HIGHER OR EQUAL THAN THE ENDING
            #TIME OF THE LAST ONE CONSIDERED?
                 
            currentOperationEndingTime = currentOperationStartingTime + jobDuration
            
            # ADD CURRENT_JOB_ENDING_TIME TO THE JOB TIMINGS ARRAY RELATED TO THE JOB
            jobTimings[value].append([currentOperationStartingTime,currentOperationEndingTime])
            fitnessValue = max(fitnessValue,currentOperationEndingTime)
            
            machineOfOperation = machineSequences[value][currentJobCounter]
            machineSchedules[machineOfOperation].append([value,currentJobCounter])
            operationNumberArray[value] = operationNumberArray[value] + 1
            
        return [fitnessValue,individual,machineSchedules,jobTimings]

