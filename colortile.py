import sys
import array

import Image

CELL_SIZE = 25

WL = -1 # Wall
BG = 0 # BackGround
GY = 1 # GraY
BL = 2 # BLue
CY = 3 # CYan
GR = 4 # GReen
YL = 5 # YeLlow
BR = 6 # BRown
OG = 7 # OranGe
RD = 8 # ReD
PK = 9 # PinK
MG = 10 # MaGenta

COLOR_MAX = MG

COLOR_TO_CHAR = {
    WL: "#",
    BG: "-",
    GY: "g",
    BL: "B",
    CY: "c",
    GR: "G",
    YL: "y",
    BR: "b",
    OG: "o",
    RD: "R",
    PK: "p",
    MG: "m"
    }

COLOR_TO_STR = {
    WL: "WL",
    BG: "BG",
    GY: "GY",
    BL: "BL",
    CY: "CY",
    GR: "GR",
    YL: "YL",
    BR: "BR",
    OG: "OG",
    RD: "RD",
    PK: "PK",
    MG: "MG"
    }


def char_tilecolor(color):
    if color in COLOR_TO_CHAR:
        return COLOR_TO_CHAR[color]
    else: return "?"

def str_tilecolor(color):
    if color in COLOR_TO_STR:
        return COLOR_TO_STR[color]
    else: return "??"

def get_tilecolor(r, g, b):
    if r == g == b:
        if r < 0xe0:
            return GY
        else:
            return BG
    elif r < g < b:
        return BL
    elif r < g == b:
        return CY
    elif b == r < g:
        return GR
    elif r == g > b:
        return YL
    elif r > g > b:
        if r == 0xff:
            return OG
        else:
            return BR
    elif r > g == b:
        return RD
    elif g < b == r:
        if r == 0xff:
            return PK
        else:
            return MG
    else:
        return -1

def is_tile(color):
    return color > 0


class ColorTileArray(object):
    def __init__(self):
        self.tile_array = None

    def fixed_image_loader(self, filename):
        tile_array = array.array('b')
        im = Image.open(filename)
        self.height = im.size[1] / CELL_SIZE
        self.width = im.size[0] / CELL_SIZE
        for i in range(0, self.height):
            for j in range(0, self.width):
                r, g, b = im.getpixel((j*25+12, i*25+12))[:3]
                tile_color = get_tilecolor(r, g, b)
                tile_array.append(tile_color)
        self.tile_array = tile_array

    def __str__(self):
        return "\n".join((" ".join(char_tilecolor(self.at(i, j)) for j in range(0, self.width))) for i in range(0, self.height))

    def index_to_pos(self, index):
        return (index / self.width, index % self.width)

    def at(self, x, y):
        return self.tile_array[x * self.width + y]

    def assign(self, x, y, color):
        self.tile_array[x * self.width + y] = color

    def count(self, color):
        return self.tile_array.count(color)

    def count_all(self):
        result = [0 for i in range(0, COLOR_MAX+1)]
        for i in self.tile_array:
            result[i] += 1
        return result

    def str_count_all(self):
        result = self.count_all()
        return "\n".join("%s: %d" % (str_tilecolor(i), result[i]) for i in range(0, len(result)))

    def position_all(self):
        result = [[] for i in range(0, COLOR_MAX+1)]
        for index, cell in enumerate(self.tile_array):
            result[cell].append(self.index_to_pos(index))
        return result


    def is_good_state(self):
        positions = self.position_all()[1:]
        # Bad state if there is the isolate tile
        if 1 in map(lambda x: len(x), positions): return False
        # Bad state if there are only three tiles with same color and cannot delete all
        for poss in filter(lambda x: len(x) == 3, positions):
            p1, p2, p3 = sorted(poss, key=lambda x: x[0])
            if not p1[0] < p2[0] < p3[0] or not p1[1] == p3[1] != p2[1]:
                return False
            p1, p2, p3 = sorted(poss, key=lambda x: x[1])
            if not p1[1] < p2[1] < p3[1] or not p1[0] == p3[0] != p2[0]:
                return False
        return True

    def is_solved(self):
        return len(self.tile_array) == self.count(BG)

    def get_neighbor(self, iter):
        for i,color in enumerate(iter):
            if is_tile(color): return (i+1, color)
        return (None, None)

    def legal_moves(self):
        moves = []
        for i in range(0, self.height):
            for j in range(0, self.width):
                if is_tile(self.at(i, j)): continue
                column = [ self.at(k, j) for k in range(0, self.height) ]
                row = self.tile_array[i*self.height:(i+1)*self.height]
                u_idx, u_color = self.get_neighbor(reversed(column[:i]))
                d_idx, d_color = self.get_neighbor(column[i+1:])
                l_idx, l_color = self.get_neighbor(reversed(row[:j]))
                r_idx, r_color = self.get_neighbor(row[j+1:])
                u = None if u_idx is None else (u_color, ((i - u_idx, j), ))
                d = None if d_idx is None else (d_color, ((i + d_idx, j), ))
                l = None if l_idx is None else (l_color, ((i, j - l_idx), ))
                r = None if r_idx is None else (r_color, ((i, j + r_idx), ))
                tileplus = lambda x, y: ((x[0], x[1] + y[1]),) if x[0] == y[0] else (x, y)
                tiles = filter(lambda a: len(a[1]) >= 2,
                               reduce(lambda a,b: a[:-1] + tileplus(a[-1], b) if len(a) > 0 else (b,),
                                      sorted(filter(lambda x: x is not None, (u,d,l,r))), ()))
                len(tiles) > 0 and moves.append(((i, j), tiles))
        return moves

    def search_depth_first(self):
        # If this state is not good, then return
        if not self.is_good_state(): return ()
        # Get legal moves, and return if there are no moves
        moves = self.legal_moves()
        if len(moves) == 0: return ()
        # See all moves
        for move, tiles in moves:
            # Drop tiles in this move
            for color, d_pos in tiles:
                for p in d_pos:
                    self.assign(p[0], p[1], BG)
            # If there are no tiles, return move
            # Else recursively call search_depth_first()
            print " ".join(str(i) for i in self.count_all()), move, tiles
            if self.is_solved():
                retval = (move,)
            else:
                branch = self.search_depth_first()
                retval = (move,) + branch if len(branch) > 0 else ()
            # Restore dropped tiles
            for color, d_pos in tiles:
                for p in d_pos:
                    self.assign(p[0], p[1], color)
            # Return move if this is valid route
            if len(retval) > 0:
                return retval
        # End of seaching all moves
        return ()


if __name__=="__main__":
    x = ColorTileArray()
    x.fixed_image_loader(sys.argv[1])
    print x
    print x.str_count_all()
    print x.search_depth_first()
