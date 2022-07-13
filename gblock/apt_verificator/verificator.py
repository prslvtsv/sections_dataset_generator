import copy


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


def neighbours_indeces(i, j, layout):
    if layout.typename == "FloorLayout":
        shape = layout.matrix.shape()
    if layout.typename == "Apartment":
        shape = layout.shape()
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
        if layout.typename == "FloorLayout":
            if not layout.matrix.cells[i][j].active:
                del ns[k]
        if layout.typename == "Apartment":
            if not layout.cells[i][j].active:
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
                for n_coords in neighbours_indeces(i, j, layout):
                    n_indeces.add(n_coords)
            cells_coords_set = set()
            for cell in cells_flattened:
                cells_coords_set.add(str(cell[0]) + ',' + str(cell[1]))
            cells_to_search = [tuple(int(j) for j in i.split(','))
                               for i in n_indeces.difference(cells_coords_set)]
            neighbours_space_types = [get_space_type(
                layout, i, j) for (i, j) in cells_to_search]
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
            for n_coords in neighbours_indeces(i, j, layout):
                n_indeces.add(n_coords)
            cells_coords_set = set()
            cells_flattened = [i.pos for i in apt.active_cells()]
            for cell in cells_flattened:
                cells_coords_set.add(str(cell[0]) + ',' + str(cell[1]))
            cells_to_search = [tuple(int(j) for j in i.split(','))
                               for i in n_indeces.difference(cells_coords_set)]
            neighbours_space_types = [get_space_type(
                layout, i, j) for (i, j) in cells_to_search]
            if 'corridor' not in neighbours_space_types:
                return False
    return True


def get_tile_dims(tile):
    outline_pts = tile.outline_xyz()
    x_arr, y_arr = set(), set()
    for pt in outline_pts:
        x_arr.add(pt[0])
        y_arr.add(pt[1])
    dx = sorted(list(x_arr))[-1] - sorted(list(x_arr))[0]
    dy = sorted(list(y_arr))[-1] - sorted(list(y_arr))[0]
    return dx, dy


def get_tileset_dims(tileset):
    x_arr, y_arr = set(), set()
    for tile in tileset:
        outline_pts = tile.outline_xyz()
        for pt in outline_pts:
            x_arr.add(pt[0])
            y_arr.add(pt[1])
    dx = sorted(list(x_arr))[-1] - sorted(list(x_arr))[0]
    dy = sorted(list(y_arr))[-1] - sorted(list(y_arr))[0]
    return dx, dy


def check_corridor_corner_tile(corridor):
    shape = corridor.shape()
    if 1 in shape:
        return False
    else:
        return True


def get_corridor_corner_tile(corridor):
    cor_cells = corridor.active_cells()
    axis = 1 if cor_cells[0].index(
        glob=False)[0] == cor_cells[1].index(glob=False)[0] else 0
    for i, cell in enumerate(cor_cells[1:], 1):
        # find axis
        if cell.index(glob=False)[0] == cor_cells[i-1].index(glob=False)[0]:
            new_axis = 1
        else:
            new_axis = 0
        # rule for corner tile
        if new_axis != axis:
            corner_tile = cor_cells[i-1]
            return corner_tile
        axis = new_axis
    return None


def check_corridor_shape(layout):
    corridor = layout.get_corridor()[0]
    for cell in corridor.active_cells():
        i, j = cell.index(glob=False)
        if not 0 < len(neighbours_indeces(i, j, corridor)) < 3:
            return False
    return True


def get_tileset_length(tileset):
    cor_cells = copy.deepcopy(tileset)
    cor_cells[0].active = None
    axis = 1 if cor_cells[0].index(
        glob=False)[0] == cor_cells[1].index(glob=False)[0] else 0
    save_length = {0: get_tile_dims(cor_cells[0])[axis]}
    for i, cell in enumerate(cor_cells[1:], 1):
        # find axis
        if cell.index(glob=False)[0] == cor_cells[i-1].index(glob=False)[0]:
            new_axis = 1
        else:
            new_axis = 0
        # rule for corner tile
        if new_axis != axis:
            corner_cell = cor_cells[i-1]
            corner_cell_length = sum(get_tile_dims(corner_cell))/2
            save_length[i-1] = corner_cell_length
        axis = new_axis
        # save length
        save_length[i] = get_tile_dims(cell)[axis]
        cell.active = None
    tileset_length = sum(save_length.values())
    return tileset_length


def check_corridor_full_length(layout, max_length=35):
    corridor = layout.get_corridor()[0]
    cor_length = get_tileset_length(corridor.active_cells())
    return False if cor_length > max_length else True


def check_corridor_segments_lengths(layout, max_length_of_segment=25):
    mls = max_length_of_segment
    corridor = layout.get_corridor()[0]
    llu = layout.get_llu()
    llu_active_cells = [i.index(glob=True) for i in llu[0].active_cells()]
    llu_i, llu_j = llu_active_cells[0]  # indexes of elevator door
    corridor_cells = corridor.active_cells()
    corridor_coords = [i.index(glob=True) for i in corridor_cells]

    # find coords of llu neighbours
    n_i = [(int(i[0]), int(i[1])) for i in [coords.split(',')
                                            for coords in list(neighbours_indeces(llu_i, llu_j, layout))]]
    # find corridor neighbour
    cn_coords = [i for i in n_i if get_space_type(
        layout, i[0], i[1]) == 'corridor'][0]
    cn_index = corridor_coords.index(cn_coords)
    cn = corridor_cells[cn_index]
    cn_dims = get_tile_dims(cn)
    corner_tile = get_corridor_corner_tile(corridor)

    seg_1 = corridor_cells[:cn_index]
    seg_2 = corridor_cells[cn_index+1:]
    seg_1_length = get_tileset_length(seg_1)
    seg_2_length = get_tileset_length(seg_2)

    # check section type
    if corner_tile and cn_coords == corner_tile.index(glob=True):
        seg_1_axis = 1 if seg_1[0].pos[0] == seg_1[1].pos[0] else 0
        seg_2_axis = 0 if seg_1_axis == 1 else 1
        seg_1_length += cn_dims[seg_1_axis]/2
        seg_2_length += cn_dims[seg_2_axis]/2
    else:
        # add 1/2 of length of corridor_neighbour tile
        if corridor_cells[cn_index-1].index(glob=True)[0] == corridor_cells[cn_index+1].index(glob=True)[0]:
            seg_1_length += cn_dims[1]/2
            seg_2_length += cn_dims[1]/2
        else:
            seg_1_length += cn_dims[0]/2
            seg_2_length += cn_dims[0]/2
    return seg_1_length <= mls and seg_2_length <= mls


def apply_verificator(layout):
    if not check_corridor_shape(layout):
        print('corridor tiles are not shaped as a polyline')
        return None
    states = check_corridor_states(layout, two_tiles_only=True)
    neighbourhood = check_corridor_neighbourhood(layout)
    full_length = check_corridor_full_length(layout, max_length=50)
    segments_lengths = check_corridor_segments_lengths(
        layout, max_length_of_segment=25)

    return states and neighbourhood and full_length and segments_lengths
