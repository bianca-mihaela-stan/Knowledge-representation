import copy

def map_characters(node_info):
    """
    Maps every character to the number of each character on the board.
    Args:
        node_info list(list(char)): A configuration of the board
    Returns:
          dictionary of chars to ints: ch_number[x] = number of instances of x in the board
    """
    ch_number = {}
    for line in node_info:
        for ch in line:
            if ch in ch_number.keys():
                ch_number[ch] += 1
            else:
                ch_number[ch] = 1
    return ch_number


def identify_zone(node_info, x, y, viz, elements_in_zone):
    """
    Identifies the zone around character at position (x,y).
     Args:
        node_info (list(list(char))): A configuration of the board
        x (int): index of line of element
        y (int): index of column of element
        viz (list(list(int))): a matrix that marks whether we counted a character or not
        elements_in_zone (list(tuple)): a list with the positions all the elements in identified zone
    Returns:
          dictionary of chars to ints: ch_number[x] = number of instances of x in the board
    """
    viz[x][y] = 1
    elements_in_zone.append((x, y))
    if x > 0 and node_info[x][y] == node_info[x - 1][y] and viz[x - 1][y] == 0 and node_info[x][y] != '#':
        identify_zone(node_info, x - 1, y, viz, elements_in_zone)
    if y > 0 and node_info[x][y] == node_info[x][y - 1] and viz[x][y - 1] == 0 and node_info[x][y] != '#':
        identify_zone(node_info, x, y - 1, viz, elements_in_zone)
    if x < len(node_info) - 1 and node_info[x][y] == node_info[x + 1][y] and viz[x + 1][y] == 0 and node_info[x][y] != '#':
        identify_zone(node_info, x + 1, y, viz, elements_in_zone)
    if y < len(node_info[0]) - 1 and node_info[x][y] == node_info[x][y + 1] and viz[x][y + 1] == 0 and node_info[x][y] != '#':
        identify_zone(node_info, x, y + 1, viz, elements_in_zone)

def identify_zones(node_info):
    """
    Identifies distinct zones on the board.
    Args:
        node_info list(list(char)): A configuration of the board
    Returns:
        (list(list(tuple)): A list lists of elements in every zone.
    """
    viz = [[0 for _ in range(len(node_info[0]))] for _ in range(len(node_info))]
    zones = []
    for i in range(len(node_info)):
        for j in range(len(node_info[i])):
            if viz[i][j] == 0 and node_info[i][j]!='#':
                elements_in_zone = []
                identify_zone(node_info, i, j, viz, elements_in_zone)
                zones.append(elements_in_zone)
    return zones

def refactor(node_info):
    """
    Refactoring the board after every move.
     Args:
        node_info list(list(char)): A configuration of the board
    Returns:
        list(list(char)): A new configuration of the board
    """
    # the fall
    for x in range(len(node_info)-1, -1, -1):
        for y in range(len(node_info[x])-1, -1, -1):
            x_copy = copy.deepcopy(x)
            y_copy = copy.deepcopy(y)
            z = x_copy+1
            while z<=len(node_info)-1 and node_info[x_copy][y_copy]!='#' and node_info[z][y_copy]=='#':
                node_info[z][y_copy] = node_info[x_copy][y_copy]
                node_info[x_copy][y_copy] = '#'
                x_copy+=1
                z+=1
    # the right shift
    for x in range(len(node_info)):
        for y in range(len(node_info[x])):
            x_copy = copy.deepcopy(x)
            y_copy = copy.deepcopy(y)
            z = y-1
            while z>=0 and node_info[x_copy][y_copy]!='#' and node_info[x_copy][z]=='#':
                node_info[x_copy][z]=node_info[x_copy][y_copy]
                node_info[x_copy][y_copy]='#'
                y_copy-=1
                z-=1

    return node_info
