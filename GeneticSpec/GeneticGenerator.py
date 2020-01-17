
from SignalTemporalLogic.STLFactory import STLFactory
import random

#Generates different genetic population sets, mainly used for Genetic Population
class GeneticGenerator:
    def __init__(self):
        pass

    #returns Genetic Population
    def optimizeGenerationParameters(self, pop, variables, time, positiveTrainSet, negativeTrainSet, positiveTestSet, negativeTestSet, atTime, genOps):
        rankFormulae = []
        rankParameters = []
        rankScore = []

        #for loop to go through  all formulas in pop

        # formula  = pop.population[0]
        formula = "G[0,900](x > 20 & y < 30)"
        stlFac = STLFactory()
        formula =  stlFac.constructFormulaTree(formula)

        self.computeAverageMultiTrajectory(variables, pop.paramDict, formula)


    def computeAverageMultiTrajectory(self, allVariables, paramDict, formula):
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



    def objectiveFunction(self, point, formulaBounds, lb, ub):
        for i in range(0,2,len(formulaBounds)-1):
            point[i+1] = point[i] + point[i + 1] * (1 - point[i])

        p = point #array of point copy
        l = list(range(0, len(point)))

        newList = []
        for i in l:
            x = lb[i] + p[i] * (ub[i] - lb[i])
            newList.append(x)

        point = newList

        #TODO - conplete this part with robustness
        value1 = self.computeRobustness()
        value2 = self.computeRobustness()

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

    #TODO here
    def computeRobustness(self):
        pass

