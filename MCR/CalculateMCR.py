
from SignalTemporalLogic.STLFactory import STLFactory
import pandas as pd

def main():
    factory = STLFactory()

    rule = "G[1,2](PCPWMN >= 2.239 & !(PASChange >= 25.630)) & BPSYSChange >= -81.566\n"

    ft = factory.constructFormulaTree(rule)
    ft.show()
    ft.toString()

    # Load Data

    absData = pd.read_csv('MCR/AbsChanges.csv', index_col=0)
    absDataLabelsR = pd.read_csv('MCR/AbsChangesRehospLabels.csv', index_col=0)
    absDataLabelsD = pd.read_csv('MCR/AbsChangesDeathLabels.csv', index_col=0)
    test = absData.loc[81]


    val = ft.evaluateTruthValue(test)
    print("\nReturned Value", val)

if __name__ == '__main__':
    main()
