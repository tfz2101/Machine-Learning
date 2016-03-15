import sys
import os
import time


import java.util.Random as Random

import dist.DiscreteDependencyTree as DiscreteDependencyTree
import dist.DiscreteUniformDistribution as DiscreteUniformDistribution
import opt.prob.GenericProbabilisticOptimizationProblem as GenericProbabilisticOptimizationProblem
import opt.prob.MIMIC as MIMIC
import shared.FixedIterationTrainer as FixedIterationTrainer
import opt.example.KnapsackEvaluationFunction as KnapsackEvaluationFunction
from array import array
import opt.example.CountOnesEvaluationFunction as CountOnesEvaluationFunction
import dist.DiscreteUniformDistribution as DiscreteUniformDistribution
import dist.Distribution as Distribution
import opt.DiscreteChangeOneNeighbor as DiscreteChangeOneNeighbor
import opt.EvaluationFunction as EvaluationFunction
import opt.GenericHillClimbingProblem as GenericHillClimbingProblem
import opt.ga.SingleCrossOver as SingleCrossOver
import opt.ga.DiscreteChangeOneMutation as DiscreteChangeOneMutation
import opt.ga.GenericGeneticAlgorithmProblem as GenericGeneticAlgorithmProblem
import opt.example.FourPeaksEvaluationFunction as FourPeaksEvaluationFunction


# Random number generator */
random = Random()


#KNAPSACK-----------------------------------------------------

# The number of items
NUM_ITEMS = 3
# The number of copies each
COPIES_EACH = 14

# create copies
#fill = [COPIES_EACH] * NUM_ITEMS
fill =[13,4,6]
copies = array('i', fill)

# create weights and volumes
fill = [0] * NUM_ITEMS
weights = array('d', fill)
volumes = array('d', fill)
weights[0]=2
weights[1]=4
weights[2]=1
volumes[0]=1
volumes[1]=3
volumes[2]=2

# The volume of the knapsack 
#KNAPSACK_VOLUME = MAX_VOLUME * NUM_ITEMS * COPIES_EACH * .4
KNAPSACK_VOLUME = 13

# create range
#fill = [COPIES_EACH + 1] * NUM_ITEMS
fill = [14,5,7] 
ranges = array('i', fill)

#print(weights)
#print(volumes)
#print(KNAPSACK_VOLUME)
#print(copies)
#print(ranges)

ef = KnapsackEvaluationFunction(weights, volumes, KNAPSACK_VOLUME, copies)
output_ks = [0,0,0]
cur_fit = 0
countIter = []
errs = []
GO = 26
opt = 0
times = []
countIter = []
for l in range(0,1000):
    odd = DiscreteUniformDistribution(ranges)
    df = DiscreteDependencyTree(.1, ranges)
    pop = GenericProbabilisticOptimizationProblem(ef, odd, df)
    s = 200
    opt = 0
    counter = 0
    s1 = time.time()
    while opt != GO:
        mimic = MIMIC(s,s/2, pop)
        counter = counter + 1
        #fit = FixedIterationTrainer(mimic, 1)
        #avg  = fit.train()
        output = mimic.getOptimal()
        opt = ef.value(output)
    countIter.append(s*counter)
    s2 = time.time()
    times.append((s2-s1))
print(countIter)
print(sum(countIter)/len(countIter))
print(times)
print(sum(times)/len(times))


#Count Ones-----------------------------------------------------
'''
N=9
fill = [2] * N
ranges = array('i', fill)

ef = CountOnesEvaluationFunction()

countIter = []
errs = []
GO = N
opt = 0
countIter = []
times = []
for l in range(0,1000):
    odd = DiscreteUniformDistribution(ranges)
    df = DiscreteDependencyTree(.1, ranges)
    pop = GenericProbabilisticOptimizationProblem(ef, odd, df)
    s = 100
    opt = 0
    counter = 0
    s1 = time.time()
    while opt != GO:
        mimic = MIMIC(s, s/2, pop)
        counter = counter + 1
        #fit = FixedIterationTrainer(mimic, 100)
        #fit.train()
        output = mimic.getOptimal()
        opt = ef.value(output)
    s2 = time.time()
    times.append((s2-s1))
    countIter.append(s*counter)
print(countIter)
print(sum(countIter)/len(countIter))        
print(times)
print(sum(times)/len(times))
'''

#FOUR PEAKS---------------------------------------------------
'''
N=10
T=2
fill = [2] * N
ranges = array('i', fill)

ef = FourPeaksEvaluationFunction(T)

countIter = []
errs = []
GO = N + N -(T+1)
opt = 0
times = []
countIter = []
for l in range(0,1000):
    odd = DiscreteUniformDistribution(ranges)
    df = DiscreteDependencyTree(.1, ranges)
    pop = GenericProbabilisticOptimizationProblem(ef, odd, df)
    s = 100
    opt = 0
    counter = 0
    s1 = time.time()
    while opt != GO:
        mimic = MIMIC(s, s/2, pop)
        counter = counter+1
        #fit = FixedIterationTrainer(mimic, 1000)
        #fit.train()
        output = mimic.getOptimal()
        opt = ef.value(output)
        print(opt)
    countIter.append(s*counter)
    s2 = time.time()
    times.append((s2-s1))
print(countIter)
print(sum(countIter)/len(countIter))       
print(times)
print(sum(times)/len(times)) 

'''