
Preliminaries:

The tool requires 3 text files: Data, Labels and Times
DATA
    Data is a 3D array of variables.
    The dimensions are: numberSlices x timePerSlice x numberAttributes
    For example, say we have a data set with a total of 10,000 time points and 20 attributes. We wish to have 2 time points per slice.
    Therefore, our dimensions will be: 10,000/2 slices x 2 time points x 20 attributes = 5000 x 2 x 20
    You must have at least 2 time points per slice, otherwise the tool will not work.

LABELS
    You should have one label per slice. For instance, in the above example we would have 5000 labels for 5000 slices.
    Labels should be binary, -1 or +1.
    Labels should be listed in a text file like: -1, -1, +1, +1, +1, -1 etc.

TIME
    Time should be for the time points per slice. For example, using previous example our time points would be: 1, 2
    Time should be listed in a text file like: 1, 2, 3, 4 etc.


FormatDataHelper - Helps you preprocess your data to be in the correct format for the tool.
Assumes input CSV data file is like follows:

Time | var1 | var2 | var 3 | ... | var n | Labels (+1 or -1)
t1                                                  +1
t2                                                  -1
t3                                                  -1
t4                                                  +1
...    ...                                          ...
tn


Required Libraries:
These can be easily installed into a Python environment such as by using PyCharm.
    GPy	1.9.9
    GPyOpt	1.2.5
    antlr4-python3-runtime	4.7.2
    bayesian-optimization	1.0.1
    matplotlib	3.1.2	3.1.2
    numpy	1.17.2
    pandas	0.25.2
    pytz	2019.3
    regex	2020.1.8
    scikit-learn	0.22
    scikit-optimize	0.5.2
    scipy	1.3.3
    treelib	1.5.5

Running Code:
To run follow the code provided in Main.py:
    1. Define variables:
        variables = ["x", "y", "v", "z"]
    2. Define lower bounds for each variable
        lower = [0, 0, 0, 0] #lowerbound
    3. Define upper bounds for each variable
        upper = [80, 45, 80, 45] # upperbound
    4. Create learning object with paths to data files
        l = Learning(logging.INFO, "Data/values", "Data/labels", "Data/times", variables, lower, upper)
    5. Start learning
        l.run()


Breakdown of Code Folders:

Data
    - Simulation data to play with

FormulaSpec
    - Formula Population stores sets of STL formulas
    - Formula Population uses Formula Generator to generate the actual formula sets stored in the formula pop class.
    - In Formula Generator, STL Factory is used to create the formula and return an STL tree that represents the formula.

Genetic Spec
    - Genetic Population stores genetically modified and generated sets of STL formulas
    - Genetic Population uses Genetic Generator to generate the actual genetic populations stored in the genetic population class.
    - Genetic Options stores defining hyperparameters for the genetic algorithm

Signal Temporal Logic
    - Contains files to parse a string formula and return a tree object that represents the STL formula
    - STL Factory creates an STL tree from the abstract syntax tree that is produced using the defined STL Grammar, STL parser and STL visitor.

STL Tree
    - STL Tree is a formula tree for STL formulas. It uses treelib to store and create tree objects
    - STL Expr, Operator and Atomic are all classes that hold node types that make up the STL tree
    - In STL Tree part, evaluateRobustness calculates robustness, evaluateValue returns boolean truth value


Workflow Notes
    To generate a formula:
        Write formula in plain text --> send to STL factory --> STL factory builds parser and visitor --> visitor reads string and returns an abstract syntax tree -->
        AST is converted to an STL  tree that  stores each part of the formula as an object type --> formula  tree is returned.





