import logging
import random

#New class to store genetic population information, uses Genetic Generator to
class GeneticPopulation:
    def __init__(self, rankFormulae=[], rankParameters=[], rankScore=[]):
        self.rankFormulae = rankFormulae #list of formulas
        self.rankParameters = rankParameters #list of double param values
        self.rankScore = rankScore #list of score objects

    def logRankFormulas(self):
        for i in range(len(self.rankFormulae)):
            st = self.rankFormulae[i].toString() + " [Discrimination Score: " + str(format(self.rankScore[i].classDif, '.3f') + "]")
            logging.info(st)

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

    def getBestHalf(self):
        half = round(len(self.rankFormulae) / 2)
        halfFormulas = self.rankFormulae[:half]
        halfParams = self.rankParameters[:half]
        halfScores = self.rankScore[:half]

        return GeneticPopulation(halfFormulas, halfParams, halfScores)

    def geneticOperations(self, pop): #takes formula population

        scoreParents = self.rankScore
        formulaParents = self.rankFormulae

        difScores = self.getAllClassScores(scoreParents)

        #calculate cumulative score array
        cmlScores = self.cumulativeScore(difScores)

        #parent A
        indexA = self.extract(cmlScores)
        #parent B
        indexB = indexA

        while indexB == indexA:
            indexB = self.extract(cmlScores)

        r = random.uniform(0,1)
        r = 0.6
        if r > 0.3:

            formulaA = formulaParents[indexA]
            formulaB  = formulaParents[indexB]
            print("Formula A", formulaA.toString())
            print("FOrmula B", formulaB.toString())

            #crossover/recombination operator, modify both new A and new B
            f = pop.crossoverNewGen(formulaA, formulaB) #TODO

            #pop.population.append(f)

        elif r > 0.0:
            newIndexA = pop.addNewFormula(formulaParents[indexA])  # TODO complete  tthis
            newIndexB = pop.addNewFormula(formulaParents[indexB])

            #mutation operator
            pop.mutateNewGen(newIndexB) #TODO
            pop.mutateNewGen(newIndexA)

        else:
            newIndexA = pop.addNewFormula(formulaParents[indexA])  # TODO complete  tthis
            newIndexB = pop.addNewFormula(formulaParents[indexB])

            #union formula sets
            pop.unionNewGen(newIndexA, newIndexB) #TODO




    def extract(self, cmlScores):
        r = random.uniform(0,1)
        for i in range(len(cmlScores)):
            if cmlScores[i] > r:
                return i - 1

        return len(cmlScores)-1


    def cumulativeScore(self, scores):
        res = [0] * len(scores)
        for i in range(1,len(scores)):
            res[i] = res[i-1] + scores[i-1]

        for i in range(len(scores)):
            res[i] = res[i] / res[len(scores)-1]

        return res

    #Return class diff scores from score object
    def getAllClassScores(self, scores):
        c = []
        for sc in scores:
            c.append(sc.classDif)

        return c

#Class that holds all score values
class Score:
    def __init__(self, aveRobPos, varRobPos, aveRobNeg, varRobNeg, classDif ):
        self.aveRobPos = aveRobPos #ave pos robustness val
        self.varRobPos = varRobPos #ave pos robustness variance
        self.aveRobNeg  = aveRobNeg #ave neg robustness
        self.varRobNeg = varRobNeg #ave neg robustness variance
        self.classDif = classDif #discrimination function value, absolute dif of rob btw classes

    def toString(self):
        return "Discrimination Score: " + str(format(self.classDif, '.3f')) + " Robustness + : " + str(format(self.aveRobPos, '.3f')) \
               + " Robustness - :" + str(format(self.aveRobNeg, '.3f'))
