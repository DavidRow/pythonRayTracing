
from image import Image
from ray import Ray
from point import Point
from ray import Ray
from color import Color 
import math
#rendors all the objects
class RenderEngine():
    MaxReflections = 5
    MinDisplacement  = 0.0000001
    specularK = 500
    # the xmax should be 1, xmin should be -1
    # same for y
    def render(self, scene):
        width = scene.width
        height = scene.height
        fov = scene.fov
        fovInRad = math.radians(fov)
        aspectRatio = float(width) / height
        #https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-generating-camera-rays/generating-camera-rays
        camera = scene.camera
        pixels = Image(width, height)
        for j in range(height):
            PixelNDCY = (j + .5 )/ height 
            Y = (1 - 2 * PixelNDCY) * math.tan(fovInRad/2)
            for i in range(width):
                PixelNDCYX = (i + .5 )/ width
                X = ((2 * PixelNDCYX - 1) * aspectRatio) * math.tan(fovInRad/2)

                ray = Ray(camera, Point(X,Y, -1 ) - camera )
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
        camera = scene.camera 
        #ColorfromHex(hex = "#00000"):
        #material.colorAt(hitPosition)
        color = material.ambient * material.colorAt(hitPosition)
        
        for light in scene.lights:
            #posiion and direction of the light ray created by the light source 
            lightRay = Ray(hitPosition, light.position - hitPosition)
            Lightdirection = lightRay.direction
            #switch this to false to change it to a less expensive diffuse shading
            if(False):
                addedColor = self.ExpensiveDiffuseShading(objectColor, material, normal, Lightdirection,hitPosition, light, new_ray_origin, scene)
                if(addedColor is not None):
                    color += addedColor
                else:
                    color = color
            else: 
                color += objectColor * material.diffuse * max(normal.dotProduct(lightRay.direction), 0)
            
            color += self.specularShading(lightRay,camera, light, material,normal)
            #light.color * material.specular * max(normal.dotProduct(halfVector), 0) ** specularK
        return color

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
    def specularShading(self, lightRay,camera, light, material,normal):
        halfVector = (lightRay.direction + camera).normalize()
        return light.color * material.specular * max(normal.dotProduct(halfVector), 0) ** self.specularK 

    # Diffuse shading (Lambert) 
    # the farther away the norm of the object is to the light direction of the light source, the dimmer it is 
    #formula Color = L * N(M)(C)
    # L = pointing from the surface to the light
    # N = and a normalized light-direction vector
    # M = Material's diffusion constant 
    # C = color of object 
    def ExpensiveDiffuseShading(self, objectColor, material, normal, Lightdirection,hitPosition, light, new_ray_origin, scene):
        direction = light.position - hitPosition
        ObjectToLight = Ray(new_ray_origin, direction)
        dist_hit, hitObject = self.findNearist(ObjectToLight, scene)
        if(hitObject is None or dist_hit >= direction.magnitude()):
            return objectColor * material.diffuse * max(normal.dotProduct(Lightdirection), 0)
        else:
            return Color(0,0,0)
            

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

