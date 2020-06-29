

#line with a starting point and normilized diration
class Ray:
    def __init__(self, origin, direction ):
        self.origin = origin
        self.direction = direction.normalize()

        
        