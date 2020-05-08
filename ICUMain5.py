import logging
from Learning import Learning
from GeneticSpec.GeneticPopulation import GeneticPopulation
import MCR.CalculateMCR_ICU as mcr
import os.path

#make learning object
variables = ['LOS', 'ICU_Pt_Days', 'Mort', 'n_evts', 'y', 'tte', 'death', 'direct',
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

lower = [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00, -5.03298611e+01,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  1.00000000e+01,  0.00000000e+00,
        0.00000000e+00,  8.50000000e+01,  0.00000000e+00,  0.00000000e+00,
        3.50000000e+01,  1.30000000e+00,  1.90000000e+01,  6.00000000e+00,
        6.00000000e+00,  2.00000000e+00,  4.80000000e+00,  8.30000000e+01,
        7.00000000e+00,  3.00000000e-01,  4.90000000e+01,  2.20000000e+00,
        2.00000000e-01,  7.00000000e-01,  7.90000000e+01,  2.00000000e+01,
        1.65000000e+01,  9.00000000e-01,  1.00000000e+01,  1.90000000e+00,
        8.00000000e-01,  1.19000000e+02,  1.00000000e-01,  3.60000000e+00,
        2.00000000e-02,  1.20000000e-01,  3.00000000e+01, -7.62808303e-02,
       -7.62808303e-02, -7.62808303e-02,  0.00000000e+00,  4.68750236e+00,
       -1.90728029e-02, -1.90728029e-02, -1.90728029e-02,  1.06648029e-03,
       -9.69343118e-01, -3.23661607e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00] #lowerbound

upper = [1.22000000e+02, 1.04000000e+02, 1.00000000e+00, 4.00000000e+00,
       1.00000000e+00, 8.77861111e+01, 1.00000000e+00, 1.00000000e+00,
       1.00000000e+00, 1.00000000e+00, 1.50000000e+01, 7.00000000e+00,
       4.90000000e+01, 1.00000000e+02, 2.60000000e+02, 3.82000000e+02,
       4.05000000e+01, 5.00000000e+00, 3.86000000e+02, 3.56000000e+02,
       2.42000000e+02, 1.11000000e+02, 1.10000000e+01, 1.32000000e+02,
       4.00000000e+01, 1.00000000e+01, 4.60000000e+02, 2.02000000e+01,
       3.40000000e+00, 3.40000000e+00, 9.98000000e+01, 1.40000000e+02,
       6.76000000e+01, 8.00000000e+00, 6.62000000e+02, 8.30000000e+00,
       5.00000000e+00, 1.51000000e+02, 9.00000000e+00, 9.70000000e+00,
       2.35000000e+01, 2.60000000e+01, 3.00000000e+02, 6.86283741e-02,
       6.86283741e-02, 6.86283741e-02, 1.00000000e+00, 5.43110090e+01,
       1.69365926e-02, 1.69365926e-02, 1.69365926e-02, 6.05001092e-01,
       2.22452357e+00, 8.51720869e-01, 4.49814800e+00, 1.00000000e+00,
       1.00000000e+00] # upperbound

for i in range(5000,6000):
    print("Patient: ", i)

    dataName =  "Data/ICUData/" + repr(i) + ".txt"
    labelName = "Data/ICUData/" + repr(i) + "labels.txt"

    if os.path.exists(dataName):

        l = Learning(logging.INFO, dataName, labelName, "Data/ICUData/time.txt", variables, lower, upper)

        #start learning
        generation = l.run()

        print("Saving Rules")

        #save rules and scores to file
        ruleScores = generation.finalFormulaScoresToString(500)
        with open("Rules/ICU/" + repr(i) + "ruleScores.txt", 'w') as filehandle:
            for r in ruleScores:
                filehandle.write('%s\n' % r)

        #save rules themselves
        rules = generation.finalFormulasToString(500)

        with open("Rules/ICU/" + repr(i) + "rules.txt", 'w') as filehandle:
            for r in rules:
                filehandle.write('%s\n' % r)


        #calculate MCR
        print("Running MCR")
        mcr.runMCR(i)