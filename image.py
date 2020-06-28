from color import Color
from PIL import Image as Im
import numpy as np
#this class creates the image itsekf
class Image:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixles = [[None for _ in range(width)] for _ in range(height)]
    #set the individual pixels NOTE: all pixels must be filled in
    def setPixle(self, x , y, col):
        self.pixles[y][x] = col
    # makes sure it's in range of 255 - 0
    def flatten(self, c):
        return round(max(min(c, 255), 0))
    
    #acctualy make the file, and puts colors in it 
    def writePPM(self, imgFile):
        #set up beggining of file
        imgFile.write("P3 {} {}\n255\n".format(self.width, self.height))

        #adds in color
        for row in self.pixles:
            for Color in row:
                imgFile.write("{} {} {} ".format(self.flatten(Color.x), self.flatten(Color.y), self.flatten(Color.z)))
            imgFile.write("\n")
    def write(self, imgFileName):

        array = []
        #adds in color
        for row in self.pixles:
            rowArray = []
            for Color in row:
                rowArray.append((self.flatten(Color.x), self.flatten(Color.y), self.flatten(Color.z)))
            array.append(rowArray)  
        array = np.array(array, dtype=np.uint8)
        new_image = Im.fromarray(array)
        new_image.save(imgFileName)



    
    


    