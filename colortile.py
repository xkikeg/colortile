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


class ColorTileArray(object):
    def __init__(self):
        self.array = []

    def fixed_image_loader(self, filename):
        array = []
        im = Image.open(filename)
        for i in range(0,im.size[1]/25):
            row = []
            for j in range(0,im.size[0]/25):
                (r, g, b) = im.getpixel((j*25+12, i*25+12))
                tile_color = get_tilecolor(r, g, b)
                row.append(tile_color)
            array.append(row)
        self.array = array

    def __str__(self):
        return "\n".join((" ".join(char_tilecolor(j) for j in i) for i in self.array))

    def count(self, color):
        return sum(filter(lambda x: x == color,
                          reduce(lambda a,b: a+b, self.array)))

    def count_all(self):
        result = [0 for i in range(0, COLOR_MAX+1)]
        for i in self.array:
            for j in i:
                result[j] += 1
        return result

    def str_count_all(self):
        result = self.count_all()
        return "\n".join("%s: %d" % (str_tilecolor(i), result[i]) for i in range(0, len(result)))


if __name__=="__main__":
    x = ColorTileArray()
    x.fixed_image_loader(sys.argv[1])
    print x
    print x.str_count_all()
