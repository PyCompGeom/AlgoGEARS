from algogears.core import Point
from algogears.kd_tree import KDTreeNode, KDTree, kd_tree


def test_kd_tree():
    pts = [
        Point.new(0, 9),
        Point.new(2, 3),
        Point.new(3, 6),
        Point.new(5, 8),
        Point.new(6, 1),
        Point.new(8, 13),
        Point.new(10, 2),
        Point.new(12, 4),
        Point.new(14, 11),
        Point.new(15, 5),
        Point.new(17, 10)
    ]
    rx = [3, 14]
    ry = [0, 8]

    ordered_x = pts
    ordered_y = [
        Point.new(6, 1),
        Point.new(10, 2),
        Point.new(2, 3),
        Point.new(12, 4),
        Point.new(15, 5),
        Point.new(3, 6),
        Point.new(5, 8),
        Point.new(0, 9),
        Point.new(17, 10),
        Point.new(14, 11),
        Point.new(8, 13)
    ]

    tree = KDTree(root=KDTreeNode(data=Point.new(8, 13)), x_range=rx, y_range=ry)
    tree.root.left = KDTreeNode(data=Point.new(3, 6))
    tree.root.left.left = KDTreeNode(data=Point.new(6, 1))
    tree.root.left.left.left = KDTreeNode(data=Point.new(2, 3))
    tree.root.left.right = KDTreeNode(data=Point.new(5, 8))
    tree.root.left.right.left = KDTreeNode(data=Point.new(0, 9))

    tree.root.right = KDTreeNode(data=Point.new(15, 5))
    tree.root.right.left = KDTreeNode(data=Point.new(12, 4))
    tree.root.right.left.left = KDTreeNode(data=Point.new(10, 2))
    tree.root.right.right = KDTreeNode(data=Point.new(17, 10))
    tree.root.right.right.left = KDTreeNode(data=Point.new(14, 11))

    partition = [
        (Point.new(8, 13), True),
        (Point.new(3, 6), False),
        (Point.new(6, 1), True),
        (Point.new(2, 3), False),
        (Point.new(5, 8), True),
        (Point.new(0, 9), False),
        (Point.new(15, 5), False),
        (Point.new(12, 4), True),
        (Point.new(10, 2), False),
        (Point.new(17, 10), True),
        (Point.new(14, 11), False)
    ]

    search_list = [
        (Point.new(8, 13), False, True),
        (Point.new(3, 6), True, True),
        (Point.new(6, 1), True, True),
        (Point.new(2, 3), False, True),
        (Point.new(5, 8), True, True),
        (Point.new(0, 9), False, False),
        (Point.new(15, 5), False, True),
        (Point.new(12, 4), True, True),
        (Point.new(10, 2), True, True),
        (Point.new(17, 10), False, False),
        (Point.new(14, 11), False, False)
    ]

    result = [
        Point.new(3, 6),
        Point.new(5, 8),
        Point.new(6, 1),
        Point.new(10, 2),
        Point.new(12, 4),
    ]

    ans = kd_tree(pts, rx, ry)
    assert next(ans) == (ordered_x, ordered_y)
    assert next(ans) == partition
    assert next(ans) == tree
    assert next(ans) == search_list
    assert sorted(next(ans)) == result
