import copy
from helpers import identify_zones

class Node:
    def __lt__(self, other):
        """
        Compares 2 nodes.
        """
        if self.f == other.f:
            return self.g > other.g
        return self.f < other.g

    def __init__(self, info, parent, cost=0, h=0, removed_characters=None, removed_character=None):
        """
        Initializes a node.
        """
        self.info = info
        self.parent = parent 
        self.g = cost
        self.h = h
        self.f = self.g + self.h
        self.removed_characters=removed_characters
        self.removed_character = removed_character

    def get_path(self):
        """
        Returns a list of all the nodes from start to current node.
        """
        l = [self]
        nod = self
        while nod.parent is not None:
            l.insert(0, nod.parent)
            nod = nod.parent
        return l

    def output_path(self, out, timp, max_noduri, total_noduri, afisCost=False, afisLung=False):  
        """
        Outputs to out the path from start to the current node.
        """
        l = self.get_path()
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
            out.write("Length: "+ str(len(l))+ "<br>")
        out.write("Time: " + "%.2f" % timp + " s <br>")
        out.write("Maximum number of nodes: " + str(max_noduri) + "<br>")
        out.write("Total number of nodes: " + str(total_noduri)+ "<br>")

    def contains_in_path(self, infoNodNou):
        """
        Returns if a certain configuration was encountered on the path from the start node to the current node.
        """
        nodDrum = self
        while nodDrum is not None:
            if (infoNodNou == nodDrum.info):
                return True
            nodDrum = nodDrum.parent

        return False

    def __repr__(self):
        sir = ""
        sir += str(self.info)
        return (sir)


    def __str__(self, ):
        """
        Transforms the current node into a string ready to be viewed in an html file.
        """
        sir = ""
        if self.parent!=None:
            for x in range(len(self.parent.info)):
                for y in range(len(self.parent.info[x])):
                    if y == 0:
                        sir+="["
                    if (x,y) in self.removed_characters:
                        sir+= "<mark> " + self.parent.info[x][y] + "</mark>"
                    else:
                        sir += self.parent.info[x][y]
                    if y == len(self.parent.info[x])-1:
                        sir+="] <br>"
                    else:
                        sir+=","
        sir += "--------------<br>"
        return sir



    def invalid_configuration(self, k):
        """
        Checks if a node cannot result in a goal configuration.
        Params:
            k (int) : minimum number of characters for a zone, as given in the command line.
        Returns:
            (bool) : True if the configuration is invalid, False if it is valid
        """
        no_zone = True
        insufficient_character = False
        viz=[]
        for linie in self.info:
            new_linie = []
            for i in linie:
                new_linie.append(0)
            viz.append(new_linie)
            
        characters=set()
        ch_number = {}
        lista_blocuri=[]
        for x in range(len(self.info)):
            for y in range(len(self.info[x])):
                if self.info[x][y]!='#':
                    characters.add(self.info[x][y])
                lista_blocuri = identify_zones(self.info)

        for bloc in lista_blocuri:
            if len(bloc)>=k:
                no_zone=False

        if no_zone==True:
            return True

        for character in ch_number.keys():
            if ch_number[character]<k:
                insufficient_character=True

        if insufficient_character==True:
            return True
        return False