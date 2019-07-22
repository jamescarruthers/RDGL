class RDGL:
    def __init__ (self):
        self.cmds = ""
        self.size = [594, 420]
        self.plotScale = 0.025
        self.offset = [-309, -210]
        self.drawMode = "CORNER"

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

    def circle(self, x, y, radius, resolution="5"):
        if (self.drawMode == "CORNER"):
            x += radius
            y += radius
        self.cmds += "PU{},{};CI{},{};\n".format(self.scaleX(x), self.scaleY(y), self.scale(radius), resolution)
        
    def fillType(self, type, spacing, angle):
        self.cmds += "FT{},{},{};\n".format(type, self.scale(spacing), angle)

    def penForce(self, f):
        self.cmds += "FS{};\n".format(f)
    
    def penSpeed(self, s):
        self.cmds += "VS{};\n".format(s)
    
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

    def RDGL(self, filename):
        f = open(filename, "w+")
        f.write(self.cmds)
        f.close()
