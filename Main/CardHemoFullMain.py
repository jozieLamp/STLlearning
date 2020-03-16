import logging
from Learning import Learning
from GeneticSpec.GeneticPopulation import GeneticPopulation

for i in range(11):
    #DEATH LABELS

    #make learning object
    variables = ['HEM', 'PLA', 'HEC', 'WBC', 'SOD', 'POT', 'BUN', 'CRT', 'ALT', 'TOTP',
           'ALB', 'TALB', 'DIN', 'DOB', 'DOP', 'MIL', 'NIG', 'DIGX', 'ACE', 'BET',
           'ANGIOT', 'Walk', 'VO2', 'RAP', 'PAS', 'PAD', 'PCWP', 'PCPWMN', 'CI',
           'BPSYS', 'BPDIAS', 'HR', 'RAPChange', 'PASChange', 'PADChange',
           'PCWPChange', 'PCPWMNChange', 'CIChange', 'BPSYSChange', 'BPDIASChange',
           'HRChange']

    lower = [   0. ,    0. ,    0. ,    0. ,    0. ,    0. ,    0. ,    0. ,
              0. ,    0. ,    0. ,    0. ,    0. ,    0. ,    0. ,    0. ,
              0. ,    0. ,    0. ,    0. ,    0. ,    0. ,    0. ,    0. ,
              0. ,    0. ,    0. ,    0. ,    0. ,    0. ,    0. ,    0. ,
            -24. ,  -85. ,  -45. ,  -40. ,  -35. ,   -3.4, -150. , -108. ,
           -113. ] #lowerbound

    upper = [9.900e+01, 5.760e+02, 5.330e+02, 8.500e+01, 1.480e+02, 6.900e+00,
           1.390e+02, 1.000e+01, 1.037e+03, 1.480e+01, 8.200e+00, 2.300e+00,
           2.400e+02, 1.000e+01, 3.000e+00, 5.000e-01, 5.000e+01, 1.250e+02,
           1.000e+00, 1.000e+00, 1.000e+00, 2.420e+03, 2.750e+01, 2.800e+01,
           8.500e+01, 4.500e+01, 4.000e+01, 3.700e+01, 3.400e+00, 1.540e+02,
           1.080e+02, 1.250e+02, 9.000e+00, 4.600e+01, 2.600e+01, 2.200e+01,
           2.200e+01, 3.100e+00, 1.100e+02, 6.800e+01, 9.400e+01] # upperbound

    l = Learning(logging.INFO, "../Data/Card/cardDataHemoFull.txt", "../Data/Card/cardDeathLabelsHemoFull.txt", "../Data/Card/cardTimeHemoFull.txt", variables, lower, upper)


    #start learning
    generation = l.run()

    # save rules and scores to file
    nameScores = "CardHemoFullScoresDeath" + str(i) + ".txt"
    ruleScores = generation.finalFormulaScoresToString(500)
    with open(nameScores, 'w') as filehandle:
        for r in ruleScores:
            filehandle.write('%s\n' % r)

    # save rules themselves
    rules = generation.finalFormulasToString(500)

    nameRules = "CardHemoFullRuleDeath" + str(i) + ".txt"
    with open(nameRules, 'w') as filehandle:
        for r in rules:
            filehandle.write('%s\n' % r)


    #REHOSP Labels
    l = Learning(logging.INFO, "../Data/Card/cardDataHemoFull.txt", "../Data/Card/cardRehospLabelsHemoFull.txt", "../Data/Card/cardTimeHemoFull.txt", variables, lower, upper)

    # save rules and scores to file
    nameScores = "CardHemoFullScoresRehosp" + str(i) + ".txt"
    ruleScores = generation.finalFormulaScoresToString(500)
    with open(nameScores, 'w') as filehandle:
        for r in ruleScores:
            filehandle.write('%s\n' % r)

    # save rules themselves
    rules = generation.finalFormulasToString(500)

    nameRules = "CardHemoFullRehosp" + str(i) + ".txt"
    with open(nameRules, 'w') as filehandle:
        for r in rules:
            filehandle.write('%s\n' % r)
