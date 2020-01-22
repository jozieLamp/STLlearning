
from SignalTemporalLogic.STLFactory import STLFactory
import random
#from scikit import BayesianOptimization as BO
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from bayes_opt import BayesianOptimization
from bayes_opt import UtilityFunction
from GeneticOptions import GeneticOptions
from GeneticSpec.Trajectory import Trajectory

#Generates different genetic population sets, mainly used for Genetic Population
class GeneticGenerator:
    def __init__(self):
        self.time = None
        self.positiveTrainSet = None
        self.negativeTrainSet = None
        self.formula = None
        self.variables = None
        self.atTime = None
        self.formulaBounds = None
        self.lb = None
        self.ub = None
        pass

    #returns Genetic Population
    def optimizeGenerationParameters(self, pop, variables, time, positiveTrainSet, negativeTrainSet, positiveTestSet, negativeTestSet, atTime, genOps):
        rankFormulae = []
        rankParameters = []
        rankScore = []

        #for loop to go through  all formulas in pop
        # for i in range(len(pop.population)):
        #     formula = pop.population[i]

        # formula  = pop.population[0]
        formula = "G[0,900](x > 40 & y < 80)\n"
        stlFac = STLFactory()
        formula =  stlFac.constructFormulaTree(formula)

        self.computeAverageMultiTrajectory(time, positiveTrainSet, negativeTrainSet, variables, atTime, pop.paramDict, formula)

    #returns list of new optimized params
    def computeAverageMultiTrajectory(self, time, positiveTrainSet, negativeTrainSet, variables, atTime, paramDict, formula):
        formulaVars = formula.getAllVars() #get vars in formula
        formulaBounds = formula.getAllTimebounds() #get all timebounds in formula
        timeLB = [float(b.lowerBound) for b in formulaBounds]
        timeUB = [float(b.upperBound) for b in formulaBounds]
        varLB = []
        varUB =  []
        for x in formulaVars:
            b = paramDict.get(x.toString())
            varLB.append(float(b[0]))
            varUB.append(float(b[1]))
        #make list  of all  lower bounds and all upper bounds
        lb = []
        lb.extend(timeLB)
        lb.extend(varLB)
        ub = []
        ub.extend(timeUB)
        ub.extend(varUB)

        #update private variables
        self.time = time
        self.positiveTrainSet = positiveTrainSet
        self.negativeTrainSet = negativeTrainSet
        self.formula = formula
        self.variables= variables
        self.atTime = atTime
        self.lb = lb
        self.ub = ub

        point = []

        val1Mean, val1Var = self.computeRobustness(self.positiveTrainSet, self.time, self.atTime, point, self.variables, formula)
        val2Mean, val2Var = self.computeRobustness(self.negativeTrainSet, self.time, self.atTime, point, self.variables, formula)

        print("val1", val1Mean, "val2", val2Mean)

        #GP-UCB Param Optimization
        # optimizer = BayesianOptimization(
        #     f=self.objectiveFunction,
        #     pbounds={'x': (0, 80), 'y': (0, 45)},
        #     verbose=2,
        #     random_state=1,
        # )
        #
        # optimizer.maximize(
        #     init_points=2,
        #     n_iter=3,
        # )
        # print(optimizer.max)

        # utility = UtilityFunction(kind="ucb", kappa=2.5, xi=0.0)
        #
        # for _ in range(5):
        #     next_point = optimizer.suggest(utility)
        #     target = self.objectiveFunction(**next_point, time, positiveTrainSet, negativeTrainSet, formula, variables, atTime, formulaBounds, lb, ub)
        #     optimizer.register(params=next_point, target=target)
        #
        #     print(target, next_point)
        # print(optimizer.max)

    # TODO here, need to fix value calculation
    # More robust when value higher
    def computeRobustness(self, trainSet, time, atTime, point, variables, formula):

        rVals = []
        #loop through train set and calculate robustness for each variable
        for i in trainSet:  # i is 2d array of values for each var
            #print(i)
            traj = Trajectory(i, time, point, variables, values=[0,0,0,0])
            rVals.append(formula.evaluateRobustness(traj, atTime))

        print("rvals", rVals)

        mean = sum(rVals) / len(rVals)
        variance = np.var(rVals)

        return mean, variance #return two doubles



    def objectiveFunction(self, point):
        formulaBoundsList = self.formula.getAllTimeboundsList()

        for i in range(0,2,len(formulaBoundsList)):
            point[i+1] = point[i] + point[i + 1] * (1 - point[i])

        p = point #array of point copy
        l = list(range(0, len(point)))

        newList = []
        for i in l:
            x = self.lb[i] + p[i] * (self.ub[i] - self.lb[i])
            newList.append(x)

        point = newList

        #TODO - complete this part with robustness

        value1 = self.computeRobustness(self.time, self.positiveTrainSet, self.variables, self.formula, point, self.atTime)
        value2 = self.computeRobustness(self.time, self.negativeTrainSet, self.variables, self.formula, point, self.atTime)

        abs = self.discriminationFunction(value1, value2)

        if abs == None:
            return 0
        else:
            return abs






    def discriminationFunction(self, x, y): #list x and y
        return (x[0]-y[0]) / abs(x[1] + y[1])









    #Grid sampler class
    #for time bounds, returns 2D list
    def sampleTime(self, n, lbounds, ubounds, formulaBounds):
        #n rows and m  columns, [[0] * m for i in range(n)]
        res = [[0] * len(lbounds) for i in range(n)]

        for i in range(0,n):
            for j in range(0, 2, len(formulaBounds)):
                res[i][j] = lbounds[j] + random.uniform(0,1) * (ubounds[j] - lbounds[j])

                res[i][j+1] = res[i][j] + random.uniform(0,1) * (ubounds[j] - res[i][j])

            for j in range(len(formulaBounds), len(res[i])):
                res[i][j] = lbounds[j] + random.uniform(0,1) * (ubounds[j] - lbounds[j])

        return res

    def sampleVars(self, n, params):#takes list of params
        pass
        #return new double [0][]

