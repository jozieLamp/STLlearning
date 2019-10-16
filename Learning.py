import logging
import numpy as np

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

        labels = self.readVectorFromFile(self.labelsPath) # returns one D array of labels
        time = self.readVectorFromFile(self.timePath) # returns one D array of time
        print("time len ", len(time))
        print("labels len ",len(labels))

        data = self.readMatrixFromFile(self.dataPath)  # returns 3D array of data


    def readVectorFromFile(self, filePath):
        vals = []
        file = open(filePath, "r")
        for line in file:
            for v in line.split(','):
                vals.append(float(v))

        return vals

    def readMatrixFromFile(self, filePath):
        rows = 1
        cols = 0
        file = open(filePath, "r")
        for line in file:
            for v in line.split(','):
                cols+=1
            rows+=1

        print(rows, cols)
        #depth, columns, rows
        vals = np.zeros((5, 1, 2))


        # print(vals)
