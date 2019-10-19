from SymbolArray import SymbolArray

class FormulaPopulation:
    def __init__(self, popSize):
        self.popSize = popSize

        self.population = [] #arrayList of formulas
        self.fitness = None
        self.model1 = None
        self.model2 = None
        self.lowerBound = {} #hashmap of key value pairs string, double
        self.upperBound = {} #hashmap of key value pairs string, double

        self.parameters = SymbolArray()
        #store = new FastStore();

        self.variables = [] #arrayList of strings

        #operators = new FormulaGenOps(this, parameters);
        #bestSolutions = new TreeSet < Solution > ();
        #setFitness(GeneticOptions.fitness_type);


    def addVariable(self, v, lower, upper):
        #store.addVariable(V, 0);
        self.variables.append(v)
        self.lowerBound[v] = lower
        self.upperBound[v] = upper

    def addGeneticInitFormula(self, varSize):
        pass
        #List < Formula > formulas = operators.atomicGeneticFormula(n);
        #self.population.addAll(formulas)