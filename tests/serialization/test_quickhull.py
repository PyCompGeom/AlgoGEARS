from pytest import fixture
from algogears.core import Point
from algogears.quickhull import QuickhullNode, QuickhullTree


@fixture
def node():
    p1, p2, p3 = points = [Point.new(1, 1), Point.new(2, 4), Point.new(3, 3)]
    root = QuickhullNode(data=points, subhull=points)
    root.left = QuickhullNode(data=points, h=p2, subhull=points)
    root.right = QuickhullNode(data=[p3, p1], subhull=[p3, p1])
    root.left.left = QuickhullNode(data=[p1, p2], subhull=[p1, p2])
    root.left.right = QuickhullNode(data=[p2, p3], subhull=[p2, p3])

    return root


def test_quickhull_node_adapter_serialization(node):
    serialized_node = node.model_dump()
    deserialized_node = QuickhullNode(**serialized_node)
    assert deserialized_node == node


def test_quickhull_tree_adapter_serialization(node):
    tree = QuickhullTree(root=node)
    serialized_tree = tree.model_dump()
    deserialized_tree = QuickhullTree(**serialized_tree)
    assert deserialized_tree == tree