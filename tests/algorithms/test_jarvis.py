from algogears.core import Point
from algogears.jarvis import jarvis


def test_jarvis1():
    pts = [
        Point.new(1, 4),
        Point.new(0, 0),
        Point.new(3, 3),
        Point.new(3, 1),
        Point.new(7, 0),
        Point.new(5, 5),
        Point.new(5, 2),
        Point.new(9, 6),
    ]
    hull = [Point.new(0, 0), Point.new(1, 4), Point.new(9, 6), Point.new(7, 0)]

    ans = jarvis(pts)
    assert ans == hull


def test_jarvis2():
    pts = [Point.new(3, 3), Point.new(1, 1), Point.new(5, 0)]
    hull = [Point.new(1, 1), Point.new(3, 3), Point.new(5, 0)]

    ans = jarvis(pts)
    assert ans == hull
