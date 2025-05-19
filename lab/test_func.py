import unittest
from triangle_func import get_triangle_type, IncorrectTriangleSides

class TestTriangleFunc(unittest.TestCase):
    def test_equilateral(self):
        self.assertEqual(get_triangle_type(5, 5, 5), "equilateral")
    
    def test_isosceles(self):
        self.assertEqual(get_triangle_type(5, 5, 8), "isosceles")
        self.assertEqual(get_triangle_type(5, 8, 5), "isosceles")
        self.assertEqual(get_triangle_type(8, 5, 5), "isosceles")
    
    def test_nonequilateral(self):
        self.assertEqual(get_triangle_type(3, 4, 5), "nonequilateral")
    
    def test_invalid_triangle(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(0, 0, 0)
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(-1, 2, 3)
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(1, 1, 3)
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(2, 3, 5)

if __name__ == "__main__":
    unittest.main()