"""File for compiler design to parse FO logic"""
import math
import re
import sys
from anytree import Node, RenderTree
from anytree.exporter import UniqueDotExporter

INPUT_FOLDER = './Inputs/'
OUTPUT_FOLDER = './Outputs/'
tree = {'<S>': Node('<S>')}
START = tree['<S>']


class Grammar:
    """A class to read in a formula and variables etc from a file and create a grammar and check
    it is valid."""

    def __init__(self):
        """The init function, setting up variables and then read in from file"""
        # Initialise the variables we will need
        self.variables = []
        self.constants = []
        self.arity = {}  # A dictionary in the form { pred: arity, ... } e.g. { 'P': 2, 'Q': 1 }
        self.predicates = []  # A list of arity.keys()
        self.equality = ''
        self.connectives = []
        self.neg = ''  # The last character of the connectives popped
        self.quantifiers = []
        self.formula = []
        self.terminals = []
        self.grammar = {}
        # Read in the file to populate the variables
        self.read_file()
        # Initialising variables to help make the tree
        self.current = None
        self.parent = START
        self.root = START
        self.ID = 0
        self.add_node('<formula>')
        self.parent = tree['0']
        self.open = 0  # Variable to keep track of number of open brackets
        self.old = 0

    def read_file(self):
        """Function to read in from file supplied from the command line and then update
        corresponding variables"""
        try:
            file = INPUT_FOLDER + sys.argv[1]
        except IndexError:
            print("Error! No file, using default example.txt")
            file = INPUT_FOLDER + 'example.txt'
        try:
            with open(file, 'r') as file:
                for line in file.readlines():
                    if 'variables: ' in line:
                        self.variables = re.findall(r'[ ](\S*)', line)
                    elif 'constants: ' in line:
                        self.constants = re.findall(r'[ ](\S*)', line)
                    elif 'predicates: ' in line:
                        predicates = re.findall(r'[ ](\S*)', line)
                        for pred in predicates:
                            size = re.search(r'\[\d+\]', pred)
                            length = len(size.group())
                            # Check here for in pred[:-length] for invalid characters
                            predicate = re.search(r'(\w+)\[', pred).group(1)
                            self.arity[predicate] = re.search(r'\d+', pred).group()
                    elif 'equality: ' in line:
                        self.equality = re.search(r'[ ](\S*)', line).group(1)
                    elif 'connectives: ' in line:
                        self.connectives = re.findall(r'[ ](\S*)', line)
                    elif 'quantifiers: ' in line:
                        self.quantifiers = re.findall(r'[ ](\S*)', line)
                    elif 'formula: ' in line:
                        self.formula = re.findall(r'\s(\S+)', line)
                    else:
                        for x in line.split(' '):
                            if x != '':
                                self.formula.append(x)
        except FileNotFoundError:
            print("Error, no such file exists: %s" % file)
            sys.exit(-1)

        self.predicates = list(self.arity.keys())
        if len(self.connectives) != 5:
            print("Incorrect number of connectives supplied!")
            sys.exit(2)
        self.neg = self.connectives.pop(-1)

        print(self.formula)
        self.gen_grammar()
        for atom in self.formula:
            if (len(atom) > 1) and (any(terminal in atom for terminal in self.terminals)):
                if atom not in self.terminals:
                    temp = re.split(r'([(),])', atom)
                    ind = self.formula.index(atom)
                    temp = [x for x in temp if x != '']
                    num = len(temp) - 1
                    self.formula.pop(ind)
                    while num >= 0:
                        self.formula.insert(ind, temp[num])
                        num -= 1

        print(self.formula)

    def gen_grammar(self):
        """Generate the grammar, the production rules and terminal and non-terminal symbols"""
        self.terminals = self.quantifiers + self.predicates + self.connectives + [self.equality] \
                         + self.constants + self.variables + [',', '(', ')']

        print('\nTerminal symbols: ' + '|'.join(self.terminals))
        print("\nGrammar Production Rules: \n")

        quants = self.quantifiers[:]  # Make a copy of the list so as not to change the original
        #                               list

        for elem in range(len(quants)):
            quants[elem] += ' <var>'

        preds = []
        for pred in self.arity.keys():
            preds.append(pred + '(')
            for i in range(int(self.arity[pred]) - 1):
                preds[-1] += '<var>, '
            preds[-1] += '<var>)'

        self.grammar = {'<S>': ['<formula>'],
                        '<formula>': ['<quant> <formula>', '(<formula> <conn> <formula>)',
                                      '<assign>', '<pred>', self.neg + ' <formula>'],
                        '<quant>': quants,
                        '<var>': self.variables,
                        '<constVar>': self.constants + ['<var>'],
                        '<assign>': ['(<constVar> ' + self.equality + ' <constVar>)'],
                        '<pred>': preds,
                        '<conn>': self.connectives
                        }

        for key in self.grammar.keys():
            t = math.ceil((12 - len(key)) / 4)
            if key == '<S>':
                t = 2
            print(key + '\t' * t + '->\t' + '|'.join(self.grammar[key]))

    def add_node(self, tag, parent=0):
        if parent != 0:
            parent = tree[str(self.ID - parent)]
        else:
            parent = self.parent

        tree[str(self.ID)] = Node(tag, parent=parent)
        self.ID += 1

    def parse(self):
        self.current = 0
        while self.current < len(self.formula):
            self.old = self.current
            atom = self.formula[self.current]
            if atom in self.quantifiers:
                pass
            elif atom in self.variables:
                pass
            elif atom == '(':
                self.open += 1
            elif atom in self.predicates:
                pass
            elif atom == ',':
                pass
            elif atom in self.connectives:
                pass
            elif atom == self.neg:
                pass
            elif atom == ")":
                self.open -= 1
                self.parent = self.parent.parent
                print(self.parent)
                if self.open < 0:
                    print("ERROR: Invalid bracketing")
                    sys.exit(1)
            elif atom == self.equality:
                pass
            elif atom in self.constants:
                pass
            else:
                print("ERROR, incorrect syntax, unknown character: " + atom)
                sys.exit(3)

            self._formula()
            if self.old == self.current:
                self.current += 1

    def _formula(self):
        atom = self.formula[self.current]
        if atom in self.quantifiers:
            """It should be a quantifier statement followed by a formula e.g. ∀ x <formula>"""
            self.add_node('<quant>')
            self.add_node(atom, 1)
            self.add_node('<formula>')
            self.next_par = tree[str(self.ID - 1)]
            self.parent = tree[str(self.ID - 3)]
            self.current += 1
            self._quant()
            self.parent = self.next_par

        elif atom in self.predicates:
            """It should be a predicate statement e.g. P(x, y)"""
            self.add_node('<pred>')
            self.add_node(atom, 1)
            self.next_par = self.parent
            self.parent = tree[str(self.ID - 2)]
            self.current += 1
            self._pred()
            self.parent = self.next_par

        elif atom == '(':
            if self.formula[self.current + 2] == self.equality:
                """It should be an assignment statement e.g. (x = y)"""
                self.add_node('<equality>')
                self.next_par = self.parent
                self.parent = tree[str(self.ID - 1)]
                self._assign()
                self.parent = self.next_par

        elif atom == self.neg:
            self.add_node('<neg>')
            self.add_node('<formula>')
            self.add_node(atom, parent=2)
            self.parent = tree[str(self.ID - 2)]
            self.current += 1

    def _quant(self):
        atom = self.formula[self.current]
        if atom in self.variables:
            self.add_node('<var>')
            self.add_node(atom, 1)
        else:
            print("Bad quantifier, not using variables: %s %s" % (self.formula[self.current - 1],
                  atom))
            sys.exit(1)
        self.current += 1


    def _var(self):
        return None

    def _const_var(self):
        return None

    def _assign(self):
        self.add_node('(')
        self.current += 1
        atom = self.formula[self.current]
        if (atom in self.constants) or (atom in self.variables):
            self.add_node('<constVar>')
        else:
            print("Error, assignment using unknown constant/var: %s" % atom)
            sys.exit(1)
        self.add_node(self.equality)
        self.current += 2
        atom = self.formula[self.current]
        if (atom in self.constants) or (atom in self.variables):
            self.add_node('<constVar>')
            self.add_node(atom, parent=1)
        else:
            print("Error, assignment using unknown constant/var: %s" % atom)
            sys.exit(1)
        self.current += 1
        atom = self.formula[self.current]
        if atom == ')':
            self.add_node(')')
        else:
            print("Error, assignment missing closing bracket: %s" %
                  " ".join(self.formula[self.current-4:self.current]))
            sys.exit(1)
        self.current += 1

    def _pred(self):
        atom = self.formula[self.current]
        pred = self.formula[self.current - 1]
        if atom == '(':
            self.add_node('(')
        else:
            print("Error, syntax error! Predicate %s isn't followed by '('." % pred)
            sys.exit(1)
        arity = int(self.arity[pred]) - 1
        self.current += 1
        atom = self.formula[self.current]
        while arity > 0:
            if (atom in self.variables) and (self.formula[self.current + 1] == ','):
                self.add_node('<var>')
                self.add_node(',')
                self.add_node(atom, 2)
                self.current += 2
                atom = self.formula[self.current]
            else:
                print("Error, syntax error! Predicate %s isn't formatted correctly" % pred)
                sys.exit(1)
            arity -= 1
        if atom in self.variables:
            self.add_node('<var>')
            self.add_node(atom, 1)
        else:
            print("Error, syntax error! Predicate %s isn't formatted correctly" % pred)
            sys.exit(1)
        self.current += 1
        atom = self.formula[self.current]
        if atom == ')':
            self.add_node(')')
        else:
            print("Error, syntax error! Predicate %s isn't formatted correctly: missing ')'" % pred)
            sys.exit(1)
        self.current += 1

    def _conn(self):
        return None

    def match(self):
        return None

    def save_tree(self):
        UniqueDotExporter(self.root).to_picture('tree.png')

    def print_tree(self):
        for pre, fill, node in RenderTree(self.root):
            print("%s%s" % (pre, node.name))


thing = Grammar()
thing.parse()
thing.print_tree()
thing.save_tree()
