"""File for compiler design to parse FO logic"""
import re
import sys
from anytree import Node, RenderTree
from anytree.exporter import DotExporter


INPUT_FOLDER = './Inputs/'
OUTPUT_FOLDER = './Outputs/'


def main():
    """Main function"""
    try:
        file = INPUT_FOLDER + sys.argv[1]
    except IndexError:
        print("error, no file, using default example")
        file = INPUT_FOLDER + 'example.txt'
    variables = []
    constants = []
    arity = {}
    equality = ''
    connectives = []
    quantifiers = []
    formula = []
    with open(file, 'r') as file:
        for line in file.readlines():
            if 'variables: ' in line:
                variables = re.findall(r'[ ](\S*)', line)
            elif 'constants: ' in line:
                constants = re.findall(r'[ ](\S*)', line)
            elif 'predicates: ' in line:
                predicates = re.findall(r'[ ](\S*)', line)
                for pred in predicates:
                    arity[re.search(r'(\w)\[', pred).group(1)] = re.search(r'\d+', pred).group()
            elif 'equality: ' in line:
                equality = re.search(r'[ ](\S*)', line).group(1)
            elif 'connectives: ' in line:
                connectives = re.findall(r'[ ](\S*)', line)
            elif 'quantifiers: ' in line:
                quantifiers = re.findall(r'[ ](\S*)', line)
            elif 'formula: ' in line:
                formula = re.findall(r'\s(\S{1,100})', line)
            else:
                for x in line.split(' '):
                    if x != '':
                        formula.append(x)

    predicates = arity.keys()

    print(formula)

    prod_rules = rules(variables, constants, arity, equality, connectives, quantifiers)


def rules(v, consts, arity, eq, conns, quants):
    """function to create rules"""

    for elem in range(len(quants)):
        quants[elem] += ' <var>'

    preds = []
    for pred in arity.keys():
        preds.append(pred + '(')
        for i in range(int(arity[pred]) - 1):
            preds[-1] += '<var>, '
        preds[-1] += '<var>)'

    neg = conns[-1]

    prod_rules_ = {'<S>': ['<formula>', '(<formula> <conn> <formula>)'],
                   '<formula>': ['<quant> <formula>', '(<formula> <conn> <formula>', '<assign>',
                                 '<constVar>', '<pred>', neg + ' <formula>'],
                   '<quant>': quants,
                   '<var>': v,
                   '<constVar>': consts + ['<var>'],
                   '<assign>': ['(<constVar> ' + eq + ' <constVar>)'],
                   '<pred>': preds,
                   '<conn>': conns[:-1]
                   }

    for key in prod_rules_.keys():
        print(key + '\t-> ' + '|'.join(prod_rules_[key]))

    return prod_rules_


if __name__ == '__main__':
    main()
