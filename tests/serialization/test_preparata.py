from pytest import fixture
from algogears.core import Point
from algogears.preparata import PreparataNode, PreparataThreadedBinTree


@fixture
def node():
    root = PreparataNode(data=Point.new(2, 4))
    root.left = PreparataNode(data=Point.new(1, 1))
    root.right = PreparataNode(data=Point.new(3, 3))
    root.prev = root.left
    root.next = root.right
    root.left.prev = root.right
    root.left.next = root
    root.right.prev = root
    root.right.next = root.left

    return root


def test_preparata_node_serialization(node):
    serialized_node = node.model_dump()
    deserialized_node = PreparataNode(**serialized_node)
    assert deserialized_node == node


def test_preparata_tree_serialization(node):
    tree = PreparataThreadedBinTree(root=node)
    serialized_tree = tree.model_dump()
    deserialized_tree = PreparataThreadedBinTree(**serialized_tree)
    assert deserialized_tree == tree