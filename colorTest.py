import unittest
from color import Color
class ColorTest(unittest.TestCase):
    def setUp(self):
        self.C1 = Color(155,2,40)
        self.C2 = Color.fromHex("#FF0000")
        self.C3 = Color.fromHex("#00FF00")
        self.C4 = Color.fromHex("#0000FF")
    def test_fromHex(self):
        self.assertEqual(155, self.C1.x)

        self.assertEqual(255,self.C2.x)
        self.assertEqual(0,self.C2.y)
        self.assertEqual(0,self.C2.z)

        self.assertEqual(255,self.C3.y)

        self.assertEqual(255,self.C4.z)

if __name__=="__main__":
    unittest.main()