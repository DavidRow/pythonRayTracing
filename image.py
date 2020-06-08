from color import Color

#this class creates the image itsekf
class Image:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixles = [[None for _ in range(width)] for _ in range(height)]
    #set the individual pixels NOTE: all pixels must be filled in
    def setPixle(self, x , y, col):
        self.pixles[y][x] = col

    
    #acctualy make the file, and puts colors in it 
    def writePPM(self, imgFile):
        # makes sure it's in range of 255 - 0
        def flatten(c):
            return round(max(min(c, 255), 0))
        
        #set up beggining of file
        imgFile.write("P3 {} {}\n255\n".format(self.width, self.height))

        #adds in color
        for row in self.pixles:
            for Color in row:
                imgFile.write("{} {} {} ".format(flatten(Color.x), flatten(Color.y), flatten(Color.z)))
            imgFile.write("\n")