from math import sqrt

# a 3d object with a radius and center
class Sphere:
    # center (point), radius(num)
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material
    
    #calulates the interseciton between a ray and this sphere, returnes Distance if intersection, None if no intersection
    #https://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-sphere-intersection < -- formula stolen from here
    # cannot handle ray starting inside sphere
    def intersection(self, ray):
        sphereToRay = ray.origin - self.center
        b = 2 * ray.direction.dotProduct(sphereToRay)
        c = sphereToRay.dotProduct(sphereToRay) - self.radius * self.radius
        discriminant = b * b - 4 * c

        if discriminant >=0:
            # simplidfied quadratic formula
            dist = (- b - sqrt(discriminant)) / 2
            if dist > 0:
                return dist
        return None
