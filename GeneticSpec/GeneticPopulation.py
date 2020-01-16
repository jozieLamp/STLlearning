
#New class to store genetic population information, uses Genetic Generator to
class GeneticPopulation:
    def __init__(self, rankFormulae=[], rankParameters=[], rankScore=[]):
        self.rankFormulae = rankFormulae #list of formulas
        self.rankParameters = rankParameters #list of double param values
        self.rankScore = rankScore #list of double score values