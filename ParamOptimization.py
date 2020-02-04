import GPyOpt
from GPyOpt.util.general import best_value
import GPy
import numpy as np
import logging

from SignalTemporalLogic.STLFactory import STLFactory

from GeneticSpec.Trajectory import Trajectory


class ParamOptimization:
    def __init__(self):
        self.time = None
        self.variables  = []
        self.atTime  = None


    def optimizeGenerationParameters(self, pop, variables, time, positiveTrainSet, negativeTrainSet, positiveTestSet,
                                     negativeTestSet, atTime, genOps, showGraphs=False):

        self.time = time
        self.atTime  = atTime
        self.variables = variables
        self.paramDict = pop.paramDict
        self.varDict = pop.varDict

        stFac = STLFactory()
        f1 = "G[10,30](x>30)"
        formula = stFac.constructFormulaTree(f1)

        # get params from formula to optimize
        params = formula.getAllParams()

        # make bounds for params & domain object
        pbounds = []
        mins = []
        domain = []
        for i in range(len(params)):
            if params[i] == "tl" or params[i] == "tu":
                pbounds.append((genOps.min_time_bound, genOps.max_time_bound))
                mins.append((genOps.min_time_bound))

                dct = {'name': params[i], 'type': 'continuous', 'domain': (genOps.min_time_bound, genOps.max_time_bound), 'dimensionality': 1}
                domain.append(dct)
            else:
                v = self.varDict[params[i]]
                pbounds.append((v[0], v[1]))
                mins.append((v[0]))

                dct = {'name': params[i], 'type': 'continuous', 'domain': (v[0],v[1]), 'dimensionality': 1}
                domain.append(dct)

        input_dim = len(params)

        #construct objective function object
        objFunc = objectiveFunction(formula, positiveTrainSet, negativeTrainSet, time, atTime, variables, self.paramDict, input_dim, mins, pbounds)

        bayesOpt = GPyOpt.methods.BayesianOptimization(f=objFunc.f,  # Objective function
                                                     domain=domain,  # Box-constraints of the problem
                                                     initial_design_numdata=5,  # Number data initial design
                                                     acquisition_type='EI',  # EI, LCB or MPI
                                                     maximize=True,
                                                     exact_feval=False)  # True evaluations, no sample noise

        bayesOpt.run_optimization(max_iter=20, eps=0)
        bestParams = (bayesOpt.x_opt).tolist()
        bestScore = min(bayesOpt.Y_best)
        if showGraphs == True:
            logging.info("Optimization Results - Best Params " + str(bestParams) + " Best Score " + str(-bestScore))
            #bayesOpt.plot_convergence()




class objectiveFunction():
    def __init__(self, formula, positiveTrainSet, negativeTrainSet, time, atTime, variables, paramDict, input_dim, mins, bounds=None):
        self.formula = formula
        self.positiveTrainSet = positiveTrainSet
        self.negativeTrainSet = negativeTrainSet
        self.time = time
        self.variables = variables
        self.paramDict = paramDict
        self.atTime = atTime
        self.bounds = bounds #[(-10,10)]
        self.min = mins  # [(0)] * input_dim
        self.fmin = -10000
        self.input_dim = input_dim
        self.sd = 0


    def f(self, X):
        params =  []
        for i in range(X.size):
            params.append(X.item(i))

        self.formula.updateParams(params)

        val1Mean, val1Var = self.computeRobustness(self.positiveTrainSet, self.formula)
        val2Mean, val2Var = self.computeRobustness(self.negativeTrainSet, self.formula)

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

