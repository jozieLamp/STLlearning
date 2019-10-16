import logging
from Learning import Learning

#make learning object
l = Learning(logging.INFO, "Data/values", "Data/labels", "Data/times")

#start learning
l.runLearning()