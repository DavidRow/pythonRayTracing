from color import Color

class Image:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixles = [[None for _ in range(width)] for _ in range(height)]
    #set the individual pixels 
    def setPixle(self, x , y, col):
        self.pixles[y][x] = col
    #acctualy make the file 
    def writePPM(self, imgFile):
        def toByte(c):
            return round(max(min(c * 255, 255), 0))

        imgFile.write("P3 {} {}\n255\n".format(self.width, self.height))
        for row in self.pixles:
            for Color in row:
                imgFile.write("{} {} {} ".format(toByte(Color.x), toByte(Color.y), toByte(Color.z)))
            imgFile.write("\n")