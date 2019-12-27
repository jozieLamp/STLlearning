import logging
from FormulaSpec import Formula
import random
#from scikit import BayesianOptimization as BO
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from bayes_opt import BayesianOptimization
from GeneticOptions import GeneticOptions

#Generates different genetic population sets, mainly used for Genetic Population
class GeneticGenerator:
    def __init__(self):
        pass

    #returns Genetic Population
    def optimizeGenerationParameters(self, pop, variables, time, positiveTrainSet, negativeTrainSet, positiveTestSet, negativeTestSet, atTime, paramDict, genOps):
        rankFormulae = []
        rankParameters = []
        rankScore = []

        for i in range(len(pop.population)):
            formula = pop.population[i]

            #gpucb
            #logging.info("OPTIMIZE PARAMETER OF FORMULA " + formula.toString())
            #fitness function = private static final BiFunction<double[], double[], Double> DISCRIMINATION_FUNCTION = (x, y) -> (x[0] - y[0]) / (Math.abs(x[1] + y[1]));
            self.computeAverageMultiTrajectory(35, variables, time, positiveTrainSet, negativeTrainSet, formula, pop, atTime, paramDict, genOps)

        #return genetic pop


    #returns an array of doubles
    #original header from java
        #normal model pos train set ineff model neg train set
    #int maxIterations, BiFunction<double[], double[], Double> fitness, String[] variablesUnique, double[] ds2Times, double[][][] normal_model, double[][][] ineffective_model, Formula formula, FormulaPopulation pop, double[] timeBoundsFormula, double atTime)
    def computeAverageMultiTrajectory(self, maxIters, variablesUnique, time, positiveTrainSet, negativeTrainSet, formula, pop, atTime, paramDict, genOps):
        variables = formula.paramList

        #Get list of bounds of time
        timeLB = []
        timeUB = []

        #if advanced formula, need to iterate through temporal operator list and get all time bounds
        if isinstance(formula, Formula.AdvancedFormula):
            numTimeBounds = 0
            for op in formula.temporalOperator:
                numTimeBounds += 1
        else:
            numTimeBounds = 2

        #keep track of min and max time bound for each timebound
        for i in range(numTimeBounds):
            timeLB.append(genOps.min_time_bound)
            timeUB.append(genOps.max_time_bound)

        #Get list of bounds of variable params
        varLB = []
        varUB = []
        for v in variables:
            varBounds = paramDict[v.name]
            varLB.append(varBounds[0])
            varUB.append(varBounds[1])

        #Make list of all lb and ub for the params (time values and variable values)
        paramLB = timeLB + varLB
        paramUB = timeUB + varUB
        numParams = len(variables) + numTimeBounds #equivalent to the number of params, used for point size

        #ObjFunction part
        #takes list of double point
        #not sure where these numbers come from for point,
        # right now I am initializing them to random num btw 0 and 1 for num of params
        point = []
        for i in range(numParams):
            point.append(random.uniform(0,1))

        for i in range(0,numTimeBounds,2):
            point[i + 1] = point[i] + point[i + 1] * (1 - point[i])

        newPoint = []
        for i in range(len(point)):
            newPoint.append(paramLB[i] + point[i] * (paramUB[i] - paramLB[i]))

        #TODO compute robustness for positive train set and negative train set
        posRobustness = self.computeRobustness(time, positiveTrainSet, variablesUnique, formula, point, atTime)
        negRobustness = self.computeRobustness(time, negativeTrainSet, variablesUnique, formula, point, atTime)


        # double[] value1 = computeAverageRobustnessMultiTrajectory(ds2Times, normal_model, variablesUnique, formula, point, atTime);
        # double[] value2 = computeAverageRobustnessMultiTrajectory(ds2Times, ineffective_model, variablesUnique, formula, point, atTime);
        # double abs = fitness.apply(value1, value2);
        # if (Double.isNaN(abs)) {
        # return 0;
        # }
        # return abs;


    # find parameters that have the best robustness - implementation of GP UCB algorithm
    def computeRobustness(self):
        DiscrmFuncVal = GeneticOptions.discriminationFunction(x=, y=)
        BayesianOptimization



    # #find parameters that have the best robustness  -  implementation of GP UCB algorithm
    # def computeRobustness(self, time, data, variablesUnique, formula, point, atTime):
    #
    #     #evaluate value for globally
    #     minVal = 99999999999999
    #     t1 = formula.temporalOperator.lowerBound + atTime
    #     t2 = formula.temporalOperator.upperBound + atTime
    #
    #     #time index after
    #     timeIndexAfter = None
    #     for i in range(len(time)):
    #         if time[i] >= t1:
    #             timeIndexAfter = i
    #     timeIndexAfter = len(time)-1
    #
    #     timeIndexUntil = None
    #     for i in range(len(time)):
    #         if time[i] > t2:
    #             timeIndexUntil = i - 1
    #         elif time[i]==t2:
    #             timeIndexUntil = i
    #     timeIndexUntil = len(time) - 1
    #
    #     if (timeIndexAfter > timeIndexUntil or t1 == t2):
    #         #TODO
    #         pass
    #         #return formula.evaluateValue(x, times[index2]);
    #
    #     #do this for all instances of x variable occurrence??
    #     for i in range(timeIndexAfter, timeIndexUntil):
    #         #gets value of actual x val, stored in original variable storage and predicted param value of x in formula
    #
    #         #double value = formula.evaluateValue(x, times[i]);
    #             #value = Math.abs(value2 - value1); # this is x actual val - predicted val
    #             #depending on what sign used, return value  or - value
    #
    #         # if value  <  minVal:
    #         #     minVal = value
    #         pass
    #
    #
    #     return minVal
