import Image
import sys

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
        self.array = []

    def fixed_image_loader(self, filename):
        array = []
        im = Image.open(filename)
        for i in range(0,im.size[1]/25):
            row = []
            for j in range(0,im.size[0]/25):
                r, g, b = im.getpixel((j*25+12, i*25+12))[:3]
                tile_color = get_tilecolor(r, g, b)
                row.append(tile_color)
            array.append(row)
        self.array = array

    def __str__(self):
        return "\n".join((" ".join(char_tilecolor(j) for j in i) for i in self.array))

    def count(self, color):
        return reduce(lambda a,b: a+b, self.array).count(color)

    def count_all(self):
        result = [0 for i in range(0, COLOR_MAX+1)]
        for i in self.array:
            for j in i:
                result[j] += 1
        return result

    def str_count_all(self):
        result = self.count_all()
        return "\n".join("%s: %d" % (str_tilecolor(i), result[i]) for i in range(0, len(result)))


    def is_good_state(self):
        counts = self.count_all()[1:]
        if len(filter(lambda x: x == 1, counts)) > 0: return False
        return True

    def is_solved(self):
        return len(reduce(lambda a,b: a+b, self.array)) == self.count(BG)

    def get_neighbor(self, iter):
        for i,color in enumerate(iter):
            if is_tile(color): return (i+1, color)
        return (None, None)

    def legal_moves(self):
        moves = []
        for i in range(0, len(self.array)):
            for j in range(0, len(self.array[i])):
                if is_tile(self.array[i][j]): continue
                column = [ self.array[k][j] for k in range(0, len(self.array)) ]
                row = self.array[i]
                u_idx, u_color = self.get_neighbor(reversed(column[:i]))
                d_idx, d_color = self.get_neighbor(column[i+1:])
                l_idx, l_color = self.get_neighbor(reversed(row[:j]))
                r_idx, r_color = self.get_neighbor(row[j+1:])
                u = None if u_idx is None else (u_color, ((i - u_idx, j), ))
                d = None if d_idx is None else (d_color, ((i + d_idx, j), ))
                l = None if l_idx is None else (l_color, ((i, j - l_idx), ))
                r = None if r_idx is None else (r_color, ((i, j + r_idx), ))
                tileplus = lambda x, y: [(x[0], x[1]+y[1])] if x[0] == y[0] else [x, y]
                tiles = filter(lambda a: len(a[1]) >= 2,
                               reduce(lambda a,b: a[:-1] + tileplus(a[-1], b) if len(a) > 0 else [b],
                                      sorted(filter(lambda x: x is not None, (u,d,l,r))), []))
                len(tiles) > 0 and moves.append(((i, j), tiles))
        return moves

    def search_depth_first(self):
        assert len(self.array) > 0, "Array is not filled"
        # If this state is not good, then return
        if not self.is_good_state(): return ()
        # Get legal moves, and return if there are no moves
        moves = self.legal_moves()
        if len(moves) == 0: return ()
        # See all moves
        for move, tiles in moves:
            # Drop tiles in this move
            for color, d_pos in tiles:
                for i in d_pos:
                    self.array[i[0]][i[1]] = BG
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
                for i in d_pos:
                    self.array[i[0]][i[1]] = color
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
