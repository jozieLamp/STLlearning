import logging
import numpy as np
import random
from FormulaPopulation import FormulaPopulation

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

        #Genetic Options
        self.initialPopSize = 50 # number of formulae in the initial population

    def setGeneticOptions(self, NE):
        self.initialPopSize = NE



    def runLearning(self):
        # BiFunction <double[], double[], Double> DISCRIMINATION_FUNCTION = (x, y) -> (x[0] - y[0]) / (Math.abs(x[1] + y[1]));  ###

        #TODO - add some automatic re-shaping of the actual input data files to be in 3D and not 2D, and create labels
        labels = self.readVectorFromFile(self.labelsPath) # returns one D array of labels
        time = self.readVectorFromFile(self.timePath) # returns one D array of time
        logging.info("Time ROWS "+ str(len(time)))
        logging.info("Labels DEPTH " + str(len(labels)))
        data = self.readMatrixFromFile(self.dataPath, time)  # returns 3D array of data
        logging.info("Data Loaded\n" + '%s' % (data) + "\n")

        self.learn(0.8, data, labels, time, self.variables, self.lowerBounds, self.upperBounds)


    def learn(self, trainPercentage, data, labels, time, variables, lower, upper):

        #make positive and negative training trajectories
        positiveTrainSet, negativeTrainSet, positiveTestSet, negativeTestSet = self.makeTrainingTrajectories(data, labels, trainPercentage)

        pop = FormulaPopulation(self.initialPopSize)

        atTime = 0 #atTime = 1 for cgm vars

        logging.info("Formula Variables" + '%s' % (variables))
        logging.info("Variable Lower Bounds" + '%s' % (lower))
        logging.info("Variable Upper Bounds" + '%s' % (upper))

        for i in range(len(variables)):
            pop.addVariable(variables[i], lower[i], upper[i])

        #adding initial Formulae (atomic + G +F + U )
        pop.addGeneticInitFormula(len(variables))



    def setGeneticOptions(self):
        threshold_name = "Theta"
        solution_set_size = 10
        #can be one of "regularised_logodds", "logodds"
        fitness_type = "regularised_logodds"
        size_penalty_coefficient = 1
        undefined_reference_threshold = 0.1
        init__random_number_of_atoms = False
        init__average_number_of_atoms = 3
        init__fixed_number_of_atoms = 2
        init__prob_of_less_than = 0.5
        init__prob_of_true_atom = 0#0.01
        init__and_weight = 1
        init__or_weight = 1
        init__not_weight = 1
        init__imply_weight = 1
        init__eventually_weight = 1
        init__globally_weight = 1
        init__until_weight = 1
        init__eventuallyglobally_weight = 1
        init__globallyeventually_weight = 1
        min_time_bound = 0 #they set this to 0
        max_time_bound = 100 #they set this to 11
        mutate__one_node = True
        mutate__mutation_probability_per_node = 0.01
        mutate__mutation_probability_one_node = 1 # 0.05;
        mutate__insert__weight = 2
        mutate__delete__weight = 2
        mutate__replace__weight = 4
        mutate__change__weight = 0
        mutate__delete__keep_left_node = 0.5
        mutate__insert__eventually_weight = 2
        mutate__insert__globally_weight = 2
        mutate__insert__negation_weight = 1
        mutate__replace__modal_to_modal_weight = 3
        mutate__replace__modal_to_bool_weight = 1
        mutate__replace__bool_to_modal_weight = 1
        mutate__replace__bool_to_bool_weight = 3
        mutate__replace__keep_left_node = 0.5
        mutate__replace__eventually_weight = 1
        mutate__replace__globally_weight = 1
        mutate__replace__until_weight = 1
        mutate__replace__and_weight = 1
        mutate__replace__or_weight = 1
        mutate__replace__imply_weight = 1
        mutate__replace__not_weight = 1
        mutate__replace__new_left_node_for_boolean = 0.5
        mutate__replace__new_left_node_for_until = 0.5
        mutate__replace__new_left_node_for_until_from_globally = 0.05
        mutate__replace__new_left_node_for_until_from_eventually = 0.95
        mutate__change__prob_lower_bound = 0.5
        mutate__change__proportion_of_variation = 0.1


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
