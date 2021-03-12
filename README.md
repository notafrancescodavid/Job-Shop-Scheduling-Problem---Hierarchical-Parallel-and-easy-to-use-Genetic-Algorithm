# Job-Shop-Scheduling-Problem---Hierarchical-Parallel-and-easy-to-use-Genetic-Algorithm
This repository provides a solution to the Job Shop Scheduling Problem. The proposed algorithm runs parallel on multicore computers (and single-core) and gives as output a schedule as solution.

The algorithm is formed by a tree of smaller genetic algorithms which over generations pass the best solutions to the children till the root that gets the best results. The Job Shop Scheduling Problem is NP-Hard. And requires optimization algorithms like the one implemented in this repository to obtain pseudo-optimal solutions.

<p align="center">
  <img src="https://github.com/notafrancescodavid/Job-Shop-Scheduling-Problem---Hierarchical-Parallel-and-easy-to-use-Genetic-Algorithm/blob/cc3d9dca809b5f13788536771d1c1b817bb70c13/img/tree_structure.png" width="350" title="hover text">
</p>

## Getting Started

Clone the repository, then launch the following command from the terminal:

```
python PATH_TO_REP/main.py PATH_TO_REP/instances/la21 400 400 8 plot_to_file PATH_TO_REPOSITORY/schedules/la21.png
```

You should see a similar result in the folder "schedules":

<p align="center">
  <img src="https://github.com/notafrancescodavid/Job-Shop-Scheduling-Problem---Hierarchical-Parallel-and-easy-to-use-Genetic-Algorithm/blob/08df9a023174c2b93d2993f69958ed82be7fa549/schedules/la21.png" title="hover text">
</p>

### Prerequisites

You need:
- pandas
- numpy
- matplotlib

You can install them by installing Anaconda, or if you prefer there are plenty of guides online that explain how to install them

### How to use the algorithm:
The algorithm can be used from source code or from the command line:

From source code
```
from treeGA import TreeGA

fileInstanceName = PATH_TO_REP/instances/INPUT_INSTANCE

# typical parameters values are: 
#     populationNumber = 400, iterationNumber = 400, numberThatIsAPowerOfTwo = 8
#     populationNumber = 800, iterationNumber = 800, numberThatIsAPowerOfTwo = 8
#     populationNumber = 1600, iterationNumber = 1600, numberThatIsAPowerOfTwo = 16
#     populationNumber = 1600, iterationNumber = 1600, numberThatIsAPowerOfTwo = 32

populationNumber = POPULATION_NUM
iterationNumber = ITERATION_NUM
numberThatIsAPowerOfTwo = NUM_OF_STARTING_ALGORITHMS

treeGA = TreeGA(fileName = fileInstanceName,populationNumber = populationNumber,iterationNumber = iterationNumber,numberThatIsAPowerOfTwo = numberThatIsAPowerOfTwo)
treeGA.execute()

minimumMakespan = treeGA.getMinimumMakespan()
bestSolution = treeGA.getBestSolution()
bestMachineSchedules = treeGA.getBestSolutionMachineSchedules()
bestJobTimings = treeGA.getBestSolutionJobTimings()

# THE MAKESPAN IS THE TIME THE ENTIRE SCHEDULE NEEDS TO BE RUN, THE LOWER IT IS THE BETTER THE RESULT
print("Minimum Makespan:")
print(minimumMakespan)

# TO SEE HOW TO CONVERT A SOLUTION INTO A CHART, SEE main.py
print("Best solution")
print(bestSolution.values)
```

Or you can use it from command line
```
python PATH_TO_REP/main.py PATH_TO_REP/instances/INPUT_INSTANCE POPULATION_NUM ITERATION_NUM NUM_OF_STARTING_ALGORITHMS ATTR_PLOT PATH_TO_REP/schedules/INPUT_INSTANCE.png
```
Where:
- PATH_TO_REP, (mandatory): is the path where you located this repository on your file system.
- INPUT_INSTANCE, (mandatory): is the file where the input data to the algorithm is stored. Later I will show an example of file input structure
- POPULATION_NUM, (mandatory): is the number of population for the algorithm with maximum number of "individuals" which in terms of genetic algorithms are potential solutions.
- ITERATION_NUM, (mandatory): is the number of iterations the algorithm does to find a pseudo-optimal solution
- NUM_OF_STARTING_ALGORITHMS, (mandatory): this algorithm is actually a tree of smaller algorithms. This attribute MUST BE A POWER OF 2. because the tree of algorithms is binary
- ATTR_PLOT, (optional): can assume two values "plot" or "plot_to_file". If the first is chosen a plot of the result is shown. The second requires to specify the path where the schedule result is stored as an image
- PATH_TO_REP/schedules/INPUT_INSTANCE.png (required only if ATTR_PLOT is "plot_to_file"), it is the path where the image of the result is stored.

IN BOTH CASES (FROM CODE OR COMMAND LINE) IT IS NEEDED TO USE A FILE AS INPUT.

### Input file structure
To understand the structure that the input file MUST have let's see an example (you can find this example in /instances/la21)
```
15 10
2 34 3 55 5 95 9 16 4 21 6 71 0 53 8 52 1 21 7 26
3 39 2 31 0 12 1 42 9 79 8 77 6 77 5 98 4 55 7 66
1 19 0 83 3 34 4 92 6 54 9 79 8 62 5 37 2 64 7 43
4 60 2 87 8 24 5 77 3 69 7 38 1 87 6 41 9 83 0 93
8 79 9 77 2 98 4 96 3 17 0 44 7 43 6 75 1 49 5 25
8 35 7 95 6  9 9 10 2 35 1  7 5 28 4 61 0 95 3 76
4 28 5 59 3 16 9 43 0 46 8 50 6 52 7 27 2 59 1 91
5  9 4 20 2 39 6 54 1 45 7 71 0 87 3 41 9 43 8 14
1 28 5 33 0 78 3 26 2 37 7  8 8 66 6 89 9 42 4 33
2 94 5 84 6 78 9 81 1 74 3 27 8 69 0 69 7 45 4 96
1 31 4 24 0 20 2 17 9 25 8 81 5 76 3 87 7 32 6 18
5 28 9 97 0 58 4 45 6 76 3 99 2 23 1 72 8 90 7 86
5 27 9 48 8 27 7 62 4 98 6 67 3 48 0 42 1 46 2 17
1 12 8 50 0 80 2 50 9 80 3 19 5 28 6 63 4 94 7 98
4 61 3 55 6 37 5 14 2 50 8 79 1 41 9 72 7 18 0 75
```
15 is the number of jobs that have to be executed on the machines. Each job is formed by several tasks. Each task has a time of execution and is executed on a single machine.
10 is the number of machines

- The input matrix is 15x10, but every element of the matrix is actually a task represented by a couple of elements. For example element [0][0] is (2,34) or element [1][1] is (2,31).
- The first number of the couple (in the examples is 2) represents the ID of the machine where the task runs, in fact by seeing the example above this number goes from 0 to 9 (that is 10 machines uniques IDs).
- The second number is the time the task that runs on the machine. In the example a task, represented by the index [0][0] belonging to the first job, runs on machine 2 and requires 34 minutes.

YOU MUST FOLLOW THE SAME INPUT SHAPE AND FILE STRUCTURE, OR CHANGE THE SOURCE CODE IN TreeGA CLASS IF YOU PREFER.

### Running tests on some benchmark input data
Examples of input files can be found under the "instances" directory. The instances.json has the list of all benchmark for the input files that can be used to test the algorithm. The benchmarks of the pseudo-optimal values ever obtained by other algorithms are available in this file.
Run some examples using input files under "instances" and compare the benchmark (available in instances.json) with this algorithm to have an idea of how close it goes to optimal values.
 
## Authors

* **Francesco David Nota**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
