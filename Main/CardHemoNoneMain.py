import logging
from Learning import Learning
from GeneticSpec.GeneticPopulation import GeneticPopulation

for i in range(11):
    #DEATH LABELS


    #make learning object
    variables = ['HEM', 'PLA', 'HEC', 'WBC', 'SOD', 'POT', 'BUN', 'CRT', 'ALT', 'TOTP',
           'ALB', 'TALB', 'DIN', 'DOB', 'DOP', 'MIL', 'NIG', 'DIGX', 'ACE', 'BET',
           'ANGIOT', 'Walk', 'VO2']

    lower = [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 0., 0., 0., 0., 0.] #lowerbound

    upper = [1.820e+01, 5.760e+02, 5.330e+02, 8.300e+01, 1.480e+02, 6.900e+00,
           1.390e+02, 8.200e+00, 1.037e+03, 1.480e+01, 8.200e+00, 2.300e+00,
           2.400e+02, 1.000e+01, 3.000e+00, 5.000e-01, 5.000e+01, 1.250e+02,
           1.000e+00, 1.000e+00, 1.000e+00, 2.420e+03, 2.750e+01] # upperbound

    l = Learning(logging.INFO, "../Data/Card/cardDataHemoNone.txt", "../Data/Card/cardDeathLabelsHemoNone.txt", "../Data/Card/cardTimeHemoNone.txt", variables, lower, upper)


    #start learning
    generation = l.run()

    # save rules and scores to file
    nameScores = "CardHemoNoneScoresDeath" + str(i) + ".txt"
    ruleScores = generation.finalFormulaScoresToString(500)
    with open(nameScores, 'w') as filehandle:
        for r in ruleScores:
            filehandle.write('%s\n' % r)

    # save rules themselves
    rules = generation.finalFormulasToString(500)

    nameRules = "CardHemoNoneRuleDeath" + str(i) + ".txt"
    with open(nameRules, 'w') as filehandle:
        for r in rules:
            filehandle.write('%s\n' % r)


    #REHOSP
    l = Learning(logging.INFO, "../Data/Card/cardDataHemoNone.txt", "../Data/Card/cardRehospLabelsHemoNone.txt",
                 "../Data/Card/cardTimeHemoNone.txt", variables, lower, upper)

    # start learning
    generation = l.run()

    # save rules and scores to file
    nameScores = "CardHemoNoneScoresRehosp" + str(i) + ".txt"
    ruleScores = generation.finalFormulaScoresToString(500)
    with open(nameScores, 'w') as filehandle:
        for r in ruleScores:
            filehandle.write('%s\n' % r)

    # save rules themselves
    rules = generation.finalFormulasToString(500)

    nameRules = "CardHemoNoneRuleRehosp" + str(i) + ".txt"
    with open(nameRules, 'w') as filehandle:
        for r in rules:
            filehandle.write('%s\n' % r)



