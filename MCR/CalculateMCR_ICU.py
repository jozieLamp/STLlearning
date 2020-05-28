
from SignalTemporalLogic.STLFactory import STLFactory
import pandas as pd
import numpy as np
import re
from collections import OrderedDict

## Make functions

def readRulesFromFile(scorefilepath):
    posRules = []
    negRules = []

    with open(scorefilepath) as fp:
        lineCount = 0
        line = fp.readline()
        while line:
            rule = (re.search('(.*) \[Discrimination Score:', line)).group(1) + "\n"
            result = re.search('\[Discrimination Score:(.*)\n', line)
            r = result.group(1)
            nums = re.findall(r"[-+]?\d*\.\d+|\d+", r)
            p = (re.search('Percent Class \+ : (.*)]', r)).group(1)
            pos = (re.search('(.*);', p)).group(1)
            neg = (re.search('Percent Class - : (.*)', p)).group(1)
            nums.insert(0, rule)
            if pos > neg:
                posRules.append(nums)
            else:
                negRules.append(nums)

            line = fp.readline()
            lineCount += 1

    return posRules, negRules


def getWordPairs(posRules, negRules):
    wordPairsPos = []
    for p in posRules:
        noTime = re.findall(r'([^[\]]+)(?:$|\[)', p)
        noTime = ' '.join([str(elem) for elem in noTime])
        nums = re.findall(r"[-+]?\d*\.\d+|\d+", noTime)
        nums = [float(i) for i in nums]
        st = re.sub('[^a-zA-Z]+', ' ', p)
        st = [i for i in st.split()]

        if 'G' in st:
            st = list(filter(lambda a: a != 'G', st))
        if 'F' in st:
            st = list(filter(lambda a: a != 'F', st))
        if 'U' in st:
            st = list(filter(lambda a: a != 'U', st))

        for w in range(len(st)):
            if "Change" in st[w]:
                if nums[w] >= 0:
                    st[w] += "+"

                else:
                    st[w] += "-"

        wordPairsPos.append(st)

    wordPairsNeg = []
    for p in negRules:
        noTime = re.findall(r'([^[\]]+)(?:$|\[)', p)
        noTime = ' '.join([str(elem) for elem in noTime])
        nums = re.findall(r"[-+]?\d*\.\d+|\d+", noTime)
        nums = [float(i) for i in nums]
        st = re.sub('[^a-zA-Z]+', ' ', p)
        st = [i for i in st.split()]

        if 'G' in st:
            st = list(filter(lambda a: a != 'G', st))
        if 'F' in st:
            st = list(filter(lambda a: a != 'F', st))
        if 'U' in st:
            st = list(filter(lambda a: a != 'U', st))

        for w in range(len(st)):
            if "Change" in st[w]:
                if nums[w] >= 0:
                    st[w] += "+"

                else:
                    st[w] += "-"

        wordPairsNeg.append(st)

    return wordPairsPos, wordPairsNeg


def getOccDataframe(wordPairsPos, wordPairsNeg, names):
    occurrences = OrderedDict((name, OrderedDict((name, 0) for name in names)) for name in names)

    # Find the co-occurrences:
    for l in wordPairsPos:
        for i in range(len(l)):
            for item in l[:i] + l[i + 1:]:
                occurrences[l[i]][item] += 1

    dfPos = pd.DataFrame(occurrences, columns=occurrences.keys())

    occurrences = OrderedDict((name, OrderedDict((name, 0) for name in names)) for name in names)
    # Find the co-occurrences:
    for l in wordPairsNeg:
        for i in range(len(l)):
            for item in l[:i] + l[i + 1:]:
                occurrences[l[i]][item] += 1

    dfNeg = pd.DataFrame(occurrences, columns=occurrences.keys())

    return dfPos, dfNeg


def getMCRPosOutcome(posRules, dt, dataLabels):
    factory = STLFactory()
    totalSlices = len(dt) / 2

    mcrList = []
    for line in posRules:
        p = line[0]
        ft = factory.constructFormulaTree(p)

        TP = 0
        TN = 0
        FP = 0
        FN = 0

        labelCount = 0
        for i in range(0, len(dt), 2):
            data = dt.iloc[i:i+2] #get rows of 2
            label = dataLabels.loc[labelCount].values[0]
            labelCount+=1

            val = ft.evaluateTruthValue(data)


            if label == 1 and val == True:
                TP += 1
            elif label == -1 and val == False:
                TN += 1
            elif label == 1 and val == False:
                FN += 1
            else: #label == -1 and val == True
                FP += 1

        actualNo = TN + FP
        actualYes = FN + TP
        predictedNo = TN + FN
        predictedYes = TP + FP
        TPR = TP / actualYes if actualYes else 0
        FPR = FP / actualNo if actualNo else 0
        TNR = TN / actualNo  if actualNo else 0
        prec = TP / predictedYes if predictedYes else 0
        accuracy = (TP + TN) / totalSlices
        MCR = 1 - accuracy

        mcrList.append([p, line[1], line[2], line[3], line[4], line[5], TP, TN, FP, FN, actualYes, actualNo, predictedYes, predictedNo, TPR, TNR, FPR, prec, accuracy, MCR])

    mcrDF = pd.DataFrame(mcrList, columns=['Rule', 'Discrimination Score', 'Pos Robustness', 'Neg Robustness', 'Percent Class +', 'Percent Class -',
                    'TP', 'TN', 'FP', 'FN', 'Actual Yes', 'Actual No', 'Predicted Yes', 'Predicted No', 'TPR/Sens', 'TNR/Spec', 'FPR', 'Precision', 'Accuracy', 'MCR'])
    mcrDF = mcrDF.sort_values(by='Accuracy', ascending=False)

    return mcrDF, totalSlices


def getMCRNegOutcome(negRules, dt, dataLabels):
    factory = STLFactory()
    totalSlices = len(dt) / 2

    mcrList = []
    for line in negRules:
        p = line[0]
        ft = factory.constructFormulaTree(p)

        TP = 0
        TN = 0
        FP = 0
        FN = 0

        labelCount = 0
        for i in range(0, len(dt), 2):
            data = dt.iloc[i:i + 2]  # get rows of 2
            label = dataLabels.loc[labelCount].values[0]
            labelCount += 1

            val = ft.evaluateTruthValue(data)

            if label == -1 and val == True:
                TN += 1
            elif label == 1 and val == False:
                TP += 1
            elif label == -1 and val == False:
                FP += 1
            else: #label == 1 and val == True
                FN += 1

        actualNo = TN + FP
        actualYes = FN + TP
        predictedNo = TN + FN
        predictedYes = TP + FP
        TPR = TP / actualYes if actualYes else 0
        FPR = FP / actualNo if actualNo else 0
        TNR = TN / actualNo if actualNo else 0
        prec = TP / predictedYes if predictedYes else 0
        accuracy = (TP + TN) / totalSlices
        MCR = 1 - accuracy

        mcrList.append(
            [p, line[1], line[2], line[3], line[4], line[5], TP, TN, FP, FN, actualYes, actualNo, predictedYes,
             predictedNo, TPR, TNR, FPR, prec, accuracy, MCR])

    mcrDF = pd.DataFrame(mcrList,
                         columns=['Rule', 'Discrimination Score', 'Pos Robustness', 'Neg Robustness', 'Percent Class +',
                                  'Percent Class -',
                                  'TP', 'TN', 'FP', 'FN', 'Actual Yes', 'Actual No', 'Predicted Yes', 'Predicted No',
                                  'TPR/Sens', 'TNR/Spec', 'FPR', 'Precision', 'Accuracy', 'MCR'])
    mcrDF = mcrDF.sort_values(by='Accuracy', ascending=False)

    return mcrDF, totalSlices

#add rules that perfectly misclassify the data to other set
def addMisclassifiedRules(posDF, negDF, totalPatients):
    negRows = negDF[negDF["MCR"] > 0.826]
    negDF.drop(negDF[negDF['MCR'] > 0.826].index, inplace=True)

    posRows = posDF[posDF["MCR"] > 0.826]
    posDF.drop(posDF[posDF["MCR"] > 0.826].index, inplace=True)

    lst = []
    for index, n in negRows.iterrows():
        TP = n["FN"]
        TN = n["FP"]
        FP = n["TN"]
        FN = n["TP"]
        actualNo = TN + FP
        actualYes = FN + TP
        predictedNo = TN + FN
        predictedYes = TP + FP
        TPR = TP / actualYes if actualYes else 0
        FPR = FP / actualNo if actualNo else 0
        TNR = TN / actualNo if actualNo else 0
        prec = TP / predictedYes if predictedYes else 0
        accuracy = (TP + TN) / totalPatients
        MCR = 1 - accuracy

        l = [n["Rule"], n['Discrimination Score'], n['Neg Robustness'], n['Pos Robustness'], n['Percent Class -'], n['Percent Class +'], TP, TN, FP, FN,
               actualYes, actualNo, predictedYes, predictedNo, TPR, TNR, FPR, prec, accuracy, MCR]

        lst.append(l)

    posLst = posDF.values.tolist()
    posLst.extend(lst)

    fullPosDF = pd.DataFrame(posLst, columns=['Rule', 'Discrimination Score', 'Pos Robustness', 'Neg Robustness',
                                      'Percent Class +','Percent Class -','TP', 'TN', 'FP', 'FN', 'Actual Yes', 'Actual No', 'Predicted Yes',
                                      'Predicted No', 'TPR/Sens', 'TNR/Spec', 'FPR', 'Precision', 'Accuracy', 'MCR'])

    lst = []
    for index, n in posRows.iterrows():
        TP = n["FN"]
        TN = n["FP"]
        FP = n["TN"]
        FN = n["TP"]
        actualNo = TN + FP
        actualYes = FN + TP
        predictedNo = TN + FN
        predictedYes = TP + FP
        TPR = TP / actualYes if actualYes else 0
        FPR = FP / actualNo if actualNo else 0
        TNR = TN / actualNo if actualNo else 0
        prec = TP / predictedYes if predictedYes else 0
        accuracy = (TP + TN) / totalPatients
        MCR = 1 - accuracy

        l = [n["Rule"], n['Discrimination Score'], n['Neg Robustness'], n['Pos Robustness'], n['Percent Class -'], n['Percent Class +'], TP, TN, FP, FN,
               actualYes, actualNo, predictedYes, predictedNo, TPR, TNR, FPR, prec, accuracy, MCR]

        lst.append(l)

    negLst = negDF.values.tolist()
    negLst.extend(lst)

    fullNegDF = pd.DataFrame(negLst, columns=['Rule', 'Discrimination Score', 'Pos Robustness', 'Neg Robustness',
                                              'Percent Class +', 'Percent Class -', 'TP', 'TN', 'FP', 'FN',
                                              'Actual Yes', 'Actual No', 'Predicted Yes',
                                              'Predicted No', 'TPR/Sens', 'TNR/Spec', 'FPR', 'Precision', 'Accuracy',
                                              'MCR'])

    fullPosDF = fullPosDF.sort_values(by='Accuracy', ascending=False)
    fullNegDF = fullNegDF.sort_values(by='Accuracy', ascending=False)

    return fullPosDF, fullNegDF



def runMCR(patient):

    # Load all rules
    filepath = "../Rules/ICU/" + str(patient) + "ruleScores.txt"
    posRules, negRules = readRulesFromFile(filepath)

    # Load Data
    data = pd.read_csv('../Data/ICUDataFrames/' + str(patient) + 'DataFrame.csv', index_col=0)
    labels = pd.read_csv('../Data/ICUDataFrames/' + str(patient) + 'Labels.csv')

    # Positive Rules MCR
    posDF, totalPatients = getMCRPosOutcome(posRules, data, labels)

    # Negative Rules MCR
    negDF, totalPatients = getMCRNegOutcome(negRules, data, labels)

    # posDF, negDF = addMisclassifiedRules(posDF, negDF, totalPatients)
    print("\nPositive rules")
    print(posDF)
    print("\nNegative rules")
    print(negDF)
    posDF.to_csv("../Rules/MCR/" + str(patient) + 'PositiveMCR.csv', index=False)
    negDF.to_csv("../Rules/MCR/" + str(patient) + 'NegativeMCR.csv', index=False)

    #make single file with mcr for all rules
    posDF['Class'] = 1
    negDF['Class'] = -1
    giantDF = posDF.append(negDF)
    giantDF = giantDF.sort_values(by='Accuracy', ascending=False)
    giantDF.to_csv("../Rules/MCR/" + str(patient) + 'AllMCR.csv', index=False)


    #save top rules from giant DF into txt file
    vals = giantDF[giantDF['Accuracy'] > 0.8]
    bestRules = vals['Rule'].values

    with open("../Rules/Best/" + repr(patient) + "Rules.txt", 'w') as filehandle:
        for b in bestRules:
            filehandle.write('%s\n' % b)


def runMCRGenRules(patient):

    # Load all rules
    filepath = "Rules/ICU/" + str(patient) + "ruleScores.txt"
    posRules, negRules = readRulesFromFile(filepath)

    # Load Data
    data = pd.read_csv('Data/ICUDataFrames/' + str(patient) + 'DataFrame.csv', index_col=0)
    labels = pd.read_csv('Data/ICUDataFrames/' + str(patient) + 'Labels.csv')

    # Positive Rules MCR
    posDF, totalPatients = getMCRPosOutcome(posRules, data, labels)

    # Negative Rules MCR
    negDF, totalPatients = getMCRNegOutcome(negRules, data, labels)

    # posDF, negDF = addMisclassifiedRules(posDF, negDF, totalPatients)
    # print("\nPositive rules")
    # print(posDF)
    # print("\nNegative rules")
    # print(negDF)
    posDF.to_csv("Rules/MCR/" + str(patient) + 'PositiveMCR.csv', index=False)
    negDF.to_csv("Rules/MCR/" + str(patient) + 'NegativeMCR.csv', index=False)

    #make single file with mcr for all rules
    posDF['Class'] = 1
    negDF['Class'] = -1
    giantDF = posDF.append(negDF)
    giantDF = giantDF.sort_values(by='Accuracy', ascending=False)
    giantDF.to_csv("Rules/MCR/" + str(patient) + 'AllMCR.csv', index=False)


    #save top rules from giant DF into txt file
    vals = giantDF[giantDF['Accuracy'] > 0.80]
    bestRules = vals['Rule'].values
    print("LEN BEST RULES =", len(bestRules))

    with open("Rules/Best/" + repr(patient) + "Rules.txt", 'w') as filehandle:
        for b in bestRules:
            filehandle.write('%s' % b)



# Main Runner
def main():
    runMCR(patient=1)



if __name__ == '__main__':
    main()


