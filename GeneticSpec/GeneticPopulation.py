
#New class to store genetic population information, uses Genetic Generator to
class GeneticPopulation:
    def __init__(self, rankFormulae=[], rankParameters=[], rankScore=[]):
        self.rankFormulae = rankFormulae #list of formulas
        self.rankParameters = rankParameters #list of double param values
        self.rankScore = rankScore #list of score objects

    #Order formula by best score
    def sortPopulation(self):

        sortedFormula = [x for _, x in sorted(zip(self.rankScore, self.rankFormulae), key=lambda x: getattr(x[0], 'classDif'), reverse=True)]
        self.rankFormulae = sortedFormula

        sortedParams = [x for _, x in sorted(zip(self.rankScore, self.rankParameters), key=lambda x: getattr(x[0], 'classDif'), reverse=True)]
        self.rankParameters = sortedParams

        self.rankScore.sort(key=lambda x: x.classDif, reverse=True)

        # print("\nSorted")
        # for i in range(len(sortedFormula)):
        #     print(sortedFormula[i].toString(), self.rankScore[i].classDif)







#Class that holds all score values
class Score:
    def __init__(self, aveRobPos, varRobPos, aveRobNeg, varRobNeg, classDif ):
        self.aveRobPos = aveRobPos #ave pos robustness val
        self.varRobPos = varRobPos #ave pos robustness variance
        self.aveRobNeg  = aveRobNeg #ave neg robustness
        self.varRobNeg = varRobNeg #ave neg robustness variance
        self.classDif = classDif #discrimination function value, absolute dif of rob btw classes

    def toString(self):
        return "Discrimination Val: " + str(format(self.classDif, '.3f')) + " Robustness + : " + str(format(self.aveRobPos, '.3f')) \
               + " Robustness - :" + str(format(self.aveRobNeg, '.3f'))