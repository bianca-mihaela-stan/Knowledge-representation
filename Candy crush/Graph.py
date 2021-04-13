from NodParcurgere import NodParcurgere
from helpers import mapeaza_caractere, identifica_blocuri, refactor
import copy


class Graph:  # graful problemei
    def __init__(self, nume_fisier, out):
        def construiesteStare(sir, out):
            sir.strip()
            sir=sir.split("\n")
            n = 0
            matrice = []
            if sir == []:
                out.write("Invalid input file.")
                print("Invalid input file.")
                exit()
            else:
                n= len(sir[0])
            for linie in sir:
                if len(linie)!= n:
                    out.write("Invalid input file.")
                    print("Invalid input file.")
                    exit()
                a = []
                for x in linie:
                    a.append(x)
                matrice.append(a)
            return matrice

        f = open(nume_fisier, "r")
        self.k = int(f.readline())
        continut_fisier = f.read()
        self.start = construiesteStare(continut_fisier, out)

    def testeaza_scop(self, nodCurent):
        for linie in nodCurent.info:
            for x in linie:
                if x!='#':
                    return False
        return True

    def testeaza_scop_info(self, infoNod):
        for linie in infoNod:
            for x in linie:
                if x!='#':
                    return False
        return True

    # va genera succesorii sub forma de noduri in arborele de parcurgere

    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
        listaSuccesori = []
        # itdentifica toate "blocurile" din aceasta matrice si le pune in lista_blocuri
        ch_number = mapeaza_caractere(nodCurent.info)
        lista_blocuri=identifica_blocuri(nodCurent.info)
        for bloc in lista_blocuri:
            if len(bloc) >= self.k:
                copie = copy.deepcopy(nodCurent.info)
                for tuplu in bloc:
                    x = tuplu[0]
                    y = tuplu[1]
                    copie[x][y] = '#'

                caracterul_eliminat = nodCurent.info[bloc[0][0]][bloc[0][1]]
                nr_caractere_de_tipul_celui_eliminat = ch_number[caracterul_eliminat]
                cost = 1+(nr_caractere_de_tipul_celui_eliminat-len(bloc))/nr_caractere_de_tipul_celui_eliminat + nodCurent.g
                copie=refactor(copie)
                nodGenerat = NodParcurgere(copie, nodCurent, cost, self.calculeaza_h(copie, tip_euristica), bloc, caracterul_eliminat)
                if nodGenerat.situatie_invalida(self.k) == False or self.testeaza_scop(nodGenerat):
                    listaSuccesori.append(nodGenerat)
        return listaSuccesori

    # euristica banala
    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
        if tip_euristica=="euristica banala":
            if self.testeaza_scop_info(infoNod) ==True:
                return 0
            else:
                return 1
        elif tip_euristica=="euristica1":       # adaug 1 pentru fiecare caracter
            return len(mapeaza_caractere(infoNod).keys())
        elif tip_euristica=="euristica2":
            lista_blocuri = identifica_blocuri(infoNod)
            nr_blocuri = len(lista_blocuri)
            ch_number = mapeaza_caractere(infoNod)

            if nr_blocuri==0:
                return 0
            cost = 0
            for bloc in lista_blocuri:
                ch = infoNod[bloc[0][0]][bloc[0][1]]
                cost+= 1 - len(bloc)/ch_number[ch]


            return cost
        elif tip_euristica=="neadmisibila":

            lista_blocuri = identifica_blocuri(infoNod)
            nr_blocuri = len(lista_blocuri)
            ch_number = mapeaza_caractere(infoNod)

            if nr_blocuri == 0:
                return 0
            cost = 0
            for bloc in lista_blocuri:
                ch = infoNod[bloc[0][0]][bloc[0][1]]
                cost += 1 + (ch_number[ch]-len(bloc)) / ch_number[ch]
            return cost

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)
