import pytest
from triangle_class import Triangle, IncorrectTriangleSides

def test_valid_triangle_creation():
    triangle = Triangle(3, 4, 5)
    assert triangle.a == 3
    assert triangle.b == 4
    assert triangle.c == 5

def test_invalid_triangle_creation():
    with pytest.raises(IncorrectTriangleSides):
        Triangle(0, 0, 0)
    with pytest.raises(IncorrectTriangleSides):
        Triangle(-1, 2, 3)
    with pytest.raises(IncorrectTriangleSides):
        Triangle(1, 1, 3)

def test_triangle_type():
    assert Triangle(5, 5, 5).triangle_type() == "equilateral"
    assert Triangle(5, 5, 8).triangle_type() == "isosceles"
    assert Triangle(3, 4, 5).triangle_type() == "nonequilateral"

def test_perimeter():
    assert Triangle(3, 4, 5).perimeter() == 12
    assert Triangle(5, 5, 5).perimeter() == 15
    assert Triangle(5, 5, 8).perimeter() == 18