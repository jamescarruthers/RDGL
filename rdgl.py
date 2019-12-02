import math

class RDGL:
    def __init__ (self):
        self.cmds = "IN;DF;"
        self.size = [594, 420]
        self.plotScale = 0.025
        self.offset = [-309, -210]
        self.drawMode = "CENTER"

    def scale(self, n):
        return int(n / self.plotScale)

    def scaleX(self, x):
        return self.scale(x) + int(self.offset[0]/self.plotScale)

    def scaleY(self, y):
        return self.scale(y) + int(self.offset[1]/self.plotScale)

    # set buffer sizes
    # DPX-3300
    # IO buffer (1024, 2-15360), polygon buffer (3072, 2-15358), character buffer (0, 444-15358)
    # max of all three = 15358
    def buffer(self, P1, P2, P3):
        self.cmds += "\x1B.T{};{};{}:\n".format(P1, P2, P3)

    def init(self):
        self.cmds += "IN;DF;\n"
        self.inputWindow(0, 0, self.size[0], self.size[1])

    def penSelect(self, pen):
        self.cmds += "SP{};\n".format(pen)

    def rect(self, x, y, w, h):
        if (self.drawMode == "CENTER"):
            x -= (w/2)
            y -= (h/2)
        self.cmds += "PU{},{};ER{},{};\n".format(self.scaleX(x), self.scaleY(y), self.scale(w), self.scale(h))
        self.cmds += "RR{},{};\n".format(self.scale(w), self.scale(h))

    def rectFill(self, x, y, w, h):
        if (self.drawMode == "CENTER"):
            x -= (w/2)
            y -= (h/2)
        self.cmds += "PU{},{};RR{},{};\n".format(self.scaleX(x), self.scaleY(y), self.scale(w), self.scale(h))

    def circle(self, x, y, radius, resolution="5"):
        if (self.drawMode == "CORNER"):
            x += radius
            y += radius
        self.cmds += "PU{},{};CI{},{};\n".format(self.scaleX(x), self.scaleY(y), self.scale(radius), resolution)
    
    def arc(self, x, y, angle, resolution="5"):
        self.cmds += "AA{},{},{},{};\n".format(self.scaleX(x), self.scaleY(y), angle, resolution)    
    
    # Fill types
    # 1: cross directional fill (pen thickness)
    # 2: one directional fill (pen thickness)
    # 3: hatching (spacing)
    # 4: cross hatching (spacing)
    # 5: cross directional hatching (user defined fill)
    # 6: one directional hatching (user defined fill)
    def fillType(self, type, spacing, angle):
        self.cmds += "FT{},{},{};\n".format(type, self.scale(spacing), angle)

    def penForce(self, f):
        self.cmds += "FS{};\n".format(f)
    
    def penSpeed(self, s):
        self.cmds += "VS{};\n".format(int(s))
    
    def penThickness(self, mm):
        self.cmds += "PT{};\n".format(mm)

    def inputWindow(self, x1, y1, x2, y2):
        self.cmds += "IW{},{},{},{};\n".format(self.scaleX(x1), self.scaleY(y1), self.scaleX(x2), self.scaleY(y2))

    #start polygon mode
    def startPolygon(self):
        self.cmds += "PM0;"

    def closePolygon(self):
        self.cmds += "PM1;"

    def endPolygon(self):
        self.cmds += "PM2;"

    def drawPolygon(self):
        self.cmds += "EP;"

    def fillPolygon(self):
        self.cmds += "FP;"

    def penUp(self, *args):
        if len(args) > 0:
            self.cmds += "PU{},{};\n".format(self.scaleX(args[0][0]), self.scaleY(args[0][1]))
        else:
            self.cmds += "PU;\n"

    def penDown(self, *args):
        if len(args) > 0:
            self.cmds += "PD{},{};\n".format(self.scaleX(args[0][0]), self.scaleY(args[0][1]))
        else:
            self.cmds += "PD;\n"

    def penPath(self, path):
        self.cmds += "PU{},{};".format(self.scaleX(path[0][0]), self.scaleY(path[0][1]))
        self.cmds += "PD"
        for xy in path[1:-1]:
            self.cmds += "{},{},".format(self.scaleX(xy[0]), self.scaleY(xy[1]))
        self.cmds += "{},{};\n".format(self.scaleX(path[-1][0]), self.scaleY(path[-1][1]))

    def pathAverage(self, path):
        xTotal = 0
        yTotal = 0
        for xy in path:
            xTotal += xy[0]
            yTotal += xy[1]
        return [xTotal/len(path), yTotal/len(path)]

    def plotAbs(self, xy):
        self.cmds += "PA{},{};".format(self.scaleX(xy[0]), self.scaleY(xy[1]))

    def label(self, xy, label):
        self.cmds += "LB{},{}\x33".format(self.scaleX(xy[0]), self.scaleY(xy[1]))
        
        # RDGL command uses cm, but function expects mm to keep things consistent
    def labelSize(self, wh):
        self.cmds += "SI{},{};".format(wh[0]/10, wh[1]/10)
        
        # RDGL command uses radians, but function expects degrees to make things easier
    def labelSlant(self, slant):
        self.cmds += "SL{};".format(math.radians(slant))

    def RDGL(self, filename):
        self.cmds += "IN;DF;"
        f = open(filename, "w+")
        f.write(self.cmds)
        f.close()
