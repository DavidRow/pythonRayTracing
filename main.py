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
    #open file and red configuration from it
    file = open("configurations/twoBalls.json")
    settings = json.loads(file.read()) 
    args = "Images/" + str(settings["FileName"])
    WIDTH  = settings["WIDTH"]
    HEIGHT = settings["HEIGHT"]
    if "ambient" in settings:
        fov = settings["fov"]
    else:
        fov = 90
    camera = Vector (settings["Camera"]["x"],settings["Camera"]["y"],settings["Camera"]["z"])
    objects = []
    lights  = []
    for obj in settings["objects"]:
        thisObject = settings["objects"][obj]
        x = thisObject["x"]
        y = thisObject["y"]
        z = thisObject["z"]
        diamiter = thisObject["diamiter"] 
        #the higher the ambient value is the ligher the object looks without any light 
        ambient    = 0.05
        #the higher diffuse value is the lighter the object looks when the normal is close to the direction of the light
        diffuse    = 1.0
        #the higher this is the shinyer the little shine looks on the sphere
        specular   = 1.0
        #the higher this is the more it reflects it's surroundings
        reflection = 0.5
        if "ambient" in thisObject:
            ambient = thisObject["ambient"]
        if "diffuse" in thisObject:
            diffuse = thisObject["diffuse"]
        if "specular" in thisObject:
            specular = thisObject["specular"]
        if "reflection" in thisObject:
            reflection = thisObject["reflection"]
        if(thisObject["Material Type"] == "Normal" ):
            color = thisObject["color"] 
            objects.append(Sphere(Point(x, y, z), 
            diamiter,Material(Color.fromHex(color)
            , ambient = ambient
            , diffuse = diffuse
            , specular = specular
            , reflection = reflection ) ))
        elif(thisObject["Material Type"] == "Chequered"):
            colorEven = color = thisObject["colorEven"]
            colorOdd = color = thisObject["colorOdd"]
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


if __name__ == '__main__':
    main()