
import unittest
from ray import Ray
from point import Point
from vector import Vector
from sphere import Sphere
class RayTest(unittest.TestCase):
        def setUp(self):
            p1 = Point(0,0,0)
            self.R1 = Ray(p1, Vector(0,0,1))
            self.R2 = Ray(Point(0,0,-1), Vector(0,0,1))
            self.S1 = Sphere(p1, 1 , 0)
        # just making sure that when inside the object the rays work correctly
        def testIntersection(self):
            self.assertEqual(self.S1.intersection(self.R1), 1)
            self.assertEqual(self.S1.intersection(self.R2), 0)
            self.assertEqual(self.S1.intersection(self.R2, True), 2)
        




if __name__=="__main__":
    unittest.main()

