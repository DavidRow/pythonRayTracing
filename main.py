#!/usr/bin/env python
from image import Image
from color import Color
from vector import Vector
from point import Point
from scene import Scene
from sphere import Sphere
from scene import Scene
from renderEngine import RenderEngine
from light import Light
from material import Material 
from material import Chequered
import json
def main():

    file = open("twoBalls.json")
    settings = json.loads(file.read()) 
    args = settings["FileName"]
    WIDTH  = settings["WIDTH"]
    HEIGHT = settings["HEIGHT"]
    fov = settings["fov"]
    
    camera = Vector (settings["Camera"]["x"],settings["Camera"]["y"],settings["Camera"]["z"])
    objects = []
    lights  = []

    for obj in settings["objects"]:
        # this kinda sucks but it works
        x = settings["objects"][obj]["x"]
        y = settings["objects"][obj]["y"]
        z = settings["objects"][obj]["z"]
        diamiter = settings["objects"][obj]["diamiter"] 
        if(settings["objects"][obj]["Material Type"] == "Normal" ):
            color = settings["objects"][obj]["color"] 
            objects.append(Sphere(Point(x, y, z), diamiter,Material(Color.fromHex(color), ambient = 0.2) ))
        elif(settings["objects"][obj]["Material Type"] == "Chequered"):
            colorEven = color = settings["objects"][obj]["colorEven"]
            colorOdd = color = settings["objects"][obj]["colorOdd"]
            objects.append(Sphere(Point(x, y, z), diamiter,Chequered(Color.fromHex(colorEven), Color.fromHex(colorOdd))))
        


    for light in settings["lights"]:
        x = settings["lights"][light]["x"]
        y = settings["lights"][light]["y"]
        z = settings["lights"][light]["z"]
        color = settings["lights"][light]["color"] 
        lights.append(Light(Point(x, y, z), Color.fromHex(color)))    
    scene = Scene(camera, objects, lights, WIDTH, HEIGHT, fov)
    engine = RenderEngine()
    image = engine.render(scene)
    with open(args, "w") as img_file:
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