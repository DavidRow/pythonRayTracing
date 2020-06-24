
from image import Image
from ray import Ray
from point import Point
from ray import Ray
from color import Color 
import math
#rendors all the objects
class RenderEngine():
    MaxReflections = 5
    MinDisplacement  = 0.0001
    

    # the xmax should be 1, xmin should be -1
    # same for y
    def render(self, scene):
        width = scene.width
        height = scene.height
        fov = scene.fov
        fovInRad = scene.fov * (3.14159/180)
        aspectRatio = float(width) / height
        #https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-generating-camera-rays/generating-camera-rays
        camera = scene.camera
        pixels = Image(width, height)
        for j in range(height):
            PixelNDCY = (j + .5 )/ height 
             
            PixelScreenY = (1 - 2 * PixelNDCY) 
            for i in range(width):
                PixelNDCYX = (i + .5 )/ width
                PixelScreenX = ((2 * PixelNDCYX - 1) * aspectRatio) * abs(math.tan(fovInRad/2))

                ray = Ray(camera, Point(PixelScreenX,PixelScreenY, 1) - camera )
                pixels.setPixle(i,j, self.rayTrace(ray, scene)) 
        return pixels
        
    # move rays
    def rayTrace(self, ray, scene, numberOfReflections = 0):
        color = Color(0, 0, 0)
        #find nearist object hit by ray
        dist_hit, hitObject = self.findNearist(ray, scene)
        if(hitObject is None):
            return color
        hitPosition = ray.origin + ray.direction * dist_hit
        hitNormal = hitObject.normal(hitPosition)
        color += self.ColorAt(hitObject, hitPosition,hitNormal ,scene) 

        #find reflections
        #https://www.scratchapixel.com/lessons/3d-basic-rendering/introduction-to-shading/reflection-refraction-fresnel
        if(numberOfReflections < self.MaxReflections):
            MIN_DISPLACE = 100
            new_ray_origin = hitPosition + (hitNormal *  self.MinDisplacement)
            #ray direction = Incoming ray - 2(Normal dot incoming) * normal
            new_ray_direction = ray.direction - 2 * (hitNormal.dotProduct(ray.direction)) * hitNormal
            reflectedRay = Ray(new_ray_origin, new_ray_direction)
            color += self.rayTrace(reflectedRay, scene, numberOfReflections + 1) * hitObject.material.reflection
        return color


    #find nearist object    
    def findNearist(self, ray, scene):
        final_distance = None
        minimum = None
        hitObject = None
        distance = None
        #print(len(scene.objects))
        for obj in scene.objects:
            distance = obj.intersection(ray) 
            if (distance is not None and (hitObject is None or distance < minimum)):
                #print(str(obj.radius) + "---------------------")
                #print(distance)
                minimum = distance
                hitObject = obj
        return (minimum, hitObject)

    #find color of the object for every pixel
    def ColorAt(self, hitObject, hitPosition, normal,scene):

        material = hitObject.material
        objectColor = material.colorAt(hitPosition)
        camera = scene.camera - hitPosition
        color = material.ambient * Color.fromHex("#F00000")
        specularK = 500
        for light in scene.lights:
            #posiion and direction of the light ray created by the light source 
            lightRay = Ray(hitPosition, light.position - hitPosition)

            # Diffuse shading (Lambert) 
            # the farther away the norm of the object is to the light direction of the light source, the dimmer it is 
            #formula Color = L * N(M)(C)
            # L = pointing from the surface to the light
            # N = and a normalized light-direction vector
            # M = Material's diffusion constant 
            # C = color of object 
            color += (
                objectColor * material.diffuse * max(normal.dotProduct(lightRay.direction), 0)
            )

            # Specular shading (Blinn–Phong reflection model) 
            # halfVector = the angle halfway between the light source and the reflextion ray 
            # = (V * R)^k 
            # K = constant on how shinine something is
            # V = viewer's ray 
            # R = lights perfectly reflected ray
            # we can replace V with H, the halfway vector between the viewer and the light
            # H = L = light source ray + V = viewer's ray
            #https://en.wikipedia.org/wiki/Blinn%E2%80%93Phong_reflection_model - for more info
            halfVector = (lightRay.direction + camera).normalize()
            color += light.color * material.specular * max(normal.dotProduct(halfVector), 0) ** specularK
        #print(color)
        return color

