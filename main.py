#!/usr/bin/env python
from image import Image
from color import Color

def main():
    WIDTH  = 3
    HEIGHT = 2
    im = Image(WIDTH, HEIGHT)
    red = Color(x = 1,y = 0,z = 0)
    green = Color(x = 0,y = 1,z = 0)
    blue = Color(x = 0,y = 0,z = 1)
    im.setPixle(0,0, red)
    im.setPixle(1,0, green)
    im.setPixle(2,0, blue)
    im.setPixle(0,1, red + blue)
    im.setPixle(1,1, red + blue + green)
    im.setPixle(2,1, red )
    with open("test.ppm", "w") as img_file:
        im.writePPM(img_file)

if __name__ == '__main__':
    main()