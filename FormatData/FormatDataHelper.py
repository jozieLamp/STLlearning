import csv
import pprint
import pandas as pd
import numpy as np

from math import floor

#Load Data
fullData = pd.read_csv("testData.csv", sep=",")
fullData = fullData.fillna(0)

time = fullData["Time"]
labels = fullData["Label"]
df = fullData.drop(columns=["Time","Label"])

totalTime = len(time)

numAttb = len(df.columns)
numTime = 5
numSlices = floor(totalTime / numTime)

print("Num Slices:", numSlices, "Num Time:", numTime, "Num Attributes:", numAttb)

# make labels:
print(len(labels))
labelArray = []
ct = 0
vals = []
for i in range(len(labels)):
    vals.append(labels[i])
    ct += 1

    if ct == numTime:
        print("vaals", vals)
        sumV = sum(vals)
        if sumV < 0:
            labelArray.append(-1)
        else:
            labelArray.append(1)
        vals = []
        ct = 0

print("Labels", labelArray)
print(len(labelArray))

#make time
timeArray = list(range(numTime))
print("Time", timeArray)

# format to be in 3D

#make 3d array of zeros
data = [[[0 for k in range(numAttb)] for j in range(numTime)] for i in range(numSlices)]
print(len(data))
#to access values in 3d array: data[slice][time][attributeNumber]

# #print array dimensions
# for x in range(len(data)):
#     print(data[x])


#load data into 3d array
dfRowCount=0
for s in range(numSlices):
    for t in range(numTime):
        for a in range(numAttb):
            data[s][t][a] = df.iloc[dfRowCount, a]
        dfRowCount += 1

#print 3d result
# for x in range(len(data)):
#     print(data[x])


#save into txt file

line = []
with open('testData.txt', 'w') as outfile:
    for x in range(len(data)):
        for i in range(numTime):
            line = line + data[x][i]
        line = [line]
        np.savetxt(outfile, line, delimiter=',', fmt='%.2f')
        line = []

with open('testLabels.txt', 'w') as filehandle:
    for l in labelArray:
        filehandle.write('%s\n' % l)

with open('testTime.txt', 'w') as filehandle:
    for t in timeArray:
        filehandle.write('%s\n' % t)
