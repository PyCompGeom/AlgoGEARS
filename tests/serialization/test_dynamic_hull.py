from pytest import fixture
from algogears.core import Point
from algogears.dynamic_hull import DynamicHullNode, DynamicHullTree, SubhullNode, SubhullThreadedBinTree


@fixture
def dynamic_hull_node():
    p1, p2 = Point.new(1, 1), Point.new(2, 2)
    root = DynamicHullNode(
        data=p1,
        subhull=[p1, p2],
        optimized_subhull=[p1, p2],
        left_supporting=p1,
        right_supporting=p2
    )
    root.left = DynamicHullNode.leaf(p1)
    root.right = DynamicHullNode.leaf(p2)

    return root


@fixture
def subhull_node():
    root = SubhullNode(data=Point.new(2, 4))
    root.left = SubhullNode(data=Point.new(1, 1))
    root.right = SubhullNode(data=Point.new(3, 3))
    root.prev = root.left
    root.next = root.right
    root.left.prev = root.right
    root.left.next = root
    root.right.prev = root
    root.right.next = root.left

    return root


def test_dynamic_hull_node_serialization(dynamic_hull_node):
    serialized_node = dynamic_hull_node.model_dump()
    deserialized_node = DynamicHullNode(**serialized_node)
    assert deserialized_node == dynamic_hull_node


def test_dynamic_hull_tree_serialization(dynamic_hull_node):
    tree = DynamicHullTree(root=dynamic_hull_node)
    serialized_tree = tree.model_dump()
    deserialized_tree = DynamicHullTree(**serialized_tree)
    assert deserialized_tree == tree


def test_subhull_node_serialization(subhull_node):
    serialized_node = subhull_node.model_dump()
    deserialized_node = SubhullNode(**serialized_node)
    assert deserialized_node == subhull_node


def test_subhull_tree_serialization(subhull_node):
    tree = SubhullThreadedBinTree(root=subhull_node)
    serialized_tree = tree.model_dump()
    deserialized_tree = SubhullThreadedBinTree(**serialized_tree)
    assert deserialized_tree == tree