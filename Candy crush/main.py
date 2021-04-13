"""
Observatie pentru cei absenti la laborator: trebuie sa dati enter după fiecare afișare a cozii până vă apare o soluție. Afișarea era ca să vedem progresul algoritmului. Puteți să o dezactivați comentând print-ul cu coada și input()
"""
import copy

info =  ['#', 'a', 'b', 'c'], \
        ['#', 'c', '#', 'c'], \
        ['b', 'b', 'd', '#']

for x in range(len(info) - 1, -1, -1):
    for y in range(len(info[x]) - 1, -1, -1):
        x_copy = copy.deepcopy(x)
        y_copy = copy.deepcopy(y)
        z = x_copy + 1
        print(x, y, z)
        while z <= len(info) - 1 and info[x_copy][y_copy] != '#' and info[z][y_copy] == '#':
            info[z][y_copy] = info[x_copy][y_copy]
            info[x_copy][y_copy] = '#'
            x_copy += 1
            z += 1