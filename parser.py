"""File for compiler design to parse FO logic"""
import math
import re
import sys
from anytree import Node
from anytree.exporter import UniqueDotExporter
from datetime import datetime

INPUT_FOLDER = './Inputs/'
OUTPUT_FOLDER = './Outputs/'
LOG = './log/log.log'
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
        self.non_terminals = []
        self.grammar = {}
        self.names = []
        # Read in the file to populate the variables
        self.file_name = ''
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
            self.file_name = sys.argv[1].strip('.txt')
        except IndexError:
            log('warning', "Warning: no file supplied, using default 'example.txt'")
            file = INPUT_FOLDER + 'example.txt'
            self.file_name = 'example'
        try:
            with open(file, 'r') as file:
                for line in file.readlines():
                    if 'variables:' in line:
                        self.variables = [re.escape(x) if '\\' in x else x for x in
                                          re.findall(r'[ ](\S+)', line)]
                        self.names += self.variables
                    elif 'constants:' in line:
                        self.constants = [re.escape(x) if '\\' in x else x for x in
                                          re.findall(r'[ ](\S+)', line)]
                        self.names += self.constants
                    elif 'predicates:' in line:
                        predicates = [re.escape(x) if '\\' in x else x for x in
                                      re.findall(r'[ ](\S+)\[(\d+)\]', line)]
                        for pred, size in predicates:
                            if '(' in pred:
                                st = "NameError: illegal character found in predicate %s, " \
                                     "the character '(' is not allowed" % pred
                                log("error", st)
                                sys.exit(1)
                            elif ')' in pred:
                                st = "NameError: illegal character found in predicate %s, " \
                                     "the character ')' is not allowed" % pred
                                log("error", st)
                                sys.exit(1)
                            elif ':' in pred:
                                st = "NameError: illegal character found in predicate %s, " \
                                     "the character ':' is not allowed" % pred
                                log("error", st)
                                sys.exit(1)
                            self.arity[pred] = size
                    elif 'equality:' in line:
                        self.equality = re.findall(r'[ ](\S+)', line)
                        if len(self.equality) != 1:
                            st = "InputError: incorrect number of equalities supplied, " \
                                 "there needs to be 1"
                            log("error", st)
                            sys.exit(2)
                        else:
                            self.equality = self.equality[0]
                        if '\\' in self.equality:
                            self.equality = re.escape(self.equality)
                        self.names.append(self.equality)
                    elif 'connectives:' in line:
                        self.connectives = [re.escape(x) if '\\' in x else x for x in
                                            re.findall(r'[ ](\S+)', line)]
                        if len(self.connectives) != 5:
                            st = "InputError: incorrect number of connectives supplied, " \
                                 "there needs to be 5"
                            log('error', st)
                            sys.exit(1)
                        self.names += self.connectives
                    elif 'quantifiers:' in line:
                        self.quantifiers = [re.escape(x) if '\\' in x else x for x in
                                            re.findall(r'[ ](\S+)', line)]
                        if len(self.quantifiers) != 2:
                            st = "InputError: incorrect number of quantifiers supplied, " \
                                 "there needs to be 2"
                            log("error", st)
                            sys.exit(1)
                        self.names += self.quantifiers
                    elif 'formula:' in line:
                        self.formula = [re.escape(x) if '\\' in x else x for x in
                                        re.findall(r'\s(\S+)', line)]
                    else:
                        for x in line.split(' '):
                            if x != '':
                                if '\\' in x:
                                    self.formula.append(re.escape(x))
                                else:
                                    self.formula.append(x)
        except FileNotFoundError:
            log("error", "FileNotFoundError: cannot find file: %s" % file)
            sys.exit(-1)

        self.predicates = list(self.arity.keys())
        self.names += self.predicates
        names_set = set(self.names)
        if len(names_set) != len(self.names):
            log("error", "InputError: no duplicate names allowed")
            sys.exit(1)

        for name in self.names:
            if re.search(r'^<', name):
                log("error", "NameError: items cannot begin with '<'")
                sys.exit(1)
            elif re.search(r'\(', name):
                log("error", "NameError: items cannot contain the character '('")
                sys.exit(1)
            elif re.search(r':', name):
                log("error", "NameError: items cannot contain the character ':'")
                sys.exit(1)
            elif re.search(r'\)', name):
                log("error", "NameError: items cannot contain the character ')'")
                sys.exit(1)
            # elif re.search(r'=', name):
            #     if name != self.equality:
            #         log("error", "NameError: items cannot contain the character '=' unless it is "
            #                      "equality")
            #         sys.exit(1)
            elif re.search(r'/', name):
                if name in self.connectives:
                    log("error", "NameError: connectives cannot contain character '/'")
                    sys.exit(1)
                elif name in self.quantifiers:
                    log("error", "NameError: quantifiers cannot contain character '/'")
                    sys.exit(1)
                else:
                    log("error", "NameError: illegal character '/' detected in %s" % name)
                    sys.exit(1)
            elif not re.match(r'^[\w\\_]+$', name):
                if not ((name == self.equality) and re.match(r'^[\w\\_=]+$', name)):
                    log("error", "NameError: illegal character detected in %s" % name)
                    sys.exit(1)

        self.neg = self.connectives.pop(-1)

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

    def gen_grammar(self):
        """Generate the grammar, the production rules and terminal and non-terminal symbols"""
        self.terminals = self.quantifiers + self.predicates + self.connectives + [self.neg]
        self.terminals += [self.equality] + self.constants + self.variables + [',', '(', ')']

        self.non_terminals = ['<S>', '<formula>', '<quant>', '<conn>', '<assign>', '<pred>',
                              '<var>', '<constVar>']

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

    def print_grammar(self):
        self.terminals = [x.replace('\\\\', '\\') if '\\\\' in x else x for x in self.terminals]
        print('\nTerminal symbols: ' + '|'.join(self.terminals))
        print('\nNon-Terminal symbols: ' + '|'.join(self.non_terminals))
        print('\nStart symbol: <S>')
        print("\nGrammar Production Rules: \n")

        for key in self.grammar.keys():
            t = math.ceil((12 - len(key)) / 4)
            if key == '<S>':
                t = 2
            print(key + '\t' * t + '->\t' + '|'.join(self.grammar[key]).replace('\\\\', '\\'))
        log("OK", "Successfully parsed formula")

    def add_node(self, tag, parent=0):
        if parent != 0:
            parent = tree[str(self.ID - parent)]
        else:
            parent = self.parent

        tree[str(self.ID)] = Node(tag, parent=parent)
        self.ID += 1
        log("info", "Added node %s" % tag)

    def parse(self):
        self.current = 0
        self._formula()
        if self.current == len(self.formula):
            self.print_grammar()
        else:
            log("error", "SyntaxError: Unexpected part of formula: %s" % ' '.join(self.formula[
                                                                                  self.current:]))
            sys.exit(1)

    def _formula(self):
        atom = self.formula[self.current]
        if atom in self.quantifiers:
            """It should be a quantifier statement followed by a formula e.g. ∀ x <formula>"""
            self.add_node('<quant>')
            self.add_node(atom, 1)
            self.add_node('<formula>')
            next_par = tree[str(self.ID - 1)]
            self.parent = tree[str(self.ID - 3)]
            self.current += 1
            self._quant()
            self.parent = next_par
            self._formula()

        elif atom in self.predicates:
            """It should be a predicate statement e.g. P(x, y)"""
            self.add_node('<pred>')
            self.add_node(atom, 1)
            next_par = self.parent
            self.parent = tree[str(self.ID - 2)]
            self.current += 1
            self._pred()
            self.parent = next_par

        elif atom == '(':
            if self.formula[self.current + 2] == self.equality:
                """It should be an assignment statement e.g. (x = y)"""
                self.add_node('<equality>')
                next_par = self.parent
                self.parent = tree[str(self.ID - 1)]
                self._assign()
                self.parent = next_par
            else:
                self.open += 1
                conn = self.find_conn()
                self.add_node('(')
                self.add_node('<formula>')
                self.current += 1
                next_par = self.parent
                self.parent = tree[str(self.ID - 1)]
                self._formula()
                self.parent = next_par
                self.add_node('<conn>')
                self.add_node(conn, parent=1)
                self.add_node('<formula>')
                self.current += 1
                self.add_node(')')
                self.parent = tree[str(self.ID - 2)]
                self._formula()
                self.current += 1

        elif atom == self.neg:
            self.add_node('<neg>')
            self.add_node('<formula>')
            self.add_node(atom, parent=2)
            self.parent = tree[str(self.ID - 2)]
            self.current += 1
            self._formula()

        elif atom == ')':
            self.add_node(')')
            self.open -= 1
            self.current += 1
            self.parent = self.parent.parent

        elif atom in self.connectives:
            self.current += 1

        else:
            log("error", "SyntaxError: Unexpected character '%s'" % atom)
            sys.exit(1)

    def _quant(self):
        atom = self.formula[self.current]
        if atom in self.variables:
            self.add_node('<var>')
            self.add_node(atom, 1)
        else:
            log("error", "SyntaxError: quantifier not followed by known variable: %s %s" % (
                self.formula[self.current - 1], atom))
            sys.exit(1)
        self.current += 1

    def _const_var(self, atom):
        if (atom in self.constants) or (atom in self.variables):
            self.add_node('<constVar>')
            self.add_node(atom, parent=1)
        else:
            log("error", "SyntaxError: assignment using unknown constant/variable: %s" % atom)
            sys.exit(1)
        self.current += 1

    def _assign(self):
        self.add_node('(')
        self.current += 1
        atom = self.formula[self.current]
        self._const_var(atom)
        self.add_node(self.equality)
        self.current += 1
        atom = self.formula[self.current]
        self._const_var(atom)
        atom = self.formula[self.current]
        if atom == ')':
            self.add_node(')')
        else:
            log("error", "SyntaxError, assignment missing closing bracket: %s" % " ".join(
                self.formula[self.current - 4:self.current]))
            sys.exit(1)
        self.current += 1

    def _pred(self):
        atom = self.formula[self.current]
        pred = self.formula[self.current - 1]
        if atom == '(':
            self.add_node('(')
        else:
            log("error", "SyntaxError: predicate %s isn't followed by '('." % pred)
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
                log("error", "Error, syntax error! Predicate %s isn't formatted correctly" % pred)
                sys.exit(1)
            arity -= 1
        if atom in self.variables:
            self.add_node('<var>')
            self.add_node(atom, 1)
        else:
            log("error", "Error, syntax error! Predicate %s isn't formatted correctly" % pred)
            sys.exit(1)
        self.current += 1
        atom = self.formula[self.current]
        if atom == ')':
            self.add_node(')')
        else:
            log("error", "Error, syntax error! Predicate %s isn't formatted correctly: missing "
                         "')'" % pred)
            sys.exit(1)
        self.current += 1

    def find_conn(self):
        num = self.current
        open_ = self.open
        for i in range(num + 1, len(self.formula)):
            atom = self.formula[i]
            if atom == '(':
                open_ += 1
            elif atom == ')':
                open_ -= 1
            elif atom in self.connectives:
                if open_ == self.open:
                    return atom
        log("error", "Error, invalid syntax, redundant brackets")
        sys.exit(1)

    def save_tree(self):
        UniqueDotExporter(self.root).to_picture('Outputs/' + self.file_name + '.png')

    def write_grammar(self):
        with open('Outputs/' + self.file_name + '-grammar.txt.', 'w') as file:
            file.write('Terminal symbols: %s\n' % '|'.join(self.terminals))
            file.write('\nNon-Terminal symbols: %s\n' % '|'.join(self.non_terminals))
            file.write('\nStart symbol: <S>\n')
            file.write("\nGrammar Production Rules: \n\n")

            for key in self.grammar.keys():
                t = math.ceil((12 - len(key)) / 4)
                if key == '<S>':
                    t = 2
                file.write(key + '\t' * t + '->\t' + '|'.join(self.grammar[key])
                           .replace('\\\\', '\\') + '\n')


def log(type_, string):
    if type_ == 'warning':
        print(string)
    elif type_ == 'OK':
        pass
    elif type_ == 'info':
        pass
    else:
        sys.stderr.write(string + '\n')
    now = datetime.now().strftime("%H:%M:%S")
    with open(LOG, 'a') as file:
        file.write(now + '\t' + type_ + '\t' + string + '\n')


thing = Grammar()
thing.parse()
thing.save_tree()
thing.write_grammar()
