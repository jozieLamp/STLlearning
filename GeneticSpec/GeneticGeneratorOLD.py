import random
#from scikit import BayesianOptimization as BO

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
        if isinstance(formula, FormulaOld.AdvancedFormula):
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

        #Initialize parameter values of formula
        point = []
        for i in range(numParams):
            point.append(random.uniform(0,1))

        #objective function
        # for i in range(0,numTimeBounds,2):
        #     point[i + 1] = point[i] + point[i + 1] * (1 - point[i])

        paramVals = []
        for i in range(len(point)):
            paramVals.append(paramLB[i] + point[i] * (paramUB[i] - paramLB[i]))

        print("point", paramVals)
        formula.printFormula()

        #TODO compute robustness for positive train set and negative train set
        posRobustness = self.computeRobustness(time, positiveTrainSet, variablesUnique, formula, paramVals, atTime)
        #negRobustness = self.computeRobustness(time, negativeTrainSet, variablesUnique, formula, point, atTime)


        # double[] value1 = computeAverageRobustnessMultiTrajectory(ds2Times, normal_model, variablesUnique, formula, point, atTime);
        # double[] value2 = computeAverageRobustnessMultiTrajectory(ds2Times, ineffective_model, variablesUnique, formula, point, atTime);
        # double abs = fitness.apply(value1, value2);
        # if (Double.isNaN(abs)) {
        # return 0;
        # }
        # return abs;

    # -  implementation of GP UCB algorithm
    def optimizeParams(self):
        pass
        #DiscrmFuncVal = GeneticOptions.discriminationFunction(x=, y=)

        #bo = BayesianOptimization(GeneticOptions.discriminationFunction(x=,y=))


    # # find parameters that have the best robustness - implementation of GP UCB algorithm
    # def computeRobustness(self, time, trainSet, variablesUnique, formula, paramVals, atTime):
    #     #pos train set is real trajectory values
    #
    #
    #     robustnessList = []
    #     for trajs in trainSet:
    #         #robustnessList.append(eval of traj)
    #         pass



    #find parameters that have the best robustness
    def computeRobustness(self, time, trainSet, variablesUnique, formula, paramVals, atTime):

        #Here need to calculate robustness of trajectory x values and time value by recursively calling evaluateValue on STL logic spec

        robustnessList = []
        for traj in trainSet:
            val = self.evaluateValue(traj,atTime, formula, time)
            print("Robustness val ", val)
            robustnessList.append(val)


    def evaluateValue(self, x, atTime, formula, time):
        #evaluate value for globally
        minVal = 99999999999999
        t1 = formula.temporalOperator.lowerBound + atTime
        t2 = formula.temporalOperator.upperBound + atTime

        #time index after
        timeIndexAfter = None
        for i in range(len(time)):
            if time[i] >= t1:
                timeIndexAfter = i
                break
            else:
                timeIndexAfter = len(time)-1

        timeIndexUntil = None
        for i in range(len(time)):
            if time[i] > t2:
                timeIndexUntil = i - 1
                break
            elif time[i]==t2:
                timeIndexUntil = i
                break
            else:
               timeIndexUntil = len(time) - 1

        if (timeIndexAfter > timeIndexUntil or t1 == t2):
            return self.evaluateValue(x, time[timeIndexUntil], formula, time)

        for i in range(timeIndexAfter, timeIndexUntil):
            #gets value of actual x val, stored in original variable storage and predicted param value of x in formula

            value = self.evaluateValue(x, time[i], formula, time)
            if value < minVal:
                minVal = value

        return minVal
