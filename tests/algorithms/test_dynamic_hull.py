from copy import deepcopy
from algogears.core import Point
from algogears.dynamic_hull import DynamicHullNode, SubhullThreadedBinTree, DynamicHullTree, PathDirection, upper_dynamic_hull, merge


def test_dynamic_hull1():
    p2, p1, p3 = Point.new(3, 3), Point.new(1, 1), Point.new(5, 0)
    pts = [p2, p1, p3]
    root = DynamicHullNode(data=p2, subhull=[p1, p2, p3], left_supporting_index=1, left_supporting=p2, right_supporting=p3)
    root.left = DynamicHullNode(data=p1, subhull=[p1, p2], left_supporting=p1, right_supporting=p2)
    root.left.left = DynamicHullNode.leaf(p1)
    root.left.right = DynamicHullNode.leaf(p2)
    root.right = DynamicHullNode.leaf(p3)
    tree = DynamicHullTree(root=root)
    
    tree.root.optimized_subhull = tree.root.subhull
    
    leaves = [root.left.left, root.left.right, root.right]
    path = [PathDirection.right]
    point_to_insert = Point.new(4, 3)
    hull = [p1, p2, point_to_insert, p3]

    ans = upper_dynamic_hull(pts, point_to_insert)

    assert leaves == next(ans)
    assert tree == next(ans)
    assert tree == next(ans)
    assert tree == next(ans)
    assert tree == next(ans)
    assert tree == next(ans)
    assert path == next(ans)

    tree.root.subhull = hull
    tree.root.optimized_subhull = hull
    tree.root.right_supporting = point_to_insert
    tree.root.right = DynamicHullNode(data=point_to_insert, subhull=[point_to_insert, p3], left_supporting=point_to_insert, right_supporting=p3)
    tree.root.right.left = DynamicHullNode.leaf(point_to_insert)
    tree.root.right.right = DynamicHullNode.leaf(p3)

    assert (tree, hull) == next(ans)
    assert hull == next(ans)


def test_dynamic_hull2():
    pts = p5, p9, p4, p2, p6, p8, p3, p10, p7, p1, p11 = [
        Point.new(3, 10),
        Point.new(6, 8),
        Point.new(3, 5),
        Point.new(2, 8),
        Point.new(4, 8),
        Point.new(5, 5),
        Point.new(3, 3),
        Point.new(7, 7),
        Point.new(5, 0),
        Point.new(0, 0),
        Point.new(10, 3)
    ]
    root = DynamicHullNode(data=p6, subhull=[p1, p2, p5, p9, p10, p11], left_supporting_index=2, left_supporting=p5, right_supporting=p9)
    root.left = DynamicHullNode(data=p3, subhull=[p1, p2, p5, p6], left_supporting_index=1, left_supporting=p2, right_supporting=p5)
    root.left.left = DynamicHullNode(data=p2, subhull=[p1, p2, p3], left_supporting_index=1, left_supporting=p2, right_supporting=p3)
    root.left.left.left = DynamicHullNode(data=p1, subhull=[p1, p2], left_supporting=p1, right_supporting=p2)
    root.left.left.left.left = DynamicHullNode.leaf(p1)
    root.left.left.left.right = DynamicHullNode.leaf(p2)
    root.left.left.right = DynamicHullNode.leaf(p3)
    root.left.right = DynamicHullNode(data=p5, subhull=[p5, p6], left_supporting=p5, right_supporting=p6)
    root.left.right.left = DynamicHullNode(data=p4, subhull=[p5], left_supporting=p5, right_supporting=p5)
    root.left.right.left.left = DynamicHullNode.leaf(p4)
    root.left.right.left.right = DynamicHullNode.leaf(p5)
    root.left.right.right = DynamicHullNode.leaf(p6)
    root.right = DynamicHullNode(data=p9, subhull=[p8, p9, p10, p11], left_supporting_index=1, left_supporting=p9, right_supporting=p10)
    root.right.left = DynamicHullNode(data=p8, subhull=[p8, p9], left_supporting=p8, right_supporting=p9)
    root.right.left.left = DynamicHullNode(data=p7, subhull=[p8], left_supporting=p8, right_supporting=p8)
    root.right.left.left.left = DynamicHullNode.leaf(p7)
    root.right.left.left.right = DynamicHullNode.leaf(p8)
    root.right.left.right = DynamicHullNode.leaf(p9)
    root.right.right = DynamicHullNode(data=p10, subhull=[p10, p11], left_supporting=p10, right_supporting=p11)
    root.right.right.left = DynamicHullNode.leaf(p10)
    root.right.right.right = DynamicHullNode.leaf(p11)
    tree = DynamicHullTree(root=root)

    tree.root.optimized_subhull = tree.root.subhull
    tree.root.left.optimized_subhull = [p6]
    tree.root.left.left.optimized_subhull = [p3]
    tree.root.left.right.left.left.optimized_subhull = [p4]
    tree.root.right.optimized_subhull = [p8]
    tree.root.right.left.left.left.optimized_subhull = [p7]

    leaves = tree.leaves_inorder()
    path = [PathDirection.left, PathDirection.right, PathDirection.left, PathDirection.right]
    point_to_delete = p5
    hull = [p1, p2, p9, p10, p11]

    ans = upper_dynamic_hull(pts, point_to_delete)

    assert leaves == next(ans)
    assert tree == next(ans)
    assert tree == next(ans)
    assert tree == next(ans)
    assert tree == next(ans)
    assert tree == next(ans)
    assert path == next(ans)

    tree.root.subhull = [p1, p2, p9, p10, p11]
    tree.root.optimized_subhull = tree.root.subhull
    tree.root.left_supporting_index = 1
    tree.root.left_supporting = p2
    tree.root.right_supporting = p9
    
    tree.root.left.subhull = [p1, p2, p6]
    tree.root.left.right_supporting = p6

    tree.root.left.right.left.right = tree.root.left.right.right
    tree.root.left.right = tree.root.left.right.left
    tree.root.left.right.subhull = [p4, p6]
    tree.root.left.right.optimized_subhull = [p4]
    tree.root.left.right.left_supporting = p4
    tree.root.left.right.right_supporting = p6

    tree.root.left.right.left.optimized_subhull = []

    assert (tree, hull) == next(ans)
    assert hull == next(ans)


def test_dynamic_hull3():
    """Vertical line, only upper point"""
    pts = p1, p2, p3, p4, p5 = [Point.new(0, i) for i in range(5)]
    root = DynamicHullNode(data=p3, subhull=[p5], left_supporting=p5, right_supporting=p5)
    root.left = DynamicHullNode(data=p2, subhull=[p3], left_supporting=p3, right_supporting=p3)
    root.left.left = DynamicHullNode(data=p1, subhull=[p2], left_supporting=p2, right_supporting=p2)
    root.left.left.left = DynamicHullNode.leaf(p1)
    root.left.left.right = DynamicHullNode.leaf(p2)
    root.left.right = DynamicHullNode.leaf(p3)
    root.right = DynamicHullNode(data=p4, subhull=[p5], left_supporting=p5, right_supporting=p5)
    root.right.left = DynamicHullNode.leaf(p4)
    root.right.right = DynamicHullNode.leaf(p5)
    tree = DynamicHullTree(root=root)

    tree.root.optimized_subhull = tree.root.subhull
    tree.root.left.optimized_subhull = tree.root.left.subhull
    tree.root.left.left.optimized_subhull = tree.root.left.left.subhull
    tree.root.left.left.left.optimized_subhull = tree.root.left.left.left.subhull
    tree.root.right.left.optimized_subhull = tree.root.right.left.subhull

    leaves = tree.leaves_inorder()
    path = [PathDirection.right] * 2
    point_to_insert = Point.new(0, 6)
    hull = [point_to_insert]

    ans = upper_dynamic_hull(pts, point_to_insert)

    assert leaves == next(ans)
    assert tree == next(ans)
    assert tree == next(ans)
    assert tree == next(ans)
    assert tree == next(ans)
    assert tree == next(ans)
    assert path == next(ans)

    tree.root.subhull = [point_to_insert]
    tree.root.optimized_subhull = tree.root.subhull
    tree.root.left_supporting = point_to_insert
    tree.root.right_supporting = point_to_insert

    tree.root.right.subhull = [point_to_insert]
    tree.root.right.left_supporting = point_to_insert
    tree.root.right.right_supporting = point_to_insert

    tree.root.right.right = DynamicHullNode(data=p5, subhull=[point_to_insert], left_supporting=point_to_insert, right_supporting=point_to_insert)
    tree.root.right.right.left = DynamicHullNode.leaf(p5)
    tree.root.right.right.left.optimized_subhull = [p5]
    
    tree.root.right.right.right = DynamicHullNode.leaf(point_to_insert)
    
    assert (tree, hull) == next(ans)
    assert hull == next(ans)


def test_dynamic_hull4():
    """Horizontal line, segment of only extreme left and right points"""
    pts = p1, p2, p3, p4, p5 = [Point.new(i, 0) for i in range(1, 6)]
    root = DynamicHullNode(data=p3, subhull=[p1, p5], left_supporting=p1, right_supporting=p5)
    root.left = DynamicHullNode(data=p2, subhull=[p1, p3], left_supporting=p1, right_supporting=p3)
    root.left.left = DynamicHullNode(data=p1, subhull=[p1, p2], left_supporting=p1, right_supporting=p2)
    root.left.left.left = DynamicHullNode.leaf(p1)
    root.left.left.right = DynamicHullNode.leaf(p2)
    root.left.right = DynamicHullNode.leaf(p3)
    root.right = DynamicHullNode(data=p4, subhull=[p4, p5], left_supporting=p4, right_supporting=p5)
    root.right.left = DynamicHullNode.leaf(p4)
    root.right.right = DynamicHullNode.leaf(p5)
    tree = DynamicHullTree(root=root)

    tree.root.optimized_subhull = tree.root.subhull
    tree.root.left.optimized_subhull = [p3]
    tree.root.left.left.optimized_subhull = [p2]
    tree.root.right.optimized_subhull = [p4]

    leaves = tree.leaves_inorder()
    path = [PathDirection.left] * 3
    point_to_insert = Point.new(0, 0)
    hull = [point_to_insert, p5]

    ans = upper_dynamic_hull(pts, point_to_insert)

    assert leaves == next(ans)
    assert tree == next(ans)
    assert tree == next(ans)
    assert tree == next(ans)
    assert tree == next(ans)
    assert tree == next(ans)
    assert path == next(ans)

    tree.root.subhull = hull
    tree.root.optimized_subhull = tree.root.subhull
    tree.root.left_supporting = point_to_insert

    tree.root.left = DynamicHullNode(data=p1, subhull=[point_to_insert, p3], optimized_subhull=[p3], left_supporting=point_to_insert, right_supporting=p3)
    tree.root.left.left = DynamicHullNode(data=point_to_insert, subhull=[point_to_insert, p1], optimized_subhull=[p1], left_supporting=point_to_insert, right_supporting=p1)
    tree.root.left.left.left = DynamicHullNode.leaf(point_to_insert)
    tree.root.left.left.right = DynamicHullNode.leaf(p1)
    tree.root.left.right = DynamicHullNode(data=p2, subhull=[p2, p3], optimized_subhull=[p2], left_supporting=p2, right_supporting=p3)
    tree.root.left.right.left = DynamicHullNode.leaf(p2)
    tree.root.left.right.right = DynamicHullNode.leaf(p3)

    assert (tree, hull) == next(ans)
    assert hull == next(ans)


def make_two_segment_nodes(points):
    p1, p2, p3, p4 = points
    n1, n2, n3, n4 = [DynamicHullNode.leaf(p) for p in points]

    segment_node1 = DynamicHullNode(data=p1, subhull=[p1, p2], left_supporting=p1, right_supporting=p2)
    segment_node1.left, segment_node1.right = n1, n2
    segment_node2 = DynamicHullNode(data=p3, subhull=[p3, p4], left_supporting=p3, right_supporting=p4)
    segment_node2.left, segment_node2.right = n3, n4
    
    return segment_node1, segment_node2


def test_merge_segments1():
    """Hull is p1-p4"""
    pts = [Point.new(0, 2), Point.new(1, 0), Point.new(3, 1), Point.new(4, 3)]
    p1, p2, p3, p4 = pts

    segment_node1, segment_node2 = make_two_segment_nodes(pts)
    joint_node = DynamicHullNode(data=p2, subhull=[p1, p4], left_supporting=p1, right_supporting=p4)
    joint_node.left, joint_node.right = segment_node1, segment_node2

    assert joint_node == merge(segment_node1, segment_node2)


def test_merge_segments2():
    """Hull is p1-p2-p4, p3 is below p1-p4"""
    pts = [Point.new(1, 1), Point.new(2, 4), Point.new(3, 1), Point.new(4, 2)]
    p1, p2, p3, p4 = pts

    segment_node1, segment_node2 = make_two_segment_nodes(pts)
    joint_node = DynamicHullNode(data=p2, subhull=[p1, p2, p4], left_supporting_index=1, left_supporting=p2, right_supporting=p4)
    joint_node.left, joint_node.right = segment_node1, segment_node2

    assert joint_node == merge(segment_node1, segment_node2)


def test_merge_segments3():
    """Hull is p1-p2-p4, p3 is above p1-p4"""
    pts = [Point.new(1, 1), Point.new(2, 4), Point.new(3, 2), Point.new(4, 2)]
    p1, p2, p3, p4 = pts

    segment_node1, segment_node2 = make_two_segment_nodes(pts)
    joint_node = DynamicHullNode(data=p2, subhull=[p1, p2, p4], left_supporting_index=1, left_supporting=p2, right_supporting=p4)
    joint_node.left, joint_node.right = segment_node1, segment_node2

    assert joint_node == merge(segment_node1, segment_node2)


def test_merge_segments4():
    """Hull is p1-p3-p4, p2 is below p1-p4"""
    pts = [Point.new(1, 3), Point.new(2, 1), Point.new(3, 3), Point.new(4, 1)]
    p1, p2, p3, p4 = pts

    segment_node1, segment_node2 = make_two_segment_nodes(pts)
    joint_node = DynamicHullNode(data=p2, subhull=[p1, p3, p4], left_supporting=p1, right_supporting=p3)
    joint_node.left, joint_node.right = segment_node1, segment_node2

    assert joint_node == merge(segment_node1, segment_node2)


def test_merge_segments5():
    """Hull is p1-p3-p4, p2 is above p1-p4"""
    pts = [Point.new(1, 3), Point.new(2, 3), Point.new(3, 4), Point.new(4, 1)]
    p1, p2, p3, p4 = pts

    segment_node1, segment_node2 = make_two_segment_nodes(pts)
    joint_node = DynamicHullNode(data=p2, subhull=[p1, p3, p4], left_supporting=p1, right_supporting=p3)
    joint_node.left, joint_node.right = segment_node1, segment_node2

    assert joint_node == merge(segment_node1, segment_node2)


def test_merge_segments6():
    """Hull is p1-p2-p3-p4"""
    pts = [Point.new(1, 1), Point.new(2, 3), Point.new(3, 3), Point.new(4, 1)]
    p1, p2, p3, p4 = pts

    segment_node1, segment_node2 = make_two_segment_nodes(pts)
    joint_node = DynamicHullNode(data=p2, subhull=[p1, p2, p3, p4], left_supporting_index=1, left_supporting=p2, right_supporting=p3)
    joint_node.left, joint_node.right = segment_node1, segment_node2

    assert joint_node == merge(segment_node1, segment_node2)


def test_merge_segment_and_point1():
    """Segment p1-p2 and point p3, where p2 is above p1-p3."""
    pts = [Point.new(0, 1), Point.new(2, 0), Point.new(5, 5)]
    p1, p2, p3 = pts
    n1, n2, n3 = [DynamicHullNode.leaf(p) for p in pts]
    segment_node = DynamicHullNode(data=p1, subhull=[p1, p2], left_supporting=p1, right_supporting=p2)
    segment_node.left, segment_node.right = n1, n2
    point_node = DynamicHullNode.leaf(p3)

    joint_node = DynamicHullNode(data=p2, subhull=[p1, p3], left_supporting=p1, right_supporting=p3)
    joint_node.left, joint_node.right = segment_node, n3

    assert joint_node == merge(segment_node, point_node)


def test_merge_segment_and_point2():
    """Segment p1-p2 and point p3, where p2 is above p1-p3."""
    pts = [Point.new(0, 1), Point.new(2, 3), Point.new(5, 0)]
    p1, p2, p3 = pts
    n1, n2, n3 = [DynamicHullNode.leaf(p) for p in pts]
    segment_node = DynamicHullNode(data=p1, subhull=[p1, p2], left_supporting=p1, right_supporting=p2)
    segment_node.left, segment_node.right = n1, n2
    point_node = DynamicHullNode.leaf(p3)

    joint_node = DynamicHullNode(data=p2, subhull=[p1, p2, p3], left_supporting_index=1, left_supporting=p2, right_supporting=p3)
    joint_node.left, joint_node.right = segment_node, n3

    assert joint_node == merge(segment_node, point_node)
