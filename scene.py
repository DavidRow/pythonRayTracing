
# contains all info for the ray tracing engein
class Scene:
    
    def __init__(self, camera, objects, lights, width, height, fov, xrotation, yrotation, zrotation):
        self.camera = camera 
        self.objects = objects
        self.width = width
        self.height = height
        self.lights = lights
        self.fov = fov
        self.xrotation = xrotation
        self.yrotation = yrotation
        self.zrotation = zrotation