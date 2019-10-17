import logging
from Learning import Learning

#make learning object
variables = ["cgm", "meal", "totalBolus", "basalBolus", "mealBolus", "corrBolus", "bgVal", "smbg", "smbgCal", "smbgHypo", "smbgTreat", "smbgTreatCarbs", "HR", "steps", "calories", "distance", "activityLevel"]
variables = ["x", "y", "v", "z"]

l = Learning(logging.INFO, "Data/values", "Data/labels", "Data/times", variables)


#start learning
l.runLearning()