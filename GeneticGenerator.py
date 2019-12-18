import logging

#Generates different genetic population sets, mainly used for Genetic Population
class GeneticGenerator:
    def __init__(self):
        pass

    #returns Genetic Population
    def optimizeGenerationParameters(self, pop, variables, time, positiveTrainSet, negativeTrainSet, positiveTestSet, negativeTestSet, atTime, paramDict):
        rankFormulae = []
        rankParameters = []
        rankScore = []

        for i in range(len(pop.population)):
            formula = pop.population[i]

            #gpucb
            logging.info("OPTIMIZE PARAMETER OF FORMULA " + formula.toString())
            #fitness function = private static final BiFunction<double[], double[], Double> DISCRIMINATION_FUNCTION = (x, y) -> (x[0] - y[0]) / (Math.abs(x[1] + y[1]));
            self.computeAverageMultiTrajectory(35, variables, time, formula, pop, atTime, paramDict)

        #return genetic pop


    #returns an array of doubles
    #original header from java
    #int maxIterations, BiFunction<double[], double[], Double> fitness, String[] variablesUnique, double[] ds2Times, double[][][] normal_model, double[][][] ineffective_model, Formula formula, FormulaPopulation pop, double[] timeBoundsFormula, double atTime)
    def computeAverageMultiTrajectory(self, maxIters, variablesUnique, time, formula, pop, atTime, paramDict):
        variables = formula.paramList

        #Get bounds of time
        timeBounds = formula.timeBound
        for t in formula.timeBound:
            pass
        lowerBound = formula.timeBound[0]
        upperBound = formula.timeBound[1]

        #Get bounds of variable params
        varLB = []
        varUB = []
        for v in variables:
            varBounds = paramDict[v.name]
            varLB.append(varBounds[0])
            varUB.append(varBounds[1])

        # print(varLB)
        # print(varUB)
