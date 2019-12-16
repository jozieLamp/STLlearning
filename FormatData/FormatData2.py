import csv
import pprint
import pandas
import numpy as np

vals = []
labelsHosp = []
labelsDeath = []
labelsBoth = []

base1 = []
base2 = []
base3 = []
base4 = []
base5 = []
base6 = []
base7 = []
base8 = []
base9 = []
base0 = []


with open('hemoLabs1.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for line in csv_reader:
        vars = []

        count = 0
        for i in range(len(line)):
            if i == 121:
                labelsHosp.append([line[i]])
            else:

                if count == 10:

                    base0.append(vars[0])
                    base1.append(vars[1])
                    base2.append(vars[2])
                    base3.append(vars[3])
                    base4.append(vars[4])
                    base5.append(vars[5])
                    base6.append(vars[6])
                    base7.append(vars[7])
                    base8.append(vars[8])
                    base9.append(vars[9])
                    vars = []
                    count = 0


                vars.append(line[i])
                count = count + 1


        vals.append([base0])
        vals.append([base1])
        vals.append([base2])
        vals.append([base3])
        vals.append([base4])
        vals.append([base5])
        vals.append([base6])
        vals.append([base7])
        vals.append([base8])
        vals.append([base9])



        base0 = []
        base2 = []
        base3 = []
        base4 = []
        base5 = []
        base6 = []
        base7 = []
        base8 = []
        base9 = []





# print(vals)
print(labelsHosp)
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


# #make 3d array of zeros
# numSlices = 433
# numTime = 2
# numAttb = 27
#
# data = [[[0 for k in range(numAttb)] for j in range(numTime)] for i in range(numSlices)]
# #to access values in 3d array: data[slice][time][attributeNumber]
#
# # #print array dimensions
# # for x in range(len(data)):
# #     print(data[x])
#
# # with open('hemo1_noHeader.csv') as csv_file:
# #     csv_reader = csv.reader(csv_file, delimiter=',')
# #     for line in csv_reader:
#
#
# df = pandas.read_csv('hemoChanges_noHeader.csv')
# print(df)
#
# #row col
# # t = df.iloc[0, 8]
# # print(t)
#
# #load data into 3d array
# dfRowCount=0
# for s in range(numSlices):
#     for t in range(numTime):
#         for a in range(numAttb):
#             data[s][t][a] = df.iloc[dfRowCount, a]
#         dfRowCount += 1
#
# #print 3d result
# # for x in range(len(data)):
# #     print(data[x])
#
#
# #save into txt file
# line = []
# with open('cDataChanges.txt', 'w') as outfile:
#     for x in range(len(data)):
#         for i in range(numTime):
#             line = line + data[x][i]
#         line = [line]
#         np.savetxt(outfile, line, delimiter=',', fmt='%.2f')
#         line = []