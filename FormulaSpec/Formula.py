from FormulaSpec import Operator
# class Time:
#     def __init__(self, lowerBound = 000, upperBound = 000):
#         self.lowerBound = lowerBound
#         self.upperBound =  upperBound

#Formula definition
class Formula:
    #Most basic formula (x <= value)
    def __init__(self, temporalOperator, boolOperator=None, paramList=[]):
        self.boolOperator = boolOperator
        self.temporalOperator = temporalOperator
        self.paramList = paramList

    def printFormula(self):
        pass

class Formula_G(Formula):
    def __init__(self, temporalOperator=Operator.Operator_G(), boolOperator=None, paramList=[]):
        self.temporalOperator  = temporalOperator
        self.timeBound = self.temporalOperator.timeBound
        self.boolOperator = boolOperator
        self.paramList = paramList

    def toString(self):
        #convert time to correct formats
        if isinstance(self.timeBound[0], str):
            timeLow = self.timeBound[0]
            timeHigh = self.timeBound[1]
        else: # type(self.timeBound[0]) == 'int' or type(self.timeBound[0]) == 'float':
            timeLow = format(self.timeBound[0], '.3f')
            timeHigh = format(self.timeBound[1], '.3f')

        #convert param vals to correct formats
        if isinstance(self.paramList[0].value,str):
            p0 = self.paramList[0].value
            if len(self.paramList) != 1:
                p1 = self.paramList[1].value
        else:
            p0 = format(self.paramList[0].value, '.3f')
            if len(self.paramList) != 1:
                p1 =  format(self.paramList[1].value, '.3f')

        if self.boolOperator == None:
            if len(self.paramList) == 1:
                statement = self.temporalOperator.type.name + "[" + timeLow+ "," + timeHigh + "] " + "(" + self.paramList[0].name + " " + self.paramList[0].sign + " " + p0 + ")"
        else:
            statement = self.temporalOperator.type.name + "[" + timeLow + "," + timeHigh + "] " + "(" + self.paramList[0].name + " " + self.paramList[0].sign + " " + p0 + " " + self.boolOperator.type.name + " " + self.paramList[1].name + " " + self.paramList[1].sign + " " + p1 + ")"

        return statement

    def printFormula(self):
        print(self.toString())


class Formula_F(Formula):
    def __init__(self, temporalOperator=Operator.Operator_F(), boolOperator=None, paramList=[]):
        self.temporalOperator  = temporalOperator
        self.timeBound = self.temporalOperator.timeBound
        self.boolOperator = boolOperator
        self.paramList = paramList

    def toString(self):
        # convert time to correct formats
        if isinstance(self.timeBound[0], str):
            timeLow = self.timeBound[0]
            timeHigh = self.timeBound[1]
        else: #type(self.timeBound[0] == 'int') or type(self.timeBound[0]) == 'float':
            timeLow = format(self.timeBound[0], '.3f')
            timeHigh = format(self.timeBound[1], '.3f')

        # convert param vals to correct formats
        if isinstance(self.paramList[0].value, str):
            p0 = self.paramList[0].value
            if len(self.paramList) != 1:
                p1 = self.paramList[1].value
        else:
            p0 = format(self.paramList[0].value, '.3f')
            if len(self.paramList) != 1:
                p1 = format(self.paramList[1].value, '.3f')

        if self.boolOperator == None:
            if len(self.paramList) == 1:
                statement = self.temporalOperator.type.name + "[" + timeLow + "," + timeHigh + "] " + "(" + self.paramList[0].name + " " + self.paramList[0].sign + " " + p0 + ")"
        else:
            statement = self.temporalOperator.type.name + "[" + timeLow + "," + timeHigh + "] " + "(" + self.paramList[0].name + " " + self.paramList[0].sign + " " + p0 + " "+ self.boolOperator.type.name + " " + self.paramList[1].name + " " + self.paramList[1].sign + " " + p1 + ")"

        return statement

    def printFormula(self):
        print(self.toString())


class Formula_U(Formula):
    def __init__(self, temporalOperator=Operator.Operator_U(), boolOperator=None, paramList=[]):
        self.temporalOperator  = temporalOperator
        self.timeBound = self.temporalOperator.timeBound
        self.boolOperator = boolOperator
        self.paramList = paramList

    def toString(self):
        # convert time to correct formats
        if isinstance(self.timeBound[0], str):
            timeLow = self.timeBound[0]
            timeHigh = self.timeBound[1]
        else: # type(self.timeBound[0] == 'int' or self.timeBound[0] == 'double'):
            timeLow = format(self.timeBound[0], '.3f')
            timeHigh = format(self.timeBound[1], '.3f')

        # convert param vals to correct formats
        if isinstance(self.paramList[0].value, str):
            p0 = self.paramList[0].value
            if len(self.paramList) != 1:
                p1 = self.paramList[1].value
        else:
            p0 = format(self.paramList[0].value, '.3f')
            if len(self.paramList) != 1:
                p1 = format(self.paramList[1].value, '.3f')

        statement = "(" + self.paramList[0].name + " " + self.paramList[0].sign + " " + p0 + ") " + self.temporalOperator.type.name + "[" + timeLow + "," + timeHigh + "] " + "(" + self.paramList[1].name + " " + self.paramList[1].sign + " " + p1 + ")"

        return statement

    def printFormula(self):
        print(self.toString())

class AdvancedFormula():
    def __init__(self, temporalOperator, boolOperator, paramList=[]):
        self.temporalOperator  = temporalOperator
        self.timeBound = self.temporalOperator.timeBound
        self.boolOperator = boolOperator
        self.paramList = paramList