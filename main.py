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
import time
def main():
    start_time = time.time()
    #open file and red configuration from it
    file = open("configurations/twoBalls.json") 
    settings = json.loads(file.read()) 
    args = "Images/" + str(settings["FileName"])
    WIDTH  = settings["WIDTH"]
    HEIGHT = settings["HEIGHT"]
    # fov will cause distortion
    if "fov" in settings:
        fov = settings["fov"]
    else:
        fov = 90
    #https://www.tutorialspoint.com/computer_graphics/3d_transformation.htm
    # rotation around the x axis
    if "xrotation" in settings:
        xrotation = settings["xrotation"]
    else:
        xrotation = 0
    # rotation around the y axis
    if "yrotation" in settings:
        yrotation = settings["yrotation"]
    else:
        yrotation = 0
    # rotation around the z axis
    if "zrotation" in settings:
        zrotation = settings["zrotation"]
    else:
        zrotation = 0

    
    
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
        reflection = 0.05
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
            objects.append(Sphere(Point(x, y, z), diamiter,Chequered(Color.fromHex(colorEven), Color.fromHex(colorOdd)
            , ambient = ambient
            , diffuse = diffuse
            , specular = specular
            , reflection = reflection)))
            
        
    for light in settings["lights"]:
        x = settings["lights"][light]["x"]
        y = settings["lights"][light]["y"]
        z = settings["lights"][light]["z"]
        color = settings["lights"][light]["color"] 
        lights.append(Light(Point(x, y, z), Color.fromHex(color))) 
        
    scene = Scene(camera, objects, lights, WIDTH, HEIGHT, fov, xrotation, yrotation, zrotation)
    engine = RenderEngine()
    image = engine.render(scene)

    with open(args, "wb") as img_file:
        image.write(img_file)
    print("it Took %s seconds to run" %(time.time() - start_time))


if __name__ == '__main__':
    main()