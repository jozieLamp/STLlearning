import csv
import pprint
import pandas
import numpy as np

# vals = []
# labelsHosp = []
# labelsDeath = []
# labelsBoth = []
#
# with open('hemoChangesOriginal.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for line in csv_reader:
#         base = []
#         final = []
#         for i in range(len(line)):
#             if i == 0: #DEID Num
#                 base.append(line[i])
#                 final.append(line[i])
#             elif i == 79:
#                 labelsHosp.append([line[i]])
#             elif i == 80:
#                 labelsDeath.append([line[i]])
#             elif i == 81:
#                 labelsBoth.append([line[i]])
#             elif i % 2 == 0.0: #even
#                 final.append(line[i])
#             else: #odd
#                 base.append(line[i])
#         vals.append(base)
#         vals.append(final)
#
# print(vals)
# print(labelsHosp)
# print(labelsDeath)
# print(labelsBoth)
#
# with open('hemoChanges.csv', 'w') as csvFile:
#     writer = csv.writer(csvFile)
#     writer.writerows(vals)
#
# csvFile.close()
#
# with open('labelsRehosp.csv', 'w') as csvFile:
#     writer = csv.writer(csvFile)
#     writer.writerows(labelsHosp)
#
# csvFile.close()
#
# with open('labelsDeath.csv', 'w') as csvFile:
#     writer = csv.writer(csvFile)
#     writer.writerows(labelsDeath)
#
# csvFile.close()
#
# with open('labelsBoth.csv', 'w') as csvFile:
#     writer = csv.writer(csvFile)
#     writer.writerows(labelsBoth)
#
# csvFile.close()




# format to be in 3D

#matlab code
# data = hemo1{:,2:10};
# time = [1,2];
# # this is slices x time x attributeNum
# data = permute(reshape(data, 433, 2, 9), [1 3 2]);
# In ACTUAL order: slices x attributes x time


#make 3d array of zeros
numSlices = 433
numTime = 2
numAttb = 39

data = [[[0 for k in range(numAttb)] for j in range(numTime)] for i in range(numSlices)]
#to access values in 3d array: data[slice][time][attributeNumber]

# #print array dimensions
# for x in range(len(data)):
#     print(data[x])

# with open('hemo1_noHeader.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     for line in csv_reader:


df = pandas.read_csv('hemoChanges.csv')
print(df)

#row col
# t = df.iloc[0, 8]
# print(t)

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
with open('cDataChanges.txt', 'w') as outfile:
    for x in range(len(data)):
        for i in range(numTime):
            line = line + data[x][i]
        line = [line]
        np.savetxt(outfile, line, delimiter=',', fmt='%.2f')
        line = []