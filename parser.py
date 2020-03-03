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
    equality = ''
    connectives = []
    quantifiers = []
    formula = []
    with open(file, 'r') as file:
        for line in file.readlines():
            if 'variables: ' in line:
                variables = re.findall(r'[ ](\S)', line)
            elif 'constants: ' in line:
                constants = re.findall(r'[ ](\S)', line)
            elif 'predicates: ' in line:
                predicates = re.findall(r'[ ](\S*)', line)
            elif 'equality: ' in line:
                equality = re.search(r'[ ](\S*)', line).group(1)
            elif 'connectives: ' in line:
                connectives = re.findall(r'[ ](\S*)', line)
            elif 'quantifiers: ' in line:
                quantifiers = re.findall(r'[ ](\S*)', line)
            elif 'formula: ' in line:
                formula = re.findall(r'[ ](\S{1,100})', line)
            else:
                for x in line.split(' '):
                    if x != '':
                        formula.append(x)

    print('variables: ' + ' '.join(variables))
    print('constants: ' + ' '.join(constants))
    print('predicates: ' + ' '.join(predicates))
    print('equality: ' + equality)
    print('connectives: ' + ' '.join(connectives))
    print('quantifiers: ' + ' '.join(quantifiers))
    print('formula: ' + ' '.join(formula))


if __name__ == '__main__':
    main()
