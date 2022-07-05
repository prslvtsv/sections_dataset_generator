
def check_corridor_states(layout, two_tiles_only=True):
    apartments = layout.get_apartments()
    for apt in apartments:
        cells_flattened = apt.active_cells()
        if two_tiles_only and len(cells_flattened) != 2:
            continue
        states = set()
        for cell in cells_flattened:
            try:
                state = cell.attrib['state']
                states.add(state)
            except:
                continue
        if states == {'corridor'}:
            return False
    return True

def get_space_type(layout, i, j):
    return layout.matrix.cells[i][j].spaceType

def neighbours_indeces(i, j, layout, apt):
    shape = layout.matrix.shape()
    ns = {'u': [i, j + 1],
          'r': [i + 1, j],
          'd': [i, j - 1],
          'l': [i - 1, j]}

    if i == 0:
        del ns['l']
    if i == shape[0] - 1:
        del ns['r']
    if j == 0:
        del ns['d']
    if j == shape[1] - 1:
        del ns['u']

    for k, (i, j) in ns.items():
        if not layout.matrix.cells[i][j].active:
            del ns[k]

    res = set()
    for k in ns.values():
        res.add(str(k[0]) + ',' + str(k[1]))
    return res

def check_corridor_neighbourhood(layout, door_tile=False):
    apartments = layout.get_apartments()
    if not door_tile:
        for apt in apartments:
            n_indeces = set()
            cells_flattened = [i.index(glob=True) for i in apt.active_cells()]
            for cell_coords in cells_flattened:
                i, j = cell_coords
                for n_coords in neighbours_indeces(i, j, layout, apt):
                    n_indeces.add(n_coords)
            cells_coords_set = set()
            for cell in cells_flattened:
                cells_coords_set.add(str(cell[0]) + ',' + str(cell[1]))
            cells_to_search = [tuple(int(j) for j in i.split(',')) for i in n_indeces.difference(cells_coords_set)]
            neighbours_space_types = [get_space_type(layout, i, j) for (i, j) in cells_to_search]
            if 'corridor' not in neighbours_space_types:
                return False
    else:
        # test for layout #6
        door_tile_dict = {0: (0, 1), 
                          1: (0, 0), 
                          2: (0, 0), 
                          3: (0, 0), 
                          4: (0, 0), 
                          5: (0, 0), 
                          6: (0, 2), 
                          7: (0, 0), 
                          8: (0, 0)}
        for apt_index, apt in enumerate(apartments):
            dt_i, dt_j = door_tile_dict[apt_index]
            i, j = apt.cells[dt_i][dt_j].index(glob=True)
            n_indeces = set()
            for n_coords in neighbours_indeces(i, j, layout, apt):
                n_indeces.add(n_coords)
            cells_coords_set = set()
            cells_flattened = [i.pos for i in apt.active_cells()]
            for cell in cells_flattened:
                cells_coords_set.add(str(cell[0]) + ',' + str(cell[1]))
            cells_to_search = [tuple(int(j) for j in i.split(',')) for i in n_indeces.difference(cells_coords_set)]
            neighbours_space_types = [get_space_type(layout, i, j) for (i, j) in cells_to_search]
            if 'corridor' not in neighbours_space_types:
                return False
    return True


def apply_verificator(layout):
    s = check_corridor_states(layout, two_tiles_only=True)
    n = check_corridor_neighbourhood(layout)
    return s and n

