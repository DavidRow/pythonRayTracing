from math import sqrt

# a 3d object with a radius and center
class Sphere:
    # center (point), radius(num)
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material
        self.radius2 = radius ** 2
    #https://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-sphere-intersection
    def intersection(self,ray, secondValue = False):
        #vector between O (the ray's origin) and C (the sphere's center)
        OriginToCenter = ray.origin - self.center
        #rays direction
        D = ray.direction
        a = 1
        b = 2 * D.dotProduct(OriginToCenter)
        c = OriginToCenter.dotProduct(OriginToCenter) - self.radius2
        discriminant = b * b - 4 * c * a
        #the ray and the circel never intersect
        if discriminant < 0: 
            return None
        # the ray and the circel intersect at one point
        if discriminant == 0:
            distance = (-b) / 2
            if(distance < 0):
                return None
            return distance
        # the ray and the circel intersect in two places
        else:
            if(secondValue is False):
                distance = (-b - sqrt(discriminant)) / 2
                # if the distance is negative, see if the other value works
                if(distance < 0):
                   distance = (-b + sqrt(discriminant)) / 2
                   # if both distances are negative than this ray must be 
                   if(distance < 0):
                        return None
                   return distance
                return distance
            else:
                distance = (-b + sqrt(discriminant)) / 2
                if(distance < 0):
                    return None
                return distance

            
        
    #finds the normal vector at a point in the sphere
    def normal(self, point):
        return (point - self.center).normalize()
