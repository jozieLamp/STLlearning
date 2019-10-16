import logging
import numpy as np
import re

#
# Learning for single client
#
class Learning:
    def __init__(self, logLevel, dataPath, labelsPath, timePath):
        logging.basicConfig(level=logLevel)
        self.dataPath = dataPath
        self.labelsPath = labelsPath
        self.timePath = timePath

    def runLearning(self):
        # BiFunction <double[], double[], Double> DISCRIMINATION_FUNCTION = (x, y) -> (x[0] - y[0]) / (Math.abs(x[1] + y[1]));  ###

        #TODO - add some automatic re-shaping of the input data files to be in 3D and not 2D, and create labels
        labels = self.readVectorFromFile(self.labelsPath) # returns one D array of labels
        time = self.readVectorFromFile(self.timePath) # returns one D array of time
        logging.info("Time ROWS "+ str(len(time)))
        logging.info("Labels DEPTH " + str(len(labels)))
        data = self.readMatrixFromFile(self.dataPath, time)  # returns 3D array of data
        logging.info("Data Loaded\n" + '%s' % (data))


    def learn(self):
        pass


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
