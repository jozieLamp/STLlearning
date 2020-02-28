import FormulaSpec.FormulaGenerator as FG
import logging
import treelib
import random
from SignalTemporalLogic.STLFactory import STLFactory
import re

#Class to hold populations of formulas, uses Formula Generator class to generate formulas themselves
class FormulaPopulation:
    def __init__(self, popSize, varDict={}, paramDict={}):
        self.popSize = popSize
        self.varDict = varDict #dictionary- VarName key: {lower bound, upper bound}
        self.paramDict  = paramDict #dictionary- paramName key: {list of param values}
        self.formulaGen = FG.FormulaGenerator() #class to generate formula sets

        self.population = [] #arrayList of formulas
        self.lowerBound = {} #hashmap of key value pairs string, double
        self.upperBound = {} #hashmap of key value pairs string, double
        self.variables = [] #arrayList of strings

    #Add variables to formula pop store
    def addVariable(self, v, lower, upper):
        #store.addVariable(V, 0);
        self.variables.append(v)
        self.lowerBound[v] = lower
        self.upperBound[v] = upper

    # Generate initial atomic formulas of G, F, U for each variable
    # Creates formulas with no params, just rule structure
    def addGeneticInitFormula(self, genOps):
        initialFormula = self.formulaGen.atomicGeneticFormula(variables=self.variables, genOps=genOps)
        self.population.extend(initialFormula)
        self.logFormulas(initialFormula, "Initial")
        logging.info("New size of population is " + '%s' % (len(self.population)) + " formulas \n")


    def addRandomInitFormula(self, genOps):
        rFormulas = []
        for i in range(genOps.max_num_rand):
            randFormula = self.formulaGen.randomFormula(variables=self.variables, varDict=self.varDict, genOps=genOps)
            rFormulas.append(randFormula)
        self.population.extend(rFormulas)
        self.logFormulas(rFormulas, "Random")
        logging.info("New size of population is " + '%s' % (len(self.population)) + " formulas \n")

    def logFormulas(self, pop, type):
        logging.info(type + " Formula Population:")

        for f in pop:
            if f  != None:
                logging.info('%s' % (f.toString()))
        #logging.info("---------------------------------------------------\n")


    #swap two internal nodes between formulas
    def crossoverNewGen(self, formulaA, formulaB):
        nodeA = formulaA.getNodeToCrossover()
        nodeB = formulaB.getNodeToCrossover()

        # print(nodeA.toString())
        # print(nodeB.toString())

        stringA = formulaA.toString().replace(nodeA.toString(), nodeB.toString())
        stringB = formulaB.toString().replace(nodeB.toString(), nodeA.toString())

        boolCount = stringA.count("&")
        boolCount += stringA.count("|")
        boolCount += stringA.count("->")

        if boolCount >= 2:
            stringA = self.fixBoolExpr(stringA)

        boolCount = stringB.count("&")
        boolCount += stringB.count("|")
        boolCount += stringB.count("->")

        if boolCount >= 2:
            stringB = self.fixBoolExpr(stringB)


        stlFac = STLFactory()
        f1 = stlFac.constructFormulaTree(stringA + "\n")
        f2 = stlFac.constructFormulaTree(stringB + "\n")

        return f1, f2



    #mutate a formula
    def mutateNewGen(self, formula, genOps, variables, varDict):

        node, parentNode = formula.getNodeToMutate()

        stlFac = STLFactory()
        newNode, newFormula = self.formulaGen.mutateNode(node=node, parentNode=parentNode, formula=formula, genOps=genOps, variables=variables, varDict=varDict)
        #print("Mutated Formula", newFormula)


        if newFormula != None:
            boolCount = newFormula.count("&")
            boolCount += newFormula.count("|")
            boolCount += newFormula.count("->")

            if boolCount >= 2:
                newFormula = self.fixBoolExpr(newFormula)

            finalFormula = stlFac.constructFormulaTree(newFormula + "\n")
        else:
            finalFormula = None

        return finalFormula


    #combine two formulas with boolean operators
    def unionNewGen(self, formulaA, formulaB):
        stringA = formulaA.toString()
        stringB = formulaB.toString()

        if stringA != None and stringB != None:

            newAnd = "(" + stringA + " & " + stringB + ")\n"
            newOr = "(" + stringA + " | " + stringB + ")\n"
            newImplies = "(" + stringA + " -> " + stringB + ")\n"

            stlFac = STLFactory()
            f1 = stlFac.constructFormulaTree(newAnd)
            f2 = stlFac.constructFormulaTree(newOr)
            f3 = stlFac.constructFormulaTree(newImplies)
            return f1, f2, f3
        else:
            return None, None, None


    def fixBoolExpr(self, text):
        numParen = text.count("(")
        symbols = re.findall('\||&|->', text)
        lastSymbol = symbols[len(symbols) - 1]
        res = text.rpartition(lastSymbol)
        parens = ")" * numParen
        end = res[2].replace(")","")

        finalRet = "(" + res[0] + parens + " " + res[1] + " " + end + ")"
        #Check for mismatched parens
        fP = finalRet.count("(")
        bP = finalRet.count(")")
        if bP > fP:
            difParen = bP - fP
            for i in range(difParen):
                # finalRet = finalRet[:-1] #remove last paren
                res = finalRet.rpartition(")")
                finalRet = res[0] + res[2]

            return finalRet
        else:
            return finalRet

