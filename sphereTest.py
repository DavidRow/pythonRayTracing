import unittest
from sphere import Sphere
from point import Point
from ray import Ray
from vector import Vector

class SphereTest(unittest.TestCase): 
    def setUp(self):
        p1 = Point(0,0,0)
        p2 = Point(-5,0,0)
        p3 = Point(-5,1,0)
        p4 = Point(-5,2,0)
        p5 = Point(0,-5,0)
        p6 = Point(-1,0,0)
        direction1 = Vector (1,0,0)
        direction2 = Vector (0,1,0)
        self.S1 = Sphere(p1, 1 , 0)
        self.R1 = Ray(p2, direction1)
        self.R2 = Ray(p3, direction1)
        self.R3 = Ray(p4, direction1)
        self.R4 = Ray(p5, direction2)
        self.R5 = Ray(p6, direction1)
        self.R6 = Ray(p1, direction1)



    def testIntersection(self):
        self.assertEqual(self.S1.intersection(self.R1), 4)
        self.assertEqual(self.S1.intersection(self.R2), 5)
        self.assertEqual(self.S1.intersection(self.R3), None)
        self.assertEqual(self.S1.intersection(self.R4), 4)
        self.assertEqual(self.S1.intersection(self.R1, True), 6)
        self.assertEqual(self.S1.intersection(self.R5), 0)
        self.assertEqual(self.S1.intersection(self.R5, True), 2)
        self.assertEqual(self.S1.intersection(self.R6), 1)


if __name__=="__main__":
    unittest.main()