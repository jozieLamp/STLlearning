
from SignalTemporalLogic.STLFactory import STLFactory
import random
import numpy as np
from GeneticOptions import GeneticOptions
from GeneticSpec.Trajectory import Trajectory
from GeneticSpec.GeneticPopulation import GeneticPopulation
from GeneticSpec.GeneticPopulation import Score
import logging

#from skopt import gp_minimize
# import GPy
# import GPyOpt
# from GPyOpt.methods import BayesianOptimization

from bayes_opt import BayesianOptimization
from bayes_opt import UtilityFunction

#Generates different genetic population sets, mainly used for Genetic Population
class GeneticGenerator:
    def __init__(self):
        self.time = None
        self.positiveTrainSet = None
        self.negativeTrainSet = None
        self.formula = None
        self.variables = None
        self.atTime = None
        self.paramDict = None


    #returns Genetic Population
    def optimizeGenerationParameters(self, pop, variables, time, positiveTrainSet, negativeTrainSet, positiveTestSet, negativeTestSet, atTime, genOps):
        rankFormulae = []
        rankParams = []
        rankScores = []

        #for loop to go through  all formulas in pop
        for i in range(20):#len(pop.population)):
            formula = pop.population[i]

            # update private variables
            self.time = time
            self.positiveTrainSet = positiveTrainSet
            self.negativeTrainSet = negativeTrainSet
            self.formula = formula
            self.variables = variables
            self.atTime = atTime
            self.paramDict = pop.paramDict

            #array of best params for formula
            bestParams = self.computeNewParams(self.formula, genOps, pop.varDict)
            #update formula params
            formula.updateParams(bestParams)

            #get score, make score variable
            val1Mean, val1Var = self.computeRobustness(self.positiveTrainSet, formula)
            val2Mean, val2Var = self.computeRobustness(self.negativeTrainSet, formula)
            classDif = self.discriminationFunction(val1Mean, val1Var, val2Mean, val2Var)
            s = Score(val1Mean, val1Var, val2Mean, val2Var, classDif)

            #print(formula.toString(), s.toString())

            #add values to genetic pop lists
            rankFormulae.append(formula)
            rankParams.append(bestParams)
            rankScores.append(s)

        return GeneticPopulation(rankFormulae, rankParams, rankScores)


    def computeNewParams(self, formula, genOps, varDict):
        # get params from formula to optimize
        params = formula.getAllParams()

        # make bounds for params
        pbounds = {}
        for i in range(len(params)):
            if params[i] == "tl" or params[i] == "tu":
                pbounds["p" + str(i)] = (genOps.min_time_bound, genOps.max_time_bound)
            else:
                v = varDict[params[i]]
                pbounds["p" + str(i)] = (v[0], v[1])

        #print("PBOUNDS ", len(pbounds))

        #call bayes opt based on number of params in objective function
        newParams = []
        if len(pbounds) == 1:
            newParams = self.optimize(pbounds, self.objectiveFunction1)
        elif len(pbounds) == 2:
            newParams = self.optimize(pbounds, self.objectiveFunction2)
        elif len(pbounds) == 3:
            newParams = self.optimize(pbounds, self.objectiveFunction3)
        elif len(pbounds) == 4:
            newParams = self.optimize(pbounds, self.objectiveFunction4)
        elif len(pbounds) == 5:
            newParams = self.optimize(pbounds, self.objectiveFunction5)
        elif len(pbounds) == 6:
            newParams = self.optimize(pbounds, self.objectiveFunction6)
        elif len(pbounds) == 7:
            newParams = self.optimize(pbounds, self.objectiveFunction7)
        elif len(pbounds) == 8:
            newParams = self.optimize(pbounds, self.objectiveFunction8)
        elif len(pbounds) == 9:
            newParams = self.optimize(pbounds, self.objectiveFunction9)
        elif len(pbounds) == 10:
            newParams = self.optimize(pbounds, self.objectiveFunction10)
        else:
            logging.error("TOO MANY PARAMETERS IN OPTIMIZATION")

        #fix ordering of time params
        for i in range(len(params)):
            if params[i] == "tl":
                if newParams[i] > newParams[i+1]:
                    temp = newParams[i]
                    newParams[i] = newParams[i+1]
                    newParams[i+1] = temp

        #return list of new params
        return newParams


    #TODO - make this faster somehow?
    #returns best optimized set of params for formula given
    def optimize(self, pbounds, function, init_pts=2, n_iter=3):
        optimizer = BayesianOptimization(
            f=function,
            pbounds=pbounds,
            verbose=0,
            random_state=1,
        )

        optimizer.maximize(
            init_points=init_pts,
            n_iter=n_iter,
        )
        #print(optimizer.max)

        newParams = list(optimizer.max["params"].values())
        classDifference = optimizer.max["target"]
        # print(newParams)
        # print(classDifference)


        return newParams



    #Defining objective functions with different number of params
    def objectiveFunction1(self, p0):
        #first construct formula with new bounds
        params = [p0]
        self.formula.updateParams(params)

        val1Mean, val1Var = self.computeRobustness(self.positiveTrainSet, self.formula)
        val2Mean, val2Var = self.computeRobustness(self.negativeTrainSet,self.formula)

        abs = self.discriminationFunction(val1Mean, val1Var, val2Mean, val2Var)

        return abs

    def objectiveFunction2(self, p0, p1):
        #first construct formula with new bounds
        params = [p0, p1]
        self.formula.updateParams(params)

        val1Mean, val1Var = self.computeRobustness(self.positiveTrainSet, self.formula)
        val2Mean, val2Var = self.computeRobustness(self.negativeTrainSet,self.formula)

        abs = self.discriminationFunction(val1Mean, val1Var, val2Mean, val2Var)

        return abs

    def objectiveFunction3(self, p0, p1, p2):
        #first construct formula with new bounds
        params = [p0, p1, p2]
        self.formula.updateParams(params)

        val1Mean, val1Var = self.computeRobustness(self.positiveTrainSet, self.formula)
        val2Mean, val2Var = self.computeRobustness(self.negativeTrainSet,self.formula)

        abs = self.discriminationFunction(val1Mean, val1Var, val2Mean, val2Var)

        return abs

    def objectiveFunction4(self, p0, p1, p2, p3):
        #first construct formula with new bounds
        params = [p0, p1, p2, p3]
        self.formula.updateParams(params)

        val1Mean, val1Var = self.computeRobustness(self.positiveTrainSet, self.formula)
        val2Mean, val2Var = self.computeRobustness(self.negativeTrainSet,self.formula)

        abs = self.discriminationFunction(val1Mean, val1Var, val2Mean, val2Var)

        return abs

    def objectiveFunction5(self, p0, p1, p2, p3, p4):
        #first construct formula with new bounds
        params = [p0, p1, p2, p3, p4]
        self.formula.updateParams(params)

        val1Mean, val1Var = self.computeRobustness(self.positiveTrainSet, self.formula)
        val2Mean, val2Var = self.computeRobustness(self.negativeTrainSet,self.formula)

        abs = self.discriminationFunction(val1Mean, val1Var, val2Mean, val2Var)

        return abs

    def objectiveFunction6(self, p0, p1, p2, p3, p4, p5):
        #first construct formula with new bounds
        params = [p0, p1, p2, p3, p4, p5]
        self.formula.updateParams(params)

        val1Mean, val1Var = self.computeRobustness(self.positiveTrainSet, self.formula)
        val2Mean, val2Var = self.computeRobustness(self.negativeTrainSet,self.formula)

        abs = self.discriminationFunction(val1Mean, val1Var, val2Mean, val2Var)

        return abs

    def objectiveFunction7(self, p0, p1, p2, p3, p4, p5, p6):
        #first construct formula with new bounds
        params = [p0, p1, p2, p3, p4, p5, p6]
        self.formula.updateParams(params)

        val1Mean, val1Var = self.computeRobustness(self.positiveTrainSet, self.formula)
        val2Mean, val2Var = self.computeRobustness(self.negativeTrainSet,self.formula)

        abs = self.discriminationFunction(val1Mean, val1Var, val2Mean, val2Var)

        return abs

    def objectiveFunction8(self, p0, p1, p2, p3, p4, p5, p6, p7):
        #first construct formula with new bounds
        params = [p0, p1, p2, p3, p4, p5, p6, p7]
        self.formula.updateParams(params)

        val1Mean, val1Var = self.computeRobustness(self.positiveTrainSet, self.formula)
        val2Mean, val2Var = self.computeRobustness(self.negativeTrainSet,self.formula)

        abs = self.discriminationFunction(val1Mean, val1Var, val2Mean, val2Var)

        return abs

    def objectiveFunction9(self, p0, p1, p2, p3, p4, p5, p6, p7, p8):
        #first construct formula with new bounds
        params = [p0, p1, p2, p3, p4, p5, p6, p7, p8]
        self.formula.updateParams(params)

        val1Mean, val1Var = self.computeRobustness(self.positiveTrainSet, self.formula)
        val2Mean, val2Var = self.computeRobustness(self.negativeTrainSet,self.formula)

        abs = self.discriminationFunction(val1Mean, val1Var, val2Mean, val2Var)

        return abs

    def objectiveFunction10(self, p0, p1, p2, p3, p4, p5, p6, p7, p8, p9):
        #first construct formula with new bounds
        params = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9]
        self.formula.updateParams(params)

        val1Mean, val1Var = self.computeRobustness(self.positiveTrainSet, self.formula)
        val2Mean, val2Var = self.computeRobustness(self.negativeTrainSet,self.formula)

        abs = self.discriminationFunction(val1Mean, val1Var, val2Mean, val2Var)

        return abs

    # More robust when value higher
    def computeRobustness(self, trainSet, formula):

        rVals = []
        #loop through train set and calculate robustness for each variable
        for i in trainSet:  # i is 2d array of values for each var
            #print(i)
            traj = Trajectory(trajectories=i, time=self.time, variables=self.variables, paramDict=self.paramDict, values=[0,0,0,0])
            rVals.append(formula.evaluateRobustness(traj, self.atTime))

        mean = sum(rVals) / len(rVals)
        variance = np.std(rVals)

        return mean, variance #return two doubles


    #Maximizes the difference between the average robustness of pos class, and the average robustness of negative class,
    # divided by the sum of the respective standard deviation
    def discriminationFunction(self, xMean, xVar, yMean, yVar): #list x and y
        #return (xMean - yMean) / abs(xVar + yVar)

        vars = abs(xVar + yVar)
        if vars != 0:
            num = (xMean - yMean) / vars
        else:
            num = (xMean - yMean)

        if np.isnan(num):
            return 0
        else:
            return num


    # Calculate class + and - predictions
    def calculateClassPredictions(self, generation,labels, positiveTestSet, negativeTestSet, time, variables, paramDict):

        testSet =  np.zeros((positiveTestSet.shape[0]+negativeTestSet.shape[0], positiveTestSet.shape[1], positiveTestSet.shape[2]))

        for i in range(positiveTestSet.shape[0]):
            testSet[i, :, :] = positiveTestSet[i, :, :]

        posSz = positiveTestSet.shape[0]
        for i in range(negativeTestSet.shape[0]):
            testSet[posSz + i, :, :] = negativeTestSet[i, :, :]

        totalTrajectories = len(labels)

        for i in range(len(generation.rankFormulae)):
            f = generation.rankFormulae[i]
            posSum = self.calculateFinalScores(testSet, f, time, variables, paramDict)
            generation.rankScore[i].posClassPctg = posSum / totalTrajectories
            generation.rankScore[i].negClassPctg = (totalTrajectories - posSum) / totalTrajectories



    def calculateFinalScores(self, testSet, formula, time, variables, paramDict):
        posClassified = []
        for i in testSet:
            traj = Trajectory(trajectories=i, time=self.time, variables=self.variables, paramDict=self.paramDict, values=[0,0,0,0])
            if formula.evaluateValue(traj, self.atTime):
                posClassified.append(1)
            else:
                posClassified.append(0)

        posSum = sum(posClassified)
        return posSum


