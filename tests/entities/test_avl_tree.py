from copy import deepcopy
from algogears.core import BinTreeNode, AVLTree

def test_avl_tree_insertion_no_imbalance():
    test_tree = AVLTree.from_iterable(i for i in range(1, 6))
    tree = deepcopy(test_tree)

    test_tree.insert(6)
    tree.root.right.right.right = BinTreeNode(data=6)

    assert tree == test_tree


def test_avl_tree_deletion_no_imbalance():
    test_tree = AVLTree.from_iterable(i for i in range(1, 12))
    tree = deepcopy(test_tree)
    
    test_tree.delete(6)

    tree.root.data = 7
    tree.root.right.left = BinTreeNode(data=8)

    assert tree == test_tree


def test_avl_tree_insertion_left_left():
    test_tree = AVLTree.from_iterable(i for i in range(1, 8))
    test_tree.insert(3.5)
    test_tree.insert(1.25)
    test_tree.insert(1.5)

    root = BinTreeNode(data=2)
    root.left = BinTreeNode(data=1)
    root.left.right = BinTreeNode(data=1.25)
    root.left.right.right = BinTreeNode(data=1.5)
    root.right = BinTreeNode(data=4)
    root.right.left = BinTreeNode(data=3)
    root.right.left.right = BinTreeNode(data=3.5)
    root.right.right = BinTreeNode(data=6)
    root.right.right.left = BinTreeNode(data=5)
    root.right.right.right = BinTreeNode(data=7)
    tree = AVLTree(root=root)

    assert tree == test_tree


def test_avl_tree_insertion_right_right():
    test_tree = AVLTree.from_iterable(i for i in range(1, 8))
    test_tree.insert(5.5)
    test_tree.insert(8)
    test_tree.insert(9)

    root = BinTreeNode(data=6)
    root.left = BinTreeNode(data=4)
    root.left.left = BinTreeNode(data=2)
    root.left.left.left = BinTreeNode(data=1)
    root.left.left.right = BinTreeNode(data=3)
    root.left.right = BinTreeNode(data=5)
    root.left.right.right = BinTreeNode(data=5.5)
    root.right = BinTreeNode(data=7)
    root.right.right = BinTreeNode(data=8)
    root.right.right.right = BinTreeNode(data=9)
    tree = AVLTree(root=root)

    assert tree == test_tree

def test_avl_tree_insertion_left_right():
    test_tree = AVLTree.from_iterable(i for i in range(1, 12))
    test_tree.insert(0)
    test_tree.insert(0.5)
    test_tree.insert(3.25)
    test_tree.insert(3.5)
    test_tree.insert(5.25)
    test_tree.insert(5.5)
    
    root = BinTreeNode(data=4)
    root.left = BinTreeNode(data=3)
    root.left.left = BinTreeNode(data=1)
    root.left.left.left = BinTreeNode(data=0)
    root.left.left.left.right = BinTreeNode(data=0.5)
    root.left.left.right = BinTreeNode(data=2)
    root.left.right = BinTreeNode(data=3.25)
    root.left.right.right = BinTreeNode(data=3.5)
    root.right = BinTreeNode(data=6)
    root.right.left = BinTreeNode(data=5)
    root.right.left.right = BinTreeNode(data=5.25)
    root.right.left.right.right = BinTreeNode(data=5.5)
    root.right.right = BinTreeNode(data=9)
    root.right.right.left = BinTreeNode(data=7)
    root.right.right.left.right = BinTreeNode(data=8)
    root.right.right.right = BinTreeNode(data=10)
    root.right.right.right.right = BinTreeNode(data=11)
    tree = AVLTree(root=root)

    assert tree == test_tree


def test_avl_tree_insertion_right_left():
    test_tree = AVLTree.from_iterable(i for i in range(1, 12))
    test_tree.insert(6.25)
    test_tree.insert(6.5)
    test_tree.insert(8.25)
    test_tree.insert(12)
    test_tree.insert(8.5)

    root = BinTreeNode(data=7)
    root.left = BinTreeNode(data=6)
    root.left.left = BinTreeNode(data=3)
    root.left.left.left = BinTreeNode(data=1)
    root.left.left.left.right = BinTreeNode(data=2)
    root.left.left.right = BinTreeNode(data=4)
    root.left.left.right.right = BinTreeNode(data=5)
    root.left.right = BinTreeNode(data=6.25)
    root.left.right.right = BinTreeNode(data=6.5)
    root.right = BinTreeNode(data=9)
    root.right.left = BinTreeNode(data=8)
    root.right.left.right = BinTreeNode(data=8.25)
    root.right.left.right.right = BinTreeNode(data=8.5)
    root.right.right = BinTreeNode(data=10)
    root.right.right.right = BinTreeNode(data=11)
    root.right.right.right.right = BinTreeNode(data=12)
    tree = AVLTree(root=root)

    assert tree == test_tree


def test_avl_tree_deletion_left_left():
    test_tree = AVLTree.from_iterable(i for i in range(1, 8))
    test_tree.insert(1.5)
    test_tree.insert(3.5)
    test_tree.delete(5)
    test_tree.delete(7)

    root = BinTreeNode(data=2)
    root.left = BinTreeNode(data=1)
    root.left.right = BinTreeNode(data=1.5)
    root.right = BinTreeNode(data=4)
    root.right.left = BinTreeNode(data=3)
    root.right.left.right = BinTreeNode(data=3.5)
    root.right.right = BinTreeNode(data=6)
    tree = AVLTree(root=root)

    assert tree == test_tree


def test_avl_tree_deletion_right_right():
    test_tree = AVLTree.from_iterable(i for i in range(1, 8))
    test_tree.insert(5.5)
    test_tree.insert(8)
    test_tree.delete(1)
    test_tree.delete(2)

    root = BinTreeNode(data=6)
    root.left = BinTreeNode(data=4)
    root.left.left = BinTreeNode(data=3)
    root.left.right = BinTreeNode(data=5)
    root.left.right.right = BinTreeNode(data=5.5)
    root.right = BinTreeNode(data=7)
    root.right.right = BinTreeNode(data=8)
    tree = AVLTree(root=root)

    assert tree == test_tree


def test_avl_tree_deletiion_left_right():
    test_tree = AVLTree.from_iterable(i for i in range(1, 12))
    test_tree.insert(0)
    test_tree.insert(0.5)
    test_tree.insert(3.25)
    test_tree.insert(3.5)
    test_tree.insert(5.25)
    test_tree.insert(8.5)
    test_tree.insert(5.5)
    test_tree.delete(8.5)

    root = BinTreeNode(data=4)
    root.left = BinTreeNode(data=3)
    root.left.left = BinTreeNode(data=1)
    root.left.left.left = BinTreeNode(data=0)
    root.left.left.left.right = BinTreeNode(data=0.5)
    root.left.left.right = BinTreeNode(data=2)
    root.left.right = BinTreeNode(data=3.25)
    root.left.right.right = BinTreeNode(data=3.5)
    root.right = BinTreeNode(data=6)
    root.right.left = BinTreeNode(data=5)
    root.right.left.right = BinTreeNode(data=5.25)
    root.right.left.right.right = BinTreeNode(data=5.5)
    root.right.right = BinTreeNode(data=9)
    root.right.right.left = BinTreeNode(data=7)
    root.right.right.left.right = BinTreeNode(data=8)
    root.right.right.right = BinTreeNode(data=10)
    root.right.right.right.right = BinTreeNode(data=11)
    tree = AVLTree(root=root)

    assert tree == test_tree


def test_avl_tree_deletion_right_left():
    test_tree = AVLTree.from_iterable(i for i in range(1, 12))
    test_tree.insert(2.5)
    test_tree.insert(6.25)
    test_tree.insert(6.5)
    test_tree.insert(8.25)
    test_tree.insert(12)
    test_tree.insert(8.5)
    test_tree.delete(2.5)

    root = BinTreeNode(data=7)
    root.left = BinTreeNode(data=6)
    root.left.left = BinTreeNode(data=3)
    root.left.left.left = BinTreeNode(data=1)
    root.left.left.left.right = BinTreeNode(data=2)
    root.left.left.right = BinTreeNode(data=4)
    root.left.left.right.right = BinTreeNode(data=5)
    root.left.right = BinTreeNode(data=6.25)
    root.left.right.right = BinTreeNode(data=6.5)
    root.right = BinTreeNode(data=9)
    root.right.left = BinTreeNode(data=8)
    root.right.left.right = BinTreeNode(data=8.25)
    root.right.left.right.right = BinTreeNode(data=8.5)
    root.right.right = BinTreeNode(data=10)
    root.right.right.right = BinTreeNode(data=11)
    root.right.right.right.right = BinTreeNode(data=12)
    tree = AVLTree(root=root)

    assert tree == test_tree


def test_avl_tree_insertion_of_prefilled_node():
    test_tree = AVLTree.from_iterable(i for i in range(1, 3))
    test_tree.insert(BinTreeNode(data=0))

    tree = AVLTree(root=BinTreeNode(data=1, left=BinTreeNode(data=0), right=BinTreeNode(data=2)))
    assert tree == test_tree