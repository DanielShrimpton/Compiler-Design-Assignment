"""File for compiler design to parse FO logic"""
import re
import sys

INPUT_FOLDER = './Inputs/'
OUTPUT_FOLDER = './Outputs/'


def main():
    """Main function"""
    file = INPUT_FOLDER + sys.argv[1]
    variables = []
    constants = []
    predicates = []
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

    # print('variables: ' + ' '.join(variables))
    # print('constants: ' + ' '.join(constants))
    # print('predicates: ' + ' '.join(predicates))
    # print('equality: ' + equality)
    # print('connectives: ' + ' '.join(connectives))
    # print('quantifiers: ' + ' '.join(quantifiers))
    # print('formula: ' + ' '.join(formula))

    # print(variables)
    # print(constants)
    # print(predicates)
    # print(equality)
    # print(connectives)
    # print(quantifiers)
    # print(formula)

    rules(variables, constants, arity, equality, connectives, quantifiers)


def rules(v, consts, arity, eq, conns, quants):
    """function to create rules"""

    for elem in range(len(quants)):
        quants[elem] += ' Var Th'

    for elem in range(len(conns)):
        conns[elem] += ' Th'

    const = '(Const' + eq + 'Var) Th'
    formula = '(replace) Th'

    preds = []
    for pred in arity.keys():
        preds.append(pred + '(')
        for i in range(int(arity[pred]) - 1):
            preds[-1] += 'Var, '
        preds[-1] += 'Var) Th'

    thing = ['', quants, conns, 'Var Th', formula]

    prod_rules = ['S\t-> Quants|Preds|' + const.replace('Var', '\\v') + '|Formula',
                  'Formula\t-> (Quants|Preds|' + const.replace('Var', '\\v') + '|Formula) Th',
                  'Th\t-> \\epsilon|Quants|Preds|\\v Th|Preds|Formula',
                  '\\v\t-> ' + '|'.join(v),
                  'Const\t-> ' + '|'.join(consts),
                  'Quants\t-> ' + '|'.join(quants).replace('Var', '\\v'),
                  'Preds\t-> ' + '|'.join(preds).replace('Var', '\\v'),
                  'Conns\t-> ' + '|'.join(conns)
                  ]

    for line in prod_rules:
        print(line)


if __name__ == '__main__':
    main()
