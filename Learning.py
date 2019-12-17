import logging
import numpy as np
import random
from FormulaPopulation import FormulaPopulation
from GeneticOptions import GeneticOptions
from GeneticPopulation import GeneticPopulation
from GeneticGenerator import GeneticGenerator

#
# Learning for single client
#
class Learning:
    def __init__(self, logLevel, dataPath, labelsPath, timePath, variables, lower, upper):
        logging.basicConfig(level=logLevel)
        self.dataPath = dataPath
        self.labelsPath = labelsPath
        self.timePath = timePath
        self.variables = variables
        self.lowerBounds = lower
        self.upperBounds = upper

        #Genetic Options Object
        self.genOps = GeneticOptions()
        self.genOps.initialPopSize = 50 # number of formulae in the initial population


    #start learning process
    def run(self):
        # BiFunction <double[], double[], Double> DISCRIMINATION_FUNCTION = (x, y) -> (x[0] - y[0]) / (Math.abs(x[1] + y[1]));  ###

        #TODO - add some automatic re-shaping of the actual input data files to be in 3D and not 2D
        #First load labels, time and data
        labels = self.readVectorFromFile(self.labelsPath) # returns one D array of labels
        time = self.readVectorFromFile(self.timePath) # returns one D array of time
        logging.info("Time ROWS "+ str(len(time)))
        logging.info("Labels DEPTH " + str(len(labels)))
        data = self.readMatrixFromFile(self.dataPath, time)  # returns 3D array of data
        logging.info("Data Loaded\n" + '%s' % (data) + "\n")


        #Run learning
        self.learn(0.8, data, labels, time, self.variables, self.lowerBounds, self.upperBounds)


    def learn(self, trainPercentage, data, labels, time, variables, lower, upper):

        #make positive and negative training trajectories
        positiveTrainSet, negativeTrainSet, positiveTestSet, negativeTestSet = self.makeTrainingTrajectories(data, labels, trainPercentage)

        logging.info("Formula Variables" + '%s' % (variables))
        logging.info("Variable Lower Bounds" + '%s' % (lower))
        logging.info("Variable Upper Bounds" + '%s' % (upper))

        #Make param dictionary for formula pop
        pd = {}
        for i in range(len(variables)):
            pd.update({variables[i]: [lower[i], upper[i]]})

        logging.info("Param Dict Created" + '%s' % (pd) + "\n")

        #Make formula population object to handle formulas
        pop = FormulaPopulation(popSize=self.genOps.initialPopSize, paramDict=pd)

        #TODO - do we need this variable????
        atTime = min(time) #atTime = 1 for cgm vars #What value time starts at, usually 0 or 1


        #add vars and their values to the formula pop object
        for i in range(len(variables)):
            pop.addVariable(variables[i], lower[i], upper[i])

        #Set some genetic options for min and max time bounds
        self.genOps.min_time_bound = min(time)
        self.genOps.max_time_bound = max(time)
        #self.genOps.use_or = False

        #adding initial Formulae (atomic + G +F + U ), using number of variables
        pop.addGeneticInitFormula(self.genOps)

        #Add random formulas
        #TODO = complete this method
        # for i in range(self.genOps.max_num_rand):
        #     pop.addRandomInitFormula(self.genOps)

        #Begin genetic algorithm learning part
        generation = GeneticPopulation()
        genGenerator = GeneticGenerator()
        numGen = self.genOps.number_generations
        logging.info("NUMBER OF GENERATIONS: " + '%s' % (numGen))
        logging.info("GENETIC ALGORITHM - START")

        for k in range(numGen):
            logging.info("GENERATION #: " + '%s' % (k))
            logging.info("> OPTIMIZING POPULATION PARAMETER")
            generation = genGenerator.optimizeGenerationParameters(pop=pop, variables=variables, time=time,
                positiveTrainSet=positiveTrainSet, negativeTrainSet=negativeTrainSet, positiveTestSet=positiveTestSet,
                            negativeTestSet=negativeTestSet, atTime=atTime)



    #Make positive and negative training and validation sets
    def makeTrainingTrajectories(self, data, labels, trainPercentage):
        positiveTrajectories = []
        negativeTrajectories = []

        for i in range(len(labels)):
            if labels[i] == -1:
                negativeTrajectories.append(i)
            else:
                positiveTrajectories.append(i)

        random.shuffle(positiveTrajectories)
        random.shuffle(negativeTrajectories)

        trainPositiveSize = len(positiveTrajectories) * trainPercentage
        validationPositiveSize = len(positiveTrajectories) - trainPositiveSize
        trainNegativeSize = len(negativeTrajectories) * trainPercentage
        validationNegativeSize = len(negativeTrajectories) - trainNegativeSize

        # TODO these were all 3d arrays  [] [] [] --> I made them one D, and then need to convert to 3D later
        positiveTrainSet = []  # trainPositiveSize
        negativeTrainSet = []  # trainNegativeSize
        positiveValidationSet = []  # validationPositiveSize
        negativeValidationSet = []  # validationNegativeSize

        for i in range(int(trainPositiveSize)):
            positiveTrainSet.append(data[positiveTrajectories[i]])

        for i in range(int(trainNegativeSize)):
            negativeTrainSet.append(data[negativeTrajectories[i]])

        for i in range(int(validationPositiveSize)):
            positiveValidationSet.append(data[positiveTrajectories[int(trainPositiveSize + i)]])

        for i in range(int(validationNegativeSize)):
            negativeValidationSet.append(data[negativeTrajectories[int(trainNegativeSize + i)]])

        logging.info("Positive Train Set Size " + str(len(positiveTrainSet)))
        logging.info("Positive Validation Set Size " + str(len(positiveValidationSet)))
        logging.info("Negative Train Set Size " + str(len(negativeTrainSet)))
        logging.info("Negative Validation Set Size " + str(len(negativeValidationSet)) + "\n")

        return positiveTrainSet, negativeTrainSet, positiveValidationSet, negativeValidationSet

    #Read in 1D vector from a txt file
    def readVectorFromFile(self, filePath):
        vals = []
        file = open(filePath, "r")
        for line in file:
            for v in line.split(','):
                vals.append(float(v))

        return vals

    #Read in 3D matrix from a txt file
    def readMatrixFromFile(self, filePath, time):
        #get dimensions of matrix
        depth = 0
        numAttributes = 0
        file = open(filePath, "r")
        for line in file:
            numAttributes = 0
            for v in line.split(','):
                numAttributes+=1
            depth+=1

        rows = len(time)
        cols = int(numAttributes / len(time))

        # depth, columns, rows
        vals = np.zeros((depth, cols, rows))
        logging.info("New Data Shape " + str(vals.shape))

        #Now load data
        file = open(filePath, "r")
        d = 0
        for line in file:
            colCounter = 0
            rowCounter = 0
            for v in line.split(','):
            # ruleStrings = re.split(',', line)
                if colCounter == cols:
                    rowCounter += 1
                    colCounter = 0

                vals[d][colCounter][rowCounter] = v
                colCounter+= 1
            #go to next depth
            d += 1

        return vals
