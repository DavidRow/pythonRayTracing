#!/usr/bin/env python
from image import Image
from color import Color
from vector import Vector
from point import Point
from scene import Scene
from sphere import Sphere
from scene import Scene
from renderEngine import RenderEngine

def main():
    WIDTH  = 320
    HEIGHT = 200
    camera = Vector (0,0,-1)
    objects = [Sphere(Point(0,0,0) , 0.5, Color.fromHex("#FF0000"))]
    scene = Scene(camera, objects, WIDTH, HEIGHT)
    engine = RenderEngine()
    image = engine.render(scene)
    with open("test.ppm", "w") as img_file:
        image.writePPM(img_file)

    """WIDTH  = 3
    HEIGHT = 2
    im = Image(WIDTH, HEIGHT)
    red = Color(x = 255,y = 0,z = 0)
    green = Color(x = 0,y = 255,z = 0)
    blue = Color(x = 0,y = 0,z = 255)
    im.setPixle(0,0, red)
    im.setPixle(1,0, green)
    im.setPixle(2,0, blue)
    im.setPixle(0,1, red + blue)
    im.setPixle(1,1, red + blue + green)
    im.setPixle(2,1, red )
"""

if __name__ == '__main__':
    main()