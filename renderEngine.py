
from image import Image
from ray import Ray
from point import Point
from ray import Ray
from color import Color 
#rendors all the objects
class RenderEngine():

    # the xmax should be 1, xmin should be -1
    # same for y
    def render(self, scene):
        width = scene.width
        height = scene.height
        aspectRatio = float(width) / height
        x0 = -1.0
        x1 = +1.0
        deltaX = (x1 - x0) / (width - 1)
        y1 = 1.0 / aspectRatio # streched/ compressed by the aspect ratio
        y0 = -1.0 / aspectRatio
        deltaY = (y1 - y0) / (height - 1)

        camera = scene.camera
        pixels = Image(width, height)

        for j in range(height):
            y = y0 + j * deltaY
            for i in range(width):
                x = x0 + i * deltaX
                ray = Ray(camera, Point(x,y) - camera)
                pixels.setPixle(i,j, self.rayTrace(ray, scene))
        return pixels
        
    # move rays
    def rayTrace(self, ray, scene):
        color = Color(1,1,1)
        #find nearist object hit by ray
        dist_hit, hitObject = self.findNearist(ray, scene)
        if(hitObject is None):
            return color
        hitPosition = ray.origin + ray.direction * dist_hit
        color += self.ColorAt(hitObject, hitPosition,scene) 
        return color


    #find nearist object    
    def findNearist(self, ray, scene):
        min = None
        hitObject = None
        for obj in scene.objects:
            distance = obj.intersection(ray) 
            if distance is not None and (hitObject is None or distance < min):
                    min = distance
                    hitObject = obj
        return (distance, hitObject)

    #find color of the object
    def ColorAt(self, hitObject, hitPosition,scene):
        return hitObject.material
