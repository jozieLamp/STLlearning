import logging
from Learning import Learning
from GeneticSpec.GeneticPopulation import GeneticPopulation


#make learning object
variables = ["x", "y", "v", "z"]
lower = [0, 0, 0, 0] #lowerbound
upper = [80, 45, 80, 45] # upperbound

l = Learning(logging.INFO, "Data/values", "Data/labels", "Data/times", variables, lower, upper)


#start learning
generation = l.run()
