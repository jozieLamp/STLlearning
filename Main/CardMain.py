import logging
from Learning import Learning
from GeneticSpec.GeneticPopulation import GeneticPopulation


#make learning object
variables = ['HEM', 'PLA', 'HEC', 'WBC', 'SOD', 'POT', 'BUN', 'CRT', 'ALT', 'TOTP',
       'ALB', 'TALB', 'DIN', 'DOB', 'DOP', 'MIL', 'NIG', 'DIGX', 'ACE', 'BET',
       'ANGIOT', 'Walk', 'VO2', 'RAP', 'PAS', 'PAD', 'PCWP', 'PCPWMN', 'CI',
       'BPSYS', 'BPDIAS', 'HR']

lower = [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
       0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.] #lowerbound

upper = [9.900e+01, 8.370e+02, 5.330e+02, 1.300e+02, 1.480e+02, 8.000e+00,
       1.670e+02, 1.000e+01, 1.037e+03, 1.480e+01, 8.200e+00, 2.400e+00,
       2.700e+02, 1.000e+01, 3.000e+00, 2.500e+00, 5.000e+01, 1.250e+02,
       1.000e+00, 1.000e+00, 1.000e+00, 2.420e+03, 2.750e+01, 8.500e+01,
       9.000e+01, 5.900e+01, 7.800e+01, 7.800e+01, 4.810e+00, 1.680e+02,
       1.250e+02, 1.280e+02] # upperbound

l = Learning(logging.INFO, "Data/Card/cardData.txt", "Data/Card/cardRehospLabels.txt", "Data/Card/cardTime.txt", variables, lower, upper)


#start learning
generation = l.run()

#save rules and scores to file
ruleScores = generation.finalFormulaScoresToString(200)
with open("CardRuleScores.txt", 'w') as filehandle:
    for r in ruleScores:
        filehandle.write('%s\n' % r)

#save rules themselves
rules = generation.finalFormulasToString(200)

with open("CardRules.txt", 'w') as filehandle:
    for r in rules:
        filehandle.write('%s\n' % r)

