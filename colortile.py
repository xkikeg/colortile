import Image
import sys

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

def str_tilecolor(color):
    if color == BG: return "-"
    elif color == GY: return "g"
    elif color == BL: return "B"
    elif color == CY: return "c"
    elif color == GR: return "G"
    elif color == YL: return "y"
    elif color == BR: return "b"
    elif color == OG: return "o"
    elif color == RD: return "R"
    elif color == PK: return "p"
    elif color == MG: return "m"
    else: return "#"

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
        return "\n".join((" ".join(str_tilecolor(j) for j in i) for i in self.array))
    def count(self):
        array = reduce(lambda a,b: a+b, self.array)
        print "GY: %d" % (sum(filter(lambda x: x == GY, array))/GY)
        print "BL: %d" % (sum(filter(lambda x: x == BL, array))/BL)
        print "CY: %d" % (sum(filter(lambda x: x == CY, array))/CY)
        print "GR: %d" % (sum(filter(lambda x: x == GR, array))/GR)
        print "YL: %d" % (sum(filter(lambda x: x == YL, array))/YL)
        print "BR: %d" % (sum(filter(lambda x: x == BR, array))/BR)
        print "OG: %d" % (sum(filter(lambda x: x == OG, array))/OG)
        print "RD: %d" % (sum(filter(lambda x: x == RD, array))/RD)
        print "PK: %d" % (sum(filter(lambda x: x == PK, array))/PK)
        print "MG: %d" % (sum(filter(lambda x: x == MG, array))/MG)

if __name__=="__main__":
    x = ColorTileArray()
    x.fixed_image_loader(sys.argv[1])
    print x
    x.count()
