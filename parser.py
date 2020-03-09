"""File for compiler design to parse FO logic"""
import math
import re
import sys
from anytree import Node, RenderTree
from anytree.exporter import DotExporter


INPUT_FOLDER = './Inputs/'
OUTPUT_FOLDER = './Outputs/'


class Grammar:
    def __init__(self):
        # Initialise the variables we will need
        self.variables = []
        self.constants = []
        self.arity = {}
        self.predicates = []
        self.equality = ''
        self.connectives = []
        self.neg = ''
        self.quantifiers = []
        self.formula = []
        self.terminals = []
        self.grammar = {}
        # Read in the file to populate the variables
        self.read_file()

    def read_file(self):
        try:
            file = INPUT_FOLDER + sys.argv[1]
        except IndexError:
            print("Error! No file, using default example.txt")
            file = INPUT_FOLDER + 'example.txt'
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

        self.predicates = list(self.arity.keys())
        if len(self.connectives) != 5:
            print("Incorrect number of connectives supplied!")
            sys.exit(2)
        self.neg = self.connectives.pop(-1)

    def gen_grammar(self):
        self.terminals = self.quantifiers + self.predicates + self.connectives + [self.equality] \
                         + self.constants + self.variables + [',', '(', ')']

        print('\nTerminal symbols: ' + '|'.join(self.terminals))
        print("\nGrammar Production Rules: \n")

        quants = self.quantifiers[:]  # Make a copy of the list so as not to change the original
                                      # list

        for elem in range(len(quants)):
            quants[elem] += ' <var>'

        preds = []
        for pred in self.arity.keys():
            preds.append(pred + '(')
            for i in range(int(self.arity[pred]) - 1):
                preds[-1] += '<var>, '
            preds[-1] += '<var>)'

        self.grammar = {'<S>': ['<formula>', '(<formula> <conn> <formula>)'],
                        '<formula>': ['<quant> <formula>', '(<formula> <conn> <formula>',
                                      '<assign>', '<constVar>', '<pred>', self.neg + ' <formula>'],
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

    def _formula(self):
        return None

    def _quant(self):
        return None

    def _var(self):
        return None

    def _constVar(self):
        return None

    def _assign(self):
        return None

    def _pred(self):
        return None

    def _conn(self):
        return None

    def match(self):
        return None


thing = Grammar()
thing.gen_grammar()
