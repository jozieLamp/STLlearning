import logging
from Learning import Learning
from GeneticSpec.GeneticPopulation import GeneticPopulation


#make learning object
variables = ['HEM', 'PLA', 'HEC', 'WBC', 'SOD', 'POT', 'BUN', 'CRT', 'ALT', 'TOTP',
       'ALB', 'TALB', 'DIN', 'DOB', 'DOP', 'MIL', 'NIG', 'DIGX', 'ACE', 'BET',
       'ANGIOT', 'Walk', 'VO2', 'RAP', 'PAS', 'PAD', 'PCWP', 'PCPWMN', 'CI',
       'BPSYS', 'BPDIAS', 'HR', 'RAPChange', 'PASChange', 'PADChange',
       'PCWPChange', 'PCPWMNChange', 'CIChange', 'BPSYSChange', 'BPDIASChange',
       'HRChange']

lower =[   0. ,    0. ,    0. ,    0. ,    0. ,    0. ,    0. ,    0. ,
          0. ,    0. ,    0. ,    0. ,    0. ,    0. ,    0. ,    0. ,
          0. ,    0. ,    0. ,    0. ,    0. ,    0. ,    0. ,    0. ,
          0. ,    0. ,    0. ,    0. ,    0. ,    0. ,    0. ,    0. ,
        -83. ,  -90. ,  -59. ,  -40. ,  -40. ,   -4.5, -150. , -108. ,
       -113. ] #lowerbound

upper = [9.900e+01, 7.070e+02, 5.330e+02, 8.500e+01, 1.480e+02, 8.000e+00,
       1.390e+02, 1.000e+01, 1.037e+03, 1.480e+01, 8.200e+00, 2.400e+00,
       2.700e+02, 1.000e+01, 3.000e+00, 2.500e+00, 5.000e+01, 1.250e+02,
       1.000e+00, 1.000e+00, 1.000e+00, 2.420e+03, 2.750e+01, 8.500e+01,
       9.000e+01, 5.900e+01, 5.300e+01, 4.900e+01, 4.810e+00, 1.680e+02,
       1.250e+02, 1.250e+02, 2.000e+01, 5.800e+01, 2.600e+01, 3.200e+01,
       2.600e+01, 3.100e+00, 1.100e+02, 6.800e+01, 9.400e+01] # upperbound

l = Learning(logging.INFO, "Data/Card/cardDataChanges.txt", "Data/Card/cardRehospLabels.txt", "Data/Card/cardTimeChanges.txt", variables, lower, upper)


#start learning
generation = l.run()

#save rules and scores to file
ruleScores = generation.finalFormulaScoresToString(200)
with open("CardChangesRuleScores.txt", 'w') as filehandle:
    for r in ruleScores:
        filehandle.write('%s\n' % r)

#save rules themselves
rules = generation.finalFormulasToString(200)

with open("CardChangesRules.txt", 'w') as filehandle:
    for r in rules:
        filehandle.write('%s\n' % r)

