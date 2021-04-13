import copy

def mapeaza_caractere(infoNod):
    ch_number = {}
    for linie in infoNod:
        for ch in linie:
            if ch in ch_number.keys():
                ch_number[ch] += 1
            else:
                ch_number[ch] = 1
    return ch_number


def identifica_bloc(infoNod, x, y, viz, elemente_in_bloc):
    viz[x][y] = 1
    elemente_in_bloc.append((x, y))
    if x > 0 and infoNod[x][y] == infoNod[x - 1][y] and viz[x - 1][y] == 0 and infoNod[x][y] != '#':
        identifica_bloc(infoNod, x - 1, y, viz, elemente_in_bloc)
    if y > 0 and infoNod[x][y] == infoNod[x][y - 1] and viz[x][y - 1] == 0 and infoNod[x][y] != '#':
        identifica_bloc(infoNod, x, y - 1, viz, elemente_in_bloc)
    if x < len(infoNod) - 1 and infoNod[x][y] == infoNod[x + 1][y] and viz[x + 1][y] == 0 and infoNod[x][y] != '#':
        identifica_bloc(infoNod, x + 1, y, viz, elemente_in_bloc)
    if y < len(infoNod[0]) - 1 and infoNod[x][y] == infoNod[x][y + 1] and viz[x][y + 1] == 0 and infoNod[x][y] != '#':
        identifica_bloc(infoNod, x, y + 1, viz, elemente_in_bloc)

def identifica_blocuri(infoNod):
    viz = [[0 for _ in range(len(infoNod[0]))] for _ in range(len(infoNod))]
    lista_blocuri = []
    for i in range(len(infoNod)):
        for j in range(len(infoNod[i])):
            if viz[i][j] == 0 and infoNod[i][j]!='#':
                elemente_in_bloc = []
                identifica_bloc(infoNod, i, j, viz, elemente_in_bloc)
                lista_blocuri.append(elemente_in_bloc)
    return lista_blocuri

def refactor(infoNod):
    #caderea
    for x in range(len(infoNod)-1, -1, -1):
        for y in range(len(infoNod[x])-1, -1, -1):
            x_copy = copy.deepcopy(x)
            y_copy = copy.deepcopy(y)
            z = x_copy+1
            while z<=len(infoNod)-1 and infoNod[x_copy][y_copy]!='#' and infoNod[z][y_copy]=='#':
                infoNod[z][y_copy] = infoNod[x_copy][y_copy]
                infoNod[x_copy][y_copy] = '#'
                x_copy+=1
                z+=1
    #shiftarea la dreapta
    for x in range(len(infoNod)):
        for y in range(len(infoNod[x])):
            x_copy = copy.deepcopy(x)
            y_copy = copy.deepcopy(y)
            z = y-1
            while z>=0 and infoNod[x_copy][y_copy]!='#' and infoNod[x_copy][z]=='#':
                infoNod[x_copy][z]=infoNod[x_copy][y_copy]
                infoNod[x_copy][y_copy]='#'
                y_copy-=1
                z-=1

    return infoNod
