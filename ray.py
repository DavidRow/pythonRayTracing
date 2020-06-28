

#line with a starting point and normilized diration
class Ray:
    def __init__(self, origin, direction, normalize = True):
        self.origin = origin
        if(normalize):
            self.direction = direction.normalize()
        else:
            self.direction = direction

        
        