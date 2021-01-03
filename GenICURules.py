import pandas as pd
import numpy as np
import random
from random import randint
from pandas.plotting import scatter_matrix # optional
import numpy as np
import matplotlib
import math
import re
from collections import OrderedDict
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from GeneticSpec.Trajectory import Trajectory
from GeneticSpec.GeneticPopulation import GeneticPopulation
from GeneticSpec.GeneticPopulation import Score
from SignalTemporalLogic.STLFactory import STLFactory
import MCR.CalculateMCR_ICU as mcr


# Helper Methods
names = ['LOS', 'ICU_Pt_Days', 'Mort', 'n_evts', 'y', 'tte', 'death', 'direct',
       'MET', 'Sgy', 'Glasgow_Coma_Scale_Total', 'O2_Flow', 'Resp', 'SpO2',
       'SBP', 'Pulse', 'Temp', 'ALBUMIN', 'ALKALINE_PHOSPHATASE', 'ALT_GPT',
       'AST_GOT', 'BLOOD_UREA_NITROGEN', 'CALCIUM', 'CHLORIDE', 'CO2',
       'CREATININE', 'GLUCOSE', 'HEMOGLOBIN', 'LACTIC_ACID', 'MAGNESIUM',
       'OXYGEN_SATURATION', 'PARTIAL_THROMBOPLASTIN_TIME', 'PCO2',
       'PHOSPHORUS', 'PLATELET_COUNT', 'POTASSIUM', 'PROTIME_INR', 'SODIUM',
       'TOTAL_BILIRUBIN', 'TOTAL_PROTEIN', 'TROPONIN_I',
       'WHITE_BLOOD_CELL_COUNT', 'hr', 's2_hr', 's8_hr', 's24_hr', 'n_edrk',
       'edrk', 's2_edrk', 's8_edrk', 's24_edrk', 'srr', 'dfa', 'cosen', 'lds',
       'af', 'AF']
temporalOp = ["G", "F", "U"]
yboolOp = ["&", "->"]
boolOp = ["|", "&", "->"]
relOp = [">", ">=", "<", "<="]


def getCorr(df):
    corr_matrix = df.corr().abs()
    cm = corr_matrix["y"].sort_values(ascending=False)
    corrMatrix = pd.DataFrame(cm)
    yCorrs = corrMatrix.reset_index()

    cList = df.corr().abs().unstack().sort_values(ascending=False).drop_duplicates()
    c = pd.DataFrame(cList)
    allCorrs = c.reset_index()

    return yCorrs, allCorrs


def makeTime(timeLower, timeUpper):
    tl = randint(timeLower, timeUpper)
    tu = randint(timeLower, timeUpper)
    if tu < tl:
        t = tu
        tu = tl
        tl = t

    return tl, tu


def makeParams(valLower, valUpper):
    return random.uniform(valLower, valUpper)


def genYRule(tl, tu, var, variables):
    temp = random.choice(temporalOp)
    bol = random.choice(yboolOp)
    rop1 = random.choice(relOp)

    if rop1 in [">", ">="]:
        val1 = makeParams(variables[var][0], variables[var][1])
    else:
        val1 = makeParams(variables[var][1], variables[var][2])

    yVal = makeParams(variables["y"][0], variables["y"][2])

    if temp != "U":
        rule = temp + "[" + str(tl) + "," + str(tu) + "]" + "(" + var + " " + rop1 + " " + str(
            val1) + " " + bol + " " + "y" + " " + "=" + " " + str(yVal) + ")"
    else:
        rule = "((" + var + " " + rop1 + " " + str(val1) + ") " + temp + "[" + str(tl) + "," + str(
            tu) + "] " + "(" + "y" + " " + "=" + " " + str(yVal) + "))"

    return rule


def genRule(tl, tu, var1, var2, variables):
    temp = random.choice(temporalOp)
    bol = random.choice(boolOp)

    r1 = random.randint(0, 1)
    r2 = random.randint(0, 1)

    if r1 == 0:  # lower
        rop1 = ">="
        val1 = makeParams(variables[var1][0], variables[var1][1])
    else:
        rop1 = "<="
        val1 = makeParams(variables[var1][1], variables[var1][2])

    if r2 == 0:  # lower
        rop2 = ">="
        val2 = makeParams(variables[var2][0], variables[var2][1])
    else:
        rop2 = "<="
        val2 = makeParams(variables[var2][1], variables[var2][2])

    if temp != "U":
        rule = temp + "[" + str(tl) + "," + str(tu) + "]" + "(" + var1 + " " + rop1 + " " + str(
            val1) + " " + bol + " " + var2 + " " + rop2 + " " + str(val2) + ")"

    else:
        rule = "((" + var1 + " " + rop1 + " " + str(val1) + ") " + temp + "[" + str(tl) + "," + str(
            tu) + "] " + "(" + var2 + " " + rop2 + " " + str(val2) + "))"

    return rule


def genInitialRuleSet(df):
    ruleset = []

    # get corrs
    yCorrs, allCorrs = getCorr(df)
    # print("YCorrs:",  len(yCorrs), "AllCorrs:",  len(allCorrs))

    # make var dictionary
    minVals = df.min()
    maxVals = df.max()
    medVals = df.mean()
    timeLower = 0
    # timeUpper = df.shape[0]
    timeUpper = 2

    variables = {}
    for b in range(0, len(names)):
        variables[names[b]] = [minVals[b], medVals[b], maxVals[b]]

    paramDict = {}
    for i in range(len(names)):
        paramDict.update({names[i]: [minVals[i], maxVals[i]]})

    # print(variables, "\n")

    # Make 5 common rules (do this 5 times)
    for tw in range(10):
        # HR and Pulse
        tl, tu = makeTime(timeLower, timeUpper)
        val1 = makeParams(variables["hr"][0], variables["hr"][1])
        val2 = makeParams(variables["Pulse"][0], variables["Pulse"][1])
        rule = "G" + "[" + str(tl) + "," + str(tu) + "]" + "(" + "hr" + " " + ">=" + " " + str(
            val1) + " " + "&" + " " + "Pulse" + " " + ">=" + " " + str(val2) + ")"
        ruleset.append(rule)

        # af and cosen
        tl, tu = makeTime(timeLower, timeUpper)
        val1 = makeParams(variables["af"][1], variables["af"][2])
        val2 = makeParams(variables["AF"][1], variables["AF"][2])
        val3 = makeParams(variables["cosen"][0], variables["cosen"][1])
        rule = "F" + "[" + str(tl) + "," + str(tu) + "]" + "((" + "af" + " " + "<=" + " " + str(
            val1) + " " + "| " + "AF" + " " + "<=" + " " + str(
            val2) + ") " + "&" + " " + "cosen" + " " + ">=" + " " + str(val3) + ")"
        ruleset.append(rule)

        # n_evts and LOS
        tl, tu = makeTime(timeLower, timeUpper)
        val1 = makeParams(variables["n_evts"][1], variables["af"][2])
        val2 = makeParams(variables["LOS"][0], variables["LOS"][1])
        rule = "G" + "[" + str(tl) + "," + str(tu) + "]" + "(" + "n_evts" + " " + "<=" + " " + str(
            val1) + " " + "->" + " " + "LOS" + " " + ">=" + " " + str(val2) + ")"
        ruleset.append(rule)

        # death and MET
        tl, tu = makeTime(timeLower, timeUpper)
        val1 = makeParams(variables["MET"][0], variables["MET"][1])
        rule = "((" + "MET" + " " + ">=" + " " + str(val1) + ") " + "U" + "[" + str(tl) + "," + str(
            tu) + "]" + " (" + "death" + " " + "=" + " " + str(variables["death"][1]) + "))"
        ruleset.append(rule)

        # Blood urea nitrogen and creatnine
        tl, tu = makeTime(timeLower, timeUpper)
        val1 = makeParams(variables["BLOOD_UREA_NITROGEN"][1], variables["BLOOD_UREA_NITROGEN"][2])
        val2 = makeParams(variables["CREATININE"][0], variables["CREATININE"][1])
        rule = "F" + "[" + str(tl) + "," + str(tu) + "]" + "(" + "BLOOD_UREA_NITROGEN" + " " + "<=" + " " + str(
            val1) + " " + "&" + " " + "CREATININE" + " " + ">=" + " " + str(val2) + ")"
        ruleset.append(rule)

    # Make y correlated rules
    if not math.isnan(yCorrs.iloc[0, 1]):
        for j in range(1, len(yCorrs)):
            tl, tu = makeTime(timeLower, timeUpper)
            var = yCorrs.iloc[j, 0]
            rule = genYRule(tl, tu, var, variables)
            ruleset.append(rule)
    else:
        for j in range(1, 50):
            tl, tu = makeTime(timeLower, timeUpper)
            var = random.choice(names)
            rule = genYRule(tl, tu, var, variables)
            ruleset.append(rule)

    # Make rules for top correlated attributes
    for k in range(1, 500):
        if k < len(allCorrs):
            tl, tu = makeTime(timeLower, timeUpper)
            corr1 = allCorrs.iloc[k, 0]
            corr2 = allCorrs.iloc[k, 1]

            if corr1.lower() < corr2.lower():
                var1 = corr1
                var2 = corr2
            else:
                var1 = corr2
                var2 = corr1

            rule = genRule(tl, tu, var1, var2, variables)
            ruleset.append(rule)
        else:  # add random for last
            tl, tu = makeTime(timeLower, timeUpper)
            var1 = random.choice(names)
            var2 = random.choice(names)
            rule = genRule(tl, tu, var1, var2, variables)
            ruleset.append(rule)

    return ruleset, paramDict

#Make positive and negative training and validation sets
def makeTrainingTrajectories(data, labels, trainPercentage):
    positiveTrajectories = []
    negativeTrajectories = []

    for i in range(len(labels)):
        if labels[i] == -1:
            negativeTrajectories.append(i)
        else:
            positiveTrajectories.append(i)

    random.shuffle(positiveTrajectories)
    random.shuffle(negativeTrajectories)

    trainPositiveSize = int(round((len(positiveTrajectories) * trainPercentage),3))
    validationPositiveSize = int(round((len(positiveTrajectories) - trainPositiveSize),3))
    trainNegativeSize = int(round((len(negativeTrajectories) * trainPercentage),3))
    validationNegativeSize = int(round((len(negativeTrajectories) - trainNegativeSize),3))

    numTime = data.shape[1]
    numAttb = data.shape[2]
    positiveTrainSet = np.zeros((trainPositiveSize,numTime,numAttb))# trainPositiveSize
    negativeTrainSet = np.zeros((trainNegativeSize,numTime,numAttb))  # trainNegativeSize
    positiveValidationSet = np.zeros((validationPositiveSize,numTime,numAttb))  # validationPositiveSize
    negativeValidationSet = np.zeros((validationNegativeSize,numTime,numAttb)) # validationNegativeSize

    for i in range(trainPositiveSize):
        positiveTrainSet[i, :, :] = data[positiveTrajectories[i], :, :]

    for i in range(trainNegativeSize):
        negativeTrainSet[i, :, :] = data[negativeTrajectories[i], :, :]

    for i in range(validationPositiveSize):
        positiveValidationSet[i, :, :] = data[positiveTrajectories[trainPositiveSize + i], :, :]

    for i in range(validationNegativeSize):
        negativeValidationSet[i, :, :] = data[negativeTrajectories[trainNegativeSize + i], :, :]

    # print("Positive Train Set Size " + str(len(positiveTrainSet)))
    # print("Negative Train Set Size " + str(len(negativeTrainSet)))
    # print("Positive Validation Set Size " + str(len(positiveValidationSet)))
    # print("Negative Validation Set Size " + str(len(negativeValidationSet)))

    return positiveTrainSet, negativeTrainSet, positiveValidationSet, negativeValidationSet

#Read in 1D vector from a txt file
def readVectorFromFile(filePath):
    vals = []
    file = open(filePath, "r")
    for line in file:
        for v in line.split(','):
            vals.append(float(v))

    return vals

#Read in 3D matrix from a txt file
def readMatrixFromFile(filePath, time):
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
    print("New Data Shape " + str(vals.shape))

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

# More robust when value higher
def computeRobustness(trainSet, time, pd, atTime, formula):

    rVals = []
    #loop through train set and calculate robustness for each variable
    for i in trainSet:  # i is 2d array of values for each var
        #print(i)
        values = []
        for v in names:
            values.append(0)
        traj = Trajectory(trajectories=i, time=time, variables=names, paramDict=pd, values=values)
        rVals.append(formula.evaluateRobustness(traj, atTime))

    if rVals == []:
        mean = 0
        variance = 0
    else:
        mean = sum(rVals) / len(rVals)
        variance = np.std(rVals)

    return mean, variance #return two doubles

def discriminationFunction(xMean, xVar, yMean, yVar):  # list x and y
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


def calculateFinalScores(testSet, formula, time, variables, paramDict):
    posClassified = []
    for i in testSet:
        values = []
        for v in variables:
            values.append(0)
        traj = Trajectory(trajectories=i, time=time, variables=variables, paramDict=paramDict, values=values)
        if formula.evaluateValue(traj, 0):
            posClassified.append(1)
        else:
            posClassified.append(0)

    posSum = sum(posClassified)
    return posSum



def run():

    stlFac = STLFactory()

    for i in range(1, 8106):
        print("\nID is ", i)

        try:
            #gen corr rules
            df = pd.read_csv("Data/ICUDataFrames/" + repr(i) + "DataFrame.csv", sep=",", index_col=0)
            dfLabels = pd.read_csv("Data/ICUDataFrames/" + repr(i) + "Labels.csv", sep=",")
            ruleset, paramDict = genInitialRuleSet(df)
            print("Length of Ruleset", len(ruleset))

            # Load labels, time and data
            labels = readVectorFromFile("Data/ICUData/" + repr(i) + "labels.txt")  # returns one D array of labels
            time = list(range(0,len(df)))  # returns one D array of time
            # print("Time ROWS " + str(len(time)))

            sliceTime = list(range(0,2))
            # print("Labels/Num Layers DEPTH " + str(len(labels)))
            data = readMatrixFromFile("Data/ICUData/" + repr(i) + ".txt", sliceTime)  # returns 3D array of data
            print("Data Loaded\n" + '%s' % (data) + "\n")

            positiveTrainSet, negativeTrainSet, positiveTestSet, negativeTestSet = makeTrainingTrajectories(data, labels, 0.5)
            testSet =  np.zeros((positiveTestSet.shape[0]+negativeTestSet.shape[0], positiveTestSet.shape[1], positiveTestSet.shape[2]))
            totalTrajectories = len(testSet)


            formulas = []
            scores  = []
            lst = []

            #Make STL tree rules
            for r in ruleset:
                formulas.append(stlFac.constructFormulaTree(r + "\n"))

            for f in formulas:
                # get score, make score variable
                val1Mean, val1Var = computeRobustness(positiveTrainSet, sliceTime, paramDict, 0, f)
                val2Mean, val2Var = computeRobustness(negativeTrainSet, sliceTime, paramDict, 0, f)
                classDif = discriminationFunction(val1Mean, val1Var, val2Mean, val2Var)
                s = Score(val1Mean, val1Var, val2Mean, val2Var, classDif)
                scores.append(s)

                #calc  positive and negative classes
                posSum = calculateFinalScores(testSet, f, sliceTime, names, paramDict)
                s.posClassPctg = posSum / totalTrajectories
                s.negClassPctg = (totalTrajectories - posSum) / totalTrajectories

                # print(f.toString() + " [" + s.toStringFull() + "]")
                lst.append(f.toString() + " [" + s.toStringFull() + "]")


            #save to file
            with open("Rules/ICU/" + repr(i) + "ruleScores.txt", 'w') as filehandle:
                for r in lst:
                    filehandle.write('%s\n' % r)

            # calculate MCR
            print("Running MCR")
            mcr.runMCRGenRules(i)


        except FileNotFoundError:
            print("******File not found for", repr(i))





# Main Runner
def main():
    run()



if __name__ == '__main__':
    main()