# Compiler Design Coursework

## parser.py

### Requirements
It uses the `re` and `datetime` package so you will need to make sure you have that installed to be
able to run it.
 
To generate the parse tree the package `anytree` is used. Install it with `pip install anytree`. 
However a prerequisite to `anytree` is GraphViz. On Windows, either find the download page and
install using the `.msi` installer or unzip and add the `bin` location to the PATH variables. 
[Here](https://graphviz.gitlab.io/_pages/Download/Download_windows.html "Windows GraphViz Download") 
is a link to the Windows download page. (I had problems with the installer not adding the files to
PATH variables, so once it is installed check if the `\bin\ ` folder is in the PATH environment
variables, and if it isn't, add it. I had to add `C:\Program Files (x86)\Graphviz2.38\bin\ `). 
 
### Setup
The python file should be stored in the root directory of where you want this to run. The folder 
structure should then be as follows:
```
Compiler Desgin/
├── Inputs/
│   ├── example.txt
│   └── example1.txt
├── log/
├── └── log.log
├── Outputs/
├── ├── example.png
├── ├── example1.png
├── ├── example-grammar.txt
├── └── example1-grammar.txt
└── parser.py
```
 
### How to use
`parser.py` is the main python file to use to run this project. It will read in the supplied file
name as a given argument e.g. `$~ python parser.py example.txt`. It will correctly read in the file 
and store the variables, constants, predicates, equality, connectives, quantifiers and formula to
the associated variables. If no text file is supplied it will default to the example text file 
included in the repository.

The input file, to be formatted correctly, must have on each line what it is defining, followed by 
a colon and a space and then space delimited items. The formula can span multiple lines and be white
space delimited also. Look at `example.txt` and `example1.txt` for further detail.

### Outputs
This script will, upon a successful run, print the terminal symbols separated by `|` followed by
the non-terminal symbols separated by `|`. It will then print the start symbol and finally the
grammar production rules. It also saves these grammar production rules, terminal and non-terminal
symbols to a file of the input name + `-grammer.txt` so e.g. for `example.txt` it would output to
`example-grammar.txt`. 

If it encounters any errors then it will print to `stderr` with the appropriate message and exit
with a non-zero exit code. It will also log this error to the log file.

It will also save the parse tree of the formula, if it is valid, to the `Outputs/` folder under
the name of the file + `.png` e.g. for `example.txt` it would output `example.png`.

Log file output including successful parsing of formula, successful node added to the graph and
any error that may occur. It is in the format 
```
HH:MM:SS    OK/warning/error    description
```