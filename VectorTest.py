import unittest
from vector import Vector
class TestVectors(unittest.TestCase):
    def setUp(self):
        self.v1 = Vector(-1, 2, -2)
        self.v2 = Vector(1, 1, 1) 
        self.v3 = Vector(-1, 2, -2)
        self.v4 = Vector(0, 3, -1)
        self.v5 = Vector(-2, 1, -3)
        self.v6 = Vector(0, 0, 0)
        self.v7 = Vector(-2, 4, -4)
        self.v8 = Vector(4, 6, -2)
        self.v9 = Vector(2, 3, -1)
    def test_magnitude(self):
        self.assertEqual(self.v1.magnitude(), 3)
    def test_dotProduct(self):
        self.assertEqual(self.v1.dotProduct(self.v2), -1)  
    def test_equals(self):
        self.assertFalse(self.v1.equals(self.v2))
        self.assertTrue(self.v1.equals(self.v3))
    def test_add(self):
        sum = self.v1 + self.v2
        self.assertTrue(sum.equals(self.v4))
    def test_sub(self):
        subtractedVector = self.v1 - self.v2
        self.assertTrue(subtractedVector.equals(self.v5))
    def test_multiplication(self):
        self.assertTrue(self.v6.equals(self.v1 * 0))
        self.assertTrue(self.v7.equals(self.v1 * 2))
        self.assertTrue(self.v7.equals(2 * self.v1))
    def test_division(self):
        self.assertTrue(self.v9.equals(self.v8 / 2))

if __name__ == "__main__":
    unittest.main()
