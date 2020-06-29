
from image import Image
from ray import Ray
from point import Point
from ray import Ray
from color import Color 
import numpy as np
import math
#rendors all the objects
class RenderEngine():
    MaxReflections = 5
    MinDisplacement  = 0.0000001
    specularK = 500
    # the xmax should be 1, xmin should be -1
    # same for y
    def render(self, scene):

        # matrix transformation
        xrotationRAD = math.radians(scene.xrotation)
        yrotationRAD = math.radians(scene.yrotation)
        zrotationRAD = math.radians(scene.zrotation)
        xRotationMatrix  = np.array(
                              [[1,0,0,0],
                               [0,math.cos(xrotationRAD),-math.sin(xrotationRAD),0],
                               [0,math.sin(xrotationRAD),math.cos(xrotationRAD),0],
                               [0,0,0,1]])
        yRotationMatrix  = np.array(
                              [[math.cos(yrotationRAD),0,math.sin(yrotationRAD),0],
                               [0,1,0,0],
                               [-math.sin(yrotationRAD),0,math.cos(yrotationRAD),0],
                               [0,0,0,1]])
        zRotationMatrix  = np.array(
                              [[math.cos(zrotationRAD),-math.sin(zrotationRAD),0,0],
                               [math.sin(zrotationRAD),math.cos(zrotationRAD),0,0],
                               [0,0,1,0],
                               [0,0,0,1]])
        tranformationMatrix = xRotationMatrix.dot(yRotationMatrix).dot(zRotationMatrix)
        width = scene.width
        height = scene.height
        fovNum = math.tan(math.radians(scene.fov)/2)
        aspectRatio = float(width) / height
        #https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-generating-camera-rays/generating-camera-rays
        pixels = Image(width, height)
        for j in range(height):
            #PixelNDCY = (j + .5 )/ height 
            #Y = (1 - 2 * PixelNDCY) * fovNum
            Y = (1 - 2 * ((j + .5 )/ height)) * fovNum
            for i in range(width):
                #PixelNDCYX = (i + .5 )/ width
                #X = ((2 * PixelNDCYX - 1) * aspectRatio) * fovNum
                X = (((2 * ((i + .5 )/ width)) - 1) * aspectRatio) * fovNum
                transformedDirection = np.array([X,Y,-1,1]).dot(tranformationMatrix)
                transformedDirection = Point(transformedDirection[0], transformedDirection[1], transformedDirection[2])
                ray = Ray(scene.camera, transformedDirection)
                pixels.setPixle(i,j, self.rayTrace(ray, scene)) 
        return pixels
        
    # move rays
    def rayTrace(self, ray, scene, depth = 0):
        color = Color(0, 0, 0)
        #find nearist object hit by ray
        dist_hit, hitObject = self.findNearist(ray, scene)
        if(hitObject is None):
            return color
        hitPosition = ray.origin + ray.direction * dist_hit
        hitNormal = hitObject.normal(hitPosition)
        new_ray_origin = hitPosition + (hitNormal *  self.MinDisplacement)
        color += self.ColorAt(hitObject, hitPosition, hitNormal, new_ray_origin, scene) 
        #find reflections
        #https://www.scratchapixel.com/lessons/3d-basic-rendering/introduction-to-shading/reflection-refraction-fresnel
        if(depth < self.MaxReflections):
            new_ray_direction = ray.direction - (2 * hitNormal * (hitNormal.dotProduct(ray.direction)))
            reflectedRay = Ray(new_ray_origin, new_ray_direction)
            color += self.rayTrace(reflectedRay, scene, depth + 1) * hitObject.material.reflection
        #if(hitObject.material.refractable is True):
            #color += self.refract(hitObject, hitPosition, hitNormal,ray, scene)
        
        return color

    #find color of the object for every pixel
    def ColorAt(self, hitObject, hitPosition, normal, new_ray_origin, scene):

        material = hitObject.material
        objectColor = material.colorAt(hitPosition)
        #ColorfromHex(hex = "#00000"):
        #material.colorAt(hitPosition)
        color = material.ambient * material.colorAt(hitPosition)
        
        for light in scene.lights:
            #posiion and direction of the light ray created by the light source 
            lightRay = Ray(hitPosition, light.position - hitPosition)
            # from hit position to light
            lightDirection = (light.position - hitPosition)
            normilzedLightDirection = lightDirection.normalize()

            #switch this to false to change it to a less expensive diffuse shading
            if(True):
                ObjectToLight = Ray(new_ray_origin, lightDirection)
                dist_hit, hitObject = self.findNearist(ObjectToLight, scene)
                addedColor = self.ExpensiveDiffuseShading(normilzedLightDirection, hitObject,dist_hit, objectColor, material, normal, lightDirection , hitPosition, light, new_ray_origin, scene)
                if(addedColor is not None):
                    color += addedColor
                else:
                    color = color
            else: 
                color += objectColor * material.diffuse * max(normal.dotProduct(normilzedLightDirection), 0)
            
            color += self.specularShading(normilzedLightDirection,scene.camera, light, material,normal)

        return color
        # Diffuse shading (Lambert) 
    # the farther away the norm of the object is to the light direction of the light source, the dimmer it is 
    #formula Color = L * N(M)(C)
    # L = pointing from the surface to the light
    # N = and a normalized light-direction vector
    # M = Material's diffusion constant 
    # C = color of object 
    def ExpensiveDiffuseShading(self,normilzedLightDirection,hitObject,dist_hit,  objectColor, material, normal, Lightdirection,hitPosition, light, new_ray_origin, scene):

        if(hitObject is None or dist_hit >= Lightdirection.magnitude()):
            return objectColor * material.diffuse * max(normal.dotProduct(normilzedLightDirection), 0)
        else:
            return Color(0,0,0)
    #https://www.scratchapixel.com/lessons/3d-basic-rendering/introduction-to-shading/reflection-refraction-fresnel
    def refract(self, hitObject, hitPosition, hitNormal,ray, scene):
        pass

    # Specular shading (Blinn–Phong reflection model) 
    # halfVector = the angle halfway between the light source and the reflextion ray 
    # = (V * R)^k 
    # K = constant on how shinine something is
    # V = viewer's ray 
    # R = lights perfectly reflected ray
    # we can replace V with H, the halfway vector between the viewer and the light
    # H = L = light source ray + V = viewer's ray
    #https://en.wikipedia.org/wiki/Blinn%E2%80%93Phong_reflection_model - for more info
    def specularShading(self, normilzedLightDirection,camera, light, material,normal):
        #halfVector = (normilzedLightDirection + camera).normalize()
        return light.color * material.specular * max(normal.dotProduct((normilzedLightDirection + camera).normalize()), 0) ** self.specularK 



    #find nearist object    
    def findNearist(self, ray, scene):
        minimum = None
        hitObject = None
        distance = None
        for obj in scene.objects:
            distance = obj.intersection(ray) 
            if (distance is not None and (hitObject is None or distance < minimum)):
                minimum = distance
                hitObject = obj
        return (minimum, hitObject)

    def transformation(self, point, matrix):
        transformedPoint = Point(0,0,0)
        somePoint = np.array([point.x, point.y, point.z, 1])
        np.matmul(somePoint)
        
        transformedPoint.x = matrix[0] * point.x
        transformedPoint.y = matrix[1] * point.y
        transformedPoint.z = matrix[2] * point.z
        return transformedPoint