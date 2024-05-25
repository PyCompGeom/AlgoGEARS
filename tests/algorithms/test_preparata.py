from algogears.core import Point, PathDirection
from algogears.preparata import preparata, PreparataThreadedBinTree


def test_preparata1():
    points = [Point.new(3, 2), Point.new(2, 4), Point.new(1, 1), Point.new(6, 2)]
    hull0 = [Point.new(1, 1), Point.new(2, 4), Point.new(3, 2)]
    hull = [Point.new(1, 1), Point.new(2, 4), Point.new(6, 2)]
    tree0 = PreparataThreadedBinTree.from_iterable(hull0)
    left_paths = [[PathDirection.right, PathDirection.right]]
    right_paths = [[]]
    left_supporting_points = [Point.new(1, 1)]
    right_supporting_points = [Point.new(2, 4)]
    deleted_points = [[Point.new(3, 2)]]
    hulls = [hull]
    trees = []
    
    ans = preparata(points)
    assert next(ans) == (hull0, tree0)
    assert next(ans) == ((left_paths, left_supporting_points), (right_paths, right_supporting_points))

    assert next(ans) == deleted_points
    assert next(ans) == (hulls, trees)
    assert next(ans) == hull


def test_preparata2():
    # Corner case for convex (>--X) where one of the angles is equal to pi
    points = [Point.new(2, 2), Point.new(0, 1), Point.new(4, 3), Point.new(1, 0)]
    hull0 = [Point.new(0, 1), Point.new(2, 2), Point.new(1, 0)]
    hull = [Point.new(0, 1), Point.new(4, 3), Point.new(1, 0)]
    tree0 = PreparataThreadedBinTree.from_iterable(hull0)
    left_paths = [[PathDirection.right]]
    right_paths = [[PathDirection.left]]
    left_supporting_points = [Point.new(1, 0)]
    right_supporting_points = [Point.new(0, 1)]
    deleted_points = [[Point.new(2, 2)]]
    hulls = [hull]
    trees = []

    ans = preparata(points)
    assert next(ans) == (hull0, tree0)
    assert next(ans) == ((left_paths, left_supporting_points), (right_paths, right_supporting_points))
    assert next(ans) == deleted_points
    assert next(ans) == (hulls, trees)
    assert next(ans) == hull


def test_preparata3():
    # Corner case for convex (>--X) where one of the angles is equal to pi
    points = [Point.new(1, 2), Point.new(0, 0), Point.new(3, 0), Point.new(5, 0)]
    hull0 = [Point.new(0, 0), Point.new(1, 2), Point.new(3, 0)]
    hull = [Point.new(0, 0), Point.new(1, 2), Point.new(5, 0)]
    tree0 = PreparataThreadedBinTree.from_iterable(hull0)
    left_paths = [[PathDirection.right, PathDirection.right]]
    right_paths = [[]]
    left_supporting_points = [Point.new(0, 0)]
    right_supporting_points = [Point.new(1, 2)]
    deleted_points = [[Point.new(3, 0)]]
    hulls = [hull]
    trees = []

    ans = preparata(points)
    assert next(ans) == (hull0, tree0)
    assert next(ans) == ((left_paths, left_supporting_points), (right_paths, right_supporting_points))
    assert next(ans) == deleted_points
    assert next(ans) == (hulls, trees)
    assert next(ans) == hull


def test_preparata4():
    # Corner cases for collinear first points and left and right supporting where one of the angles is 0
    points = [Point.new(1, 1), Point.new(1, 5), Point.new(5, 3), Point.new(1, 11), Point.new(6, 1), Point.new(10, 1)]
    hull0 = [Point.new(1, 1), Point.new(1, 5), Point.new(5, 3)]
    hull = [Point.new(1, 1), Point.new(1, 11), Point.new(10, 1)]
    tree0 = PreparataThreadedBinTree.from_iterable(hull0)
    left_paths = [
        [PathDirection.right],
        [PathDirection.right, PathDirection.right],
        [PathDirection.right, PathDirection.right]
    ]
    right_paths = [
        [PathDirection.left],
        [],
        []
    ]
    left_supporting_points = [
        Point.new(5, 3),
        Point.new(1, 1),
        Point.new(1, 1)
    ]
    right_supporting_points = [
        Point.new(1, 1),
        Point.new(1, 11),
        Point.new(1, 11)
    ]
    deleted_points = [[Point.new(1, 5)], [Point.new(5, 3)], [Point.new(6, 1)]]
    hulls = [
        [Point.new(1, 1), Point.new(1, 11), Point.new(5, 3)],
        [Point.new(1, 1), Point.new(1, 11), Point.new(6, 1)],
        hull
    ]
    trees = [PreparataThreadedBinTree.from_iterable(hulls[0]), PreparataThreadedBinTree.from_iterable(hulls[1])]

    ans = preparata(points)
    assert next(ans) == (hull0, tree0)
    assert next(ans) == ((left_paths, left_supporting_points), (right_paths, right_supporting_points))
    assert next(ans) == deleted_points
    assert next(ans) == (hulls, trees)
    assert next(ans) == hull


def test_preparata5():
    p1 = Point.new(7, 0)
    p2 = Point.new(3, 3)
    p3 = Point.new(0, 0)
    p4 = Point.new(10, 8)
    p5 = Point.new(7, 9)
    points = [p1, p2, p3, p4, p5]
    hull0 = [p3, p2, p1]
    hull = [p3, p5, p4, p1]
    tree0 = PreparataThreadedBinTree.from_iterable(hull0)
    left_paths = [
        [PathDirection.right],
        [PathDirection.right]
    ]
    right_paths = [
        [PathDirection.left],
        []
    ]
    left_supporting_points = [p1, p1]
    right_supporting_points = [p3, p5]
    deleted_points = [[p2], []]
    hulls = [
        [p3, p5, p1],
        hull
    ]
    trees = [PreparataThreadedBinTree.from_iterable(hulls[0])]

    ans = preparata(points)
    assert next(ans) == (hull0, tree0)
    assert next(ans) == ((left_paths, left_supporting_points), (right_paths, right_supporting_points))
    assert next(ans) == deleted_points
    assert next(ans) == (hulls, trees)
    assert next(ans) == hull