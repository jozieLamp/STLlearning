
STL Tree is a formula tree for STL formulas.
STL Factory creates an STL tree from the abstract syntax tree that is produced using the defined STL Grammar, STL parser and STL visitor.
To generate a formula:
Write formula in plain text --> send to STL factory --> STL factory builds parser and visitor --> visitor reads string and returns an abstract syntax
tree --> AST is converted to an STL  tree that  stores each part of the formula as an object type --> formula  tree is returned.


Formula Population uses Formula Generator to generate the actual formula sets stored in the formula pop class.
In Formula Generator,  STL Factory is used to create the formula and return an STL tree that represents the formula.

Genetic Population uses Genetic Generator to generate the actual genetic populations stored in the genetic population class.

