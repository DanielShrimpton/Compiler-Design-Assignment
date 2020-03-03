# Compiler Design Coursework

## parser.py

### Requirements
 It uses the `re` package so you will need to make sure you have that installed to be able to run 
 it.
 
 ### Setup
 The python file should be stored in the root directory of where you want this to run. The folder 
 structure should then be as follows:
```
Compiler Desgin/
├── parser.py
├── Inputs/
│   ├── example.txt
│   ├── example1.txt
└── Outputs/
```
 
 ### How to use
This file is the main python file to use to run this project. It will read in the supplied file name 
as a given argument e.g. `$~ python parser.py example.txt`. It will correctly read in the file 
and store the variables, constants, predicates, equality, connectives, quantifiers and formula to
the associated variables, where all but the equality are lists.