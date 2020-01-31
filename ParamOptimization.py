import numpy as np
from GeneticSpec.Trajectory import Trajectory
from GeneticSpec.GeneticPopulation import GeneticPopulation
from GeneticSpec.GeneticPopulation import Score
import logging


class ParamOptimization:
    def __init__(self):
        pass


    def optimizeGenerationParameters(self, pop, variables, time, positiveTrainSet, negativeTrainSet, positiveTestSet,
                                     negativeTestSet, atTime, genOps):
        rankFormulae = []
        rankParams = []
        rankScores = []

        # for loop to go through  all formulas in pop
        for i in range(20):  # len(pop.population)):
            formula = pop.population[i]

            # update private variables
            self.time = time
            self.positiveTrainSet = positiveTrainSet
            self.negativeTrainSet = negativeTrainSet
            self.formula = formula
            self.variables = variables
            self.atTime = atTime
            self.paramDict = pop.paramDict

            # array of best params for formula
            bestParams = self.computeNewParams(self.formula, genOps, pop.varDict)
            # update formula params
            formula.updateParams(bestParams)


    def computeNewParams(self, formula, genOps, varDict):
        # get params from formula to optimize
        params = formula.getAllParams()
        print(params)


    def objectiveFunction3(self, p0, p1, p2):
        #first construct formula with new bounds
        params = [p0, p1, p2]
        self.formula.updateParams(params)

        val1Mean, val1Var = self.computeRobustness(self.positiveTrainSet, self.formula)
        val2Mean, val2Var = self.computeRobustness(self.negativeTrainSet,self.formula)

        abs = self.discriminationFunction(val1Mean, val1Var, val2Mean, val2Var)

        return abs


    # More robust when value higher
    def computeRobustness(self, trainSet, formula):

        rVals = []
        # loop through train set and calculate robustness for each variable
        for i in trainSet:  # i is 2d array of values for each var
            # print(i)
            traj = Trajectory(trajectories=i, time=self.time, variables=self.variables, paramDict=self.paramDict,
                              values=[0, 0, 0, 0])
            rVals.append(formula.evaluateRobustness(traj, self.atTime))

        mean = sum(rVals) / len(rVals)
        variance = np.std(rVals)

        return mean, variance  # return two doubles

    # Maximizes the difference between the average robustness of pos class, and the average robustness of negative class,
    # divided by the sum of the respective standard deviation
    def discriminationFunction(self, xMean, xVar, yMean, yVar):  # list x and y
        # return (xMean - yMean) / abs(xVar + yVar)

        vars = abs(xVar + yVar)
        if vars != 0:
            num = (xMean - yMean) / vars
        else:
            num = (xMean - yMean)

        if np.isnan(num):
            return 0
        else:
            return num