"""
Dati enter dupa fiecare solutie afisata.

Presupunem ca avem costul de mutare al unui bloc egal cu indicele in alfabet, cu indicii incepănd de la 1 (care se calculează prin 1+ diferenta dintre valoarea codului ascii al literei blocului de mutat si codul ascii al literei "a" ) .
"""

import copy


# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    # initializeaza un nod din parcurgere
    def __init__(self, info, parinte, cost=0, h=0):
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost
        self.h = h
        self.f = self.g + self.h

    # obtine o lista cu drumul de la nodul de start la nodul care apeleaza
    def obtineDrum(self):
        l = [self];
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    # afiseaza drumul de la nodul de start la nodul care apeleaza
    def afisDrum(self, afisCost=False, afisLung=False):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        for nod in l:
            print(str(nod))
        if afisCost:
            print("Cost: ", self.g)
        if afisCost:
            print("Lungime: ", len(l))
        return len(l)

    # verifica daca informatiile unui nod se afla in drumul de la radacina la nodul care apeleaza
    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:
            if (infoNodNou == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte

        return False

    def __repr__(self):
        sir = ""
        sir += str(self.info)
        return (sir)

    # euristica banală: daca nu e stare scop, returnez 1, altfel 0

    """
    def __str__(self):
        sir=""
        maxInalt=max([len(stiva) for stiva in self.info])
        for inalt in range(maxInalt, 0, -1):
            for stiva in self.info:
                if len(stiva)< inalt:
                    sir+="  "
                else:
                    sir+=stiva[inalt-1]+" "
            sir+="\n"
        sir+="-"*(2*len(self.info)-1)
        return sir
    """

    def __str__(self):
        sir = ""
        for stiva in self.info:
            sir += (str(stiva)) + "\n"
        sir += "--------------\n"
        return sir

    def identifica_blocuri(self, x, y, viz, elemente_in_bloc):
        viz[x][y]=1
        elemente_in_bloc.append((x,y))
        if x>0 and self.info[x][y]==self.info[x-1][y] and viz[x-1][y]==0 and self.info[x][y]!='#':
            self.identifica_blocuri(x-1, y, viz, elemente_in_bloc)
        if y>0 and self.info[x][y]==self.info[x][y-1] and viz[x][y-1]==0 and self.info[x][y]!='#':
            self.identifica_blocuri(x, y-1, viz, elemente_in_bloc)
        if x<len(self.info)-1 and self.info[x][y]==self.info[x+1][y] and viz[x+1][y]==0 and self.info[x][y]!='#':
            self.identifica_blocuri(x+1, y, viz, elemente_in_bloc)
        if y<len(self.info[0])-1 and self.info[x][y]==self.info[x][y+1] and viz[x][y+1]==0 and self.info[x][y]!='#':
            self.identifica_blocuri(x, y+1, viz, elemente_in_bloc)

    def refactor(self):
        modificari = True
        while modificari == True:
            for linie in self.info:
                while linie[0]=='#' and linie!='#'*len(linie):
                    shift_left(linie)


def shift_left(linie):
    for i in range(len(linie)-1):
        linie[i]=linie[i+1]
    linie[len(linie)-1]='#'


class Graph:  # graful problemei
    def __init__(self, nume_fisier):
        def construiesteStare(sir):
            sir.strip()
            sir=sir.split("\n")
            matrice = []
            for linie in sir:
                a = []
                for x in linie:
                    a.append(x)
                matrice.append(a)
            return matrice

        f = open(nume_fisier, "r")
        self.k = int(f.readline())
        continutfisier = f.read()
        self.start = construiesteStare(continutfisier)

    def testeaza_scop(self, nodCurent):
        for linie in nodCurent.info:
            for x in linie:
                if x!='#':
                    return False
        return True

    # va genera succesorii sub forma de noduri in arborele de parcurgere

    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
        listaSuccesori = []
        matrice_nod_curent = nodCurent.info
        nr_elem_matrice = len(matrice_nod_curent)* len(matrice_nod_curent[0])
        nr_linii = len(matrice_nod_curent)
        viz = []
        for linie in nodCurent.info:
            new_linie = []
            for i in linie:
                new_linie.append(0)
            viz.append(new_linie)

        lista_blocuri = []
        for i in range(len(nodCurent.info)):
            for j in range(len(nodCurent.info[i])):
                if viz[i][j] == 0:
                    elemente_in_bloc = []
                    nodCurent.identifica_blocuri(i, j, viz, elemente_in_bloc)
                    lista_blocuri.append(elemente_in_bloc)

        for bloc in lista_blocuri:
            if len(bloc) >= self.k:
                copie = copy.deepcopy(nodCurent.info)
                for tuplu in bloc:
                    x = tuplu[0]
                    y = tuplu[1]
                    copie[x][y] = '#'

                listaSuccesori.append(NodParcurgere(copie, nodCurent, 1, 1+(nr_elem_matrice-len(bloc))/nr_elem_matrice).refactor())

        return listaSuccesori


    # euristica banala
    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
        return 0


    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)


def breadth_first(gr, nrSolutiiCautate):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None)]

    while len(c) > 0:
        # print("Coada actuala: " + str(c))
        # input()
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            print("Solutie:")
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            print("\n----------------\n")
            input()
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        c.extend(lSuccesori)


def uniform_cost(gr, nrSolutiiCautate=1):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]

    while len(c) > 0:
        print("Coada actuala: " + str(c))
        input()
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            print("Solutie: ", end="")
            nodCurent.afisDrum()
            print("\n----------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # ordonez dupa cost(notat cu g aici și în desenele de pe site)
                if c[i].g > s.g:
                    gasit_loc = True
                    break;
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


def a_star(gr, nrSolutiiCautate, tip_euristica):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]

    while len(c) > 0:
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            print("Solutie: ")
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            print("\n----------------\n")
            input()
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # diferenta fata de UCS e ca ordonez dupa f
                if c[i].f >= s.f:
                    gasit_loc = True
                    break;
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


gr = Graph("input.txt")
c = [NodParcurgere(gr.start, None, 0)]
gr.genereazaSuccesori(c[0])

# Rezolvat cu breadth first
# print("Solutii obtinute cu breadth first:")
# breadth_first(gr, nrSolutiiCautate=3)

print("\n\n##################\nSolutii obtinute cu UCS:")
# print("\nObservatie: stivele sunt afisate pe orizontala, cu baza la stanga si varful la dreapta.")
uniform_cost(gr, nrSolutiiCautate=4)
# print("\n\n##################\nSolutii obtinute cu A*:")
# a_star(gr, nrSolutiiCautate=3,tip_euristica="euristica nebanala")


"""
a b c
d e
g


g e c
d a b
|

"""