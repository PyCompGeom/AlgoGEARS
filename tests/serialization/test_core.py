from copy import deepcopy
from pytest import fixture
from algogears.core import Vector, Point, Line2D, BinTreeNode, BinTree, AVLTree, ThreadedBinTreeNode, ThreadedBinTree


def test_point_serialization():
    point = Point.new(1, 2, 3)
    serialized_point = point.model_dump()
    deserialized_point = Point(**serialized_point)
    assert deserialized_point == point


def test_vector_serialization():
    vector = Vector.new(1, 2, 3)
    serialized_vector = vector.model_dump()
    deserialized_vector = Vector(**serialized_vector)
    assert deserialized_vector == vector


def test_line2d_serialization():
    line = Line2D(point1=Point.new(1, 1), point2=Point.new(2, 2))
    serialized_line = line.model_dump()
    deserialized_line = Line2D(**serialized_line)
    assert deserialized_line == line


@fixture
def root():
    return BinTreeNode(data=1, left=BinTreeNode(data=2), right=BinTreeNode(data=3))


def test_bin_tree_node_serialization(root):
    serialized_root = root.model_dump()
    deserialized_root = BinTreeNode(**serialized_root)
    assert deserialized_root == root


def test_bin_tree_serialization(root):
    tree = BinTree(root=root)
    serialized_tree = tree.model_dump()
    deserialized_tree = BinTree(**serialized_tree)
    assert deserialized_tree == tree


def test_avl_tree_serialization(root):
    avl_tree = AVLTree(root=root)
    serialized_avl_tree = avl_tree.model_dump()
    deserialized_avl_tree = AVLTree(**serialized_avl_tree)
    assert deserialized_avl_tree == avl_tree


@fixture
def tbt_root_circular():
    left = ThreadedBinTreeNode(data=2)
    right = ThreadedBinTreeNode(data=3)
    root = ThreadedBinTreeNode(data=1, left=left, right=right)
    root.prev = left
    root.next = right
    left.prev = right
    left.next = root
    right.prev = root
    right.next = left

    return root


@fixture
def tbt_root(tbt_root_circular):
    tbt_root = deepcopy(tbt_root_circular)
    tbt_root.left.prev = None
    tbt_root.right.next = None

    return tbt_root


def test_threaded_bin_tree_node_seriaization(tbt_root):
    serialized_root = tbt_root.model_dump()
    deserialized_root = ThreadedBinTreeNode(**serialized_root)
    assert deserialized_root == tbt_root


def test_threaded_bin_tree_node__circular_seriaization(tbt_root_circular):
    serialized_root = tbt_root_circular.model_dump()
    deserialized_root = ThreadedBinTreeNode(**serialized_root)
    assert deserialized_root == tbt_root_circular


def test_threaded_bin_tree_serialization(tbt_root):
    tbt = ThreadedBinTree(root=tbt_root)
    serialized_tbt = tbt.model_dump()
    deserialized_tbt = ThreadedBinTree(**serialized_tbt)

    assert deserialized_tbt == tbt


def test_threaded_bin_tree_circular_serialization(tbt_root_circular):
    tbt = ThreadedBinTree(root=tbt_root_circular)
    serialized_tbt = tbt.model_dump()
    deserialized_tbt = ThreadedBinTree(**serialized_tbt)

    assert deserialized_tbt == tbt