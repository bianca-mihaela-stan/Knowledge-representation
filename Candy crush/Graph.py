from Node import Node
from helpers import map_characters, identify_zones, refactor
import copy


class Graph:
    def __init__(self, file_name, out):
        """
        Initializes a graph.
        """
        def build_configuration(sir, out):
            sir.strip()
            sir=sir.split("\n")
            n = 0
            matrix = []
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
                matrix.append(a)
            return matrix

        f = open(file_name, "r")
        self.k = int(f.readline())
        file_contents = f.read()
        self.start = build_configuration(file_contents, out)

    def test_goal(self, current_node):
        """
        Tests if a given node has reached the goal.
        """
        for linie in current_node.info:
            for x in linie:
                if x!='#':
                    return False
        return True

    def test_goal_info(self, node_info):
        """
        Tests if a given configuration has reached the goal.
        """
        for linie in node_info:
            for x in linie:
                if x!='#':
                    return False
        return True


    def generate_successors(self, current_node, heuristic="simple heuristic"):
        """
        Generates immediate successors from a given state.
        """
        successors = []
        ch_number = map_characters(current_node.info)
        zones=identify_zones(current_node.info)
        for bloc in zones:
            if len(bloc) >= self.k:
                copie = copy.deepcopy(current_node.info)
                for tuplu in bloc:
                    x = tuplu[0]
                    y = tuplu[1]
                    copie[x][y] = '#'

                caracterul_eliminat = current_node.info[bloc[0][0]][bloc[0][1]]
                nr_caractere_de_tipul_celui_eliminat = ch_number[caracterul_eliminat]
                cost = 1+(nr_caractere_de_tipul_celui_eliminat-len(bloc))/nr_caractere_de_tipul_celui_eliminat + current_node.g
                copie=refactor(copie)
                nodGenerat = Node(copie, current_node, cost, self.estimate_h(copie, heuristic), bloc, caracterul_eliminat)
                if nodGenerat.invalid_configuration(self.k) == False or self.test_goal(nodGenerat):
                    successors.append(nodGenerat)
        return successors

    def estimate_h(self, node_info, heuristic="simple heuristic"):
        """
        Estimates h for a given heuristic and a given configuration.
        Args:
            node_info (list(list(char))): A configuration of the board
            heuristic (string): the name of the heuristic used
        Returns:
            (list(list(tuple)): A list lists of elements in every zone.
        """
        if heuristic=="simple heuristic":
            if self.test_goal_info(node_info):
                return 0
            else:
                return 1
        elif heuristic == "first heuristic":       # adaug 1 pentru fiecare caracter
            return len(map_characters(node_info).keys())
        elif heuristic == "second heuristic":
            zones = identify_zones(node_info)
            nr_zones = len(zones)
            ch_number = map_characters(node_info)

            if nr_zones==0:
                return 0
            cost = 0
            for bloc in zones:
                ch = node_info[bloc[0][0]][bloc[0][1]]
                cost += 1 - len(bloc)/ch_number[ch]
            return cost

        elif heuristic == "invalid":
            zones = identify_zones(node_info)
            nr_zones = len(zones)
            ch_number = map_characters(node_info)

            if nr_zones == 0:
                return 0
            cost = 0
            for bloc in zones:
                ch = node_info[bloc[0][0]][bloc[0][1]]
                cost += 1 + (ch_number[ch]-len(bloc)) / ch_number[ch]
            return cost

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)
