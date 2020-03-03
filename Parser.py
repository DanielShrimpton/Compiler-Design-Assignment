import re

variables = []
constants = []
predicates = []
equality = ''
connectives = []
quantifiers = []
formula = []
with open('example.txt', 'r') as f:
    for line in f.readlines():
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


