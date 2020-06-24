
# contains all info for the ray tracing engein
class Scene:
    
    def __init__(self, camera, objects, lights, width, height, fov):
        self.camera = camera 
        self.objects = objects
        self.width = width
        self.height = height
        self.lights = lights
        self.fov = fov
