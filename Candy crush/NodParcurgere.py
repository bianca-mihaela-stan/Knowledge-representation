import copy
from helpers import identifica_blocuri

class NodParcurgere:
    # initializeaza un nod din parcurgere
    def __lt__(self, other):
        if self.f == other.f:
            return self.g > other.g
            return self.g > other.g
        return self.f < other.g


    def __hash__(self):
        return hash((repr(self.info), self.parinte, self.g, self.h, self.f))

    def __init__(self, info, parinte, cost=0, h=0, caractere_eliminate=None, caracter_eliminat=None):
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost
        self.h = h
        self.f = self.g + self.h
        self.caractere_eliminate=caractere_eliminate
        self.caractere_eliminat = caracter_eliminat

    # obtine o lista cu drumul de la nodul de start la nodul care apeleaza
    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    # afiseaza drumul de la nodul de start la nodul care apeleaza
    def afisDrum(self, out, timp, max_noduri, total_noduri, afisCost=False, afisLung=False):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        for nod in l:
            out.write(str(nod))
        for x in range(len(l[0].info)):
            for y in range(len(l[0].info[x])):
                if y==0:
                    out.write("[")
                if y==len(l[0].info[x])-1:
                    out.write("'#']<br>")
                else:
                    out.write("'#',")
        out.write("--------------<br>")

        if afisCost:
            out.write("Cost: "+ "%.2f" % self.g + "<br>")
            print("%.2f" % self.g +"\n")
        if afisCost:
            out.write("Lungime: "+ str(len(l))+ "<br>")
        out.write("Timp necesar: " + "%.2f" % timp + " s <br>")
        out.write("Maximul numarului de noduri tinut in memorie: " + str(max_noduri) + "<br>")
        out.write("Numarul total de noduri generate: " + str(total_noduri)+ "<br>")

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


    def __str__(self, ):
        sir = ""
        if self.parinte!=None:
            for x in range(len(self.parinte.info)):
                for y in range(len(self.parinte.info[x])):
                    if y == 0:
                        sir+="["
                    if (x,y) in self.caractere_eliminate:
                        sir+= "<mark> " + self.parinte.info[x][y] + "</mark>"
                    else:
                        sir += self.parinte.info[x][y]
                    if y == len(self.parinte.info[x])-1:
                        sir+="] <br>"
                    else:
                        sir+=","
        sir += "--------------<br>"
        return sir



    def situatie_invalida(self, k):
        niciun_bloc = True
        caracter_insuficient = False
        viz=[]
        for linie in self.info:
            new_linie = []
            for i in linie:
                new_linie.append(0)
            viz.append(new_linie)
        caractere=set()
        ch_number = {}
        lista_blocuri=[]
        for x in range(len(self.info)):
            for y in range(len(self.info[x])):
                elemente_in_bloc=[]
                if self.info[x][y]!='#':
                    caractere.add(self.info[x][y])
                lista_blocuri = identifica_blocuri(self.info)

        for bloc in lista_blocuri:
            if len(bloc)>=k:
                niciun_bloc=False

        if niciun_bloc==True:
            return True

        for caracter in ch_number.keys():
            if ch_number[caracter]<k:
                caracter_insuficient=True

        if caracter_insuficient==True:
            return True
        return False