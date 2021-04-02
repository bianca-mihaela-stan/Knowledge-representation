"""
Observatie pentru cei absenti la laborator: trebuie sa dati enter după fiecare afișare a cozii până vă apare o soluție. Afișarea era ca să vedem progresul algoritmului. Puteți să o dezactivați comentând print-ul cu coada și input()
"""
import copy

# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    # initializeaza un nod din parcurgere
    def __init__(self, info, parinte, cost=0, h=0):
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost  # consider cost=1 pentru o mutare
        self.h = h
        # self.f = self.g + self.h

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

    def identifica_blocuri(self, x, y, viz, elemente_in_bloc):
        viz[x][y]=1
        elemente_in_bloc.append((x,y))
        if x>0 and self.info[x][y]==self.info[x-1][y]:
            self.identifica_blocuri(x-1, y, viz, elemente_in_bloc)
        if y>0 and self.info[x][y]==self.info[x][y-1]:
            self.identifica_blocuri(x, y-1, viz, elemente_in_bloc)
        if x<len(self.info)-1 and self.info[x][y]==self.info[x+1][y]:
            self.identifica_blocuri(x+1, y, viz, elemente_in_bloc)
        if x<len(self.info[0])-1 and self.info[x][y+1]==self.info[x][y+1]:
            self.identifica_blocuri(x, y+1, viz, elemente_in_bloc)


    def normalise(self):
        print("normalise")



class Graph:  # graful problemei
    def __init__(self, noduri, nrNoduri, start, k):
        self.noduri = noduri
        # self.matriceAdiacenta = matriceAdiacenta
        # self.matricePonderi = matricePonderi
        self.nrNoduri = nrNoduri
        self.start = start
        self.k = k
        # self.scopuri = scopuri

    def indiceNod(self, n):
        return self.noduri.index(n)

    def testeaza_scop(self, nodCurent):
        return nodCurent.info in self.scopuri;


    # va genera succesorii sub forma de noduri in arborele de parcurgere
    def genereazaSuccesori(self, nodCurent):
        listaSuccesori = []
        matrice_nod_curent = nodCurent.info
        print(nodCurent.info)
        nr_linii = len(matrice_nod_curent)
        viz =[]
        for linie  in nodCurent.info:
            new_linie =[]
            for i in linie:
                new_linie.append(0)
            viz.append(new_linie)

        lista_blocuri=[]
        for i in range(len(nodCurent.info)):
            for j in range(len(nodCurent.info[i])):
                if viz[i][j]==0:
                    elemente_in_bloc = []
                    nodCurent.identifica_blocuri(i, j, viz, elemente_in_bloc)
                    lista_blocuri.append(elemente_in_bloc)

        for bloc in lista_blocuri:
            if len(bloc)>=self.k:
                copie = copy.deepcopy(nodCurent.info)
                for tuplu in bloc:
                    x = tuplu[0]
                    y = tuplu[1]
                    copie.info[x][y]='#'
                listaSuccesori.append(copie)

        return listaSuccesori

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)



def parse_input():
    f = open("input.txt", 'r')
    k=int(f.readline())
    x= f.readline()
    stare_initiala = []
    while x:
        x=x.strip()
        linie = []
        for i in x:
            linie.append(i)
        stare_initiala.append(linie)
        x=f.readline()
    return stare_initiala, k

stare_initiala, k = parse_input()
noduri = []
noduri.append(stare_initiala)
gr = Graph(noduri, 1, stare_initiala, k)
c = [NodParcurgere(gr.noduri.index(gr.start), gr.start, 0, None)]
nodCurent = c.pop()
gr.genereazaSuccesori(nodCurent)


##############################################################################################
#                                 Initializare problema                                      #
##############################################################################################		

# pozitia i din vectorul de noduri da si numarul liniei/coloanei corespunzatoare din matricea de adiacenta
# noduri = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
#
# m = [
#     [0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
#     [1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
#     [0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
#     [1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
#     [1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
#     [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
#     [0, 0, 1, 0, 1, 0, 0, 0, 1, 1],
#     [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
# ]
#
# start = "a"
# scopuri = ["f", "j"]
# gr = Graph(noduri, m, start, scopuri)
#
#
#### algoritm BF
# presupunem ca vrem mai multe solutii (un numar fix) prin urmare vom folosi o variabilă numită nrSolutiiCautate
# daca vrem doar o solutie, renuntam la variabila nrSolutiiCautate
# si doar oprim algoritmul la afisarea primei solutii

# def breadth_first(gr, nrSolutiiCautate=1):
#     # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
#     c = [NodParcurgere(gr.noduri.index(gr.start), gr.start, 0, None)]
#
#     while len(c) > 0:
#         print("Coada actuala: " + str(c))
#         input()
#         nodCurent = c.pop(0)
#
#         if gr.testeaza_scop(nodCurent):
#             print("Solutie:")
#             nodCurent.afisDrum()
#             print("\n----------------\n")
#             input()
#             nrSolutiiCautate -= 1
#             if nrSolutiiCautate == 0:
#                 return
#         lSuccesori = gr.genereazaSuccesori(nodCurent)
#         c.extend(lSuccesori)
#
#
# def depth_first(gr, nrSolutiiCautate=1):
#     # vom simula o stiva prin relatia de parinte a nodului curent
#     df(NodParcurgere(gr.noduri.index(gr.start), gr.start, None), nrSolutiiCautate)
#
#
# def df(nodCurent, nrSolutiiCautate):
#     if nrSolutiiCautate == 0:  # testul acesta s-ar valida doar daca in apelul initial avem df(start,if nrSolutiiCautate=0)
#         return nrSolutiiCautate
#     print("Stiva actuala: " + "->".join(nodCurent.obtineDrum()))
#     input()
#     if gr.testeaza_scop(nodCurent):
#         print("Solutie: ", end="")
#         nodCurent.afisDrum()
#         print("\n----------------\n")
#         input()
#         nrSolutiiCautate -= 1
#         if nrSolutiiCautate == 0:
#             return nrSolutiiCautate
#     lSuccesori = gr.genereazaSuccesori(nodCurent)
#     for sc in lSuccesori:
#         if nrSolutiiCautate != 0:
#             nrSolutiiCautate = df(sc, nrSolutiiCautate)
#     return nrSolutiiCautate
#
#
# #############################################
#
#
# def dfi(nodCurent, adancime, nrSolutiiCautate):
#     print("Stiva actuala: " + "->".join(nodCurent.obtineDrum()))
#     input()
#     if adancime == 1 and gr.testeaza_scop(nodCurent):
#         print("Solutie: ", end="")
#         nodCurent.afisDrum()
#         print("\n----------------\n")
#         input()
#         nrSolutiiCautate -= 1
#         if nrSolutiiCautate == 0:
#             return nrSolutiiCautate
#     if adancime > 1:
#         lSuccesori = gr.genereazaSuccesori(nodCurent)
#         for sc in lSuccesori:
#             if nrSolutiiCautate != 0:
#                 nrSolutiiCautate = dfi(sc, adancime - 1, nrSolutiiCautate)
#     return nrSolutiiCautate
#
#
# def depth_first_iterativ(gr, nrSolutiiCautate=1):
#     for i in range(1, gr.nrNoduri + 1):
#         if nrSolutiiCautate == 0:
#             return
#         print("**************\nAdancime maxima: ", i)
#         nrSolutiiCautate = dfi(NodParcurgere(gr.noduri.index(gr.start), gr.start, None), i, nrSolutiiCautate)
#
#
# """
# Mai jos puteti comenta si decomenta apelurile catre algoritmi. Pentru moment e apelat doar breadth-first
# """
#
# # breadth_first(gr, nrSolutiiCautate=4)
#
# ####################################################3
#
#
# # depth_first(gr, nrSolutiiCautate=4)
#
# ##################################################
#
# depth_first_iterativ(gr, nrSolutiiCautate=4)

parse_input()
