from copy import deepcopy
from algogears.core import ThreadedBinTreeNode, ThreadedBinTree


def test_threaded_bin_trees_eq():
    f = root = ThreadedBinTreeNode(data="F")
    b = root.left = ThreadedBinTreeNode(data="B")
    a = root.left.left = ThreadedBinTreeNode(data="A")
    d = root.left.right = ThreadedBinTreeNode(data="D")
    c = root.left.right.left = ThreadedBinTreeNode(data="C")
    e = root.left.right.right = ThreadedBinTreeNode(data="E")
    g = root.right = ThreadedBinTreeNode(data="G")
    i = root.right.right = ThreadedBinTreeNode(data="I")
    h = root.right.right.left = ThreadedBinTreeNode(data="H")

    root2 = deepcopy(root)
    tree = ThreadedBinTree(root=root2)

    a.prev, a.next = i, b
    b.prev, b.next = a, c
    c.prev, c.next = b, d
    d.prev, d.next = c, e
    e.prev, e.next = d, f
    f.prev, f.next = e, g
    g.prev, g.next = f, h
    h.prev, h.next = g, i
    i.prev, i.next = h, a

    assert root == tree.root


def test_threaded_bin_tree_from_iterable():
    lst = ["A", "B", "C", "D", "E"]
    c = root = ThreadedBinTreeNode(data="C")
    a = root.left = ThreadedBinTreeNode(data="A")
    b = root.left.right = ThreadedBinTreeNode(data="B")
    d = root.right = ThreadedBinTreeNode(data="D")
    e = root.right.right = ThreadedBinTreeNode(data="E")

    a.prev, a.next = e, b
    b.prev, b.next = a, c
    c.prev, c.next = b, d
    d.prev, d.next = c, e
    e.prev, e.next = d, a

    tree = ThreadedBinTree(root=root)
    assert tree == ThreadedBinTree.from_iterable(lst)


def test_threaded_bin_tree_non_circular():
    b = root = ThreadedBinTreeNode(data="B")
    a = root.left = ThreadedBinTreeNode(data="A")
    c = root.right = ThreadedBinTreeNode(data="C")

    a.next = b
    b.prev, b.next = a, c
    c.prev = b
    
    tree = ThreadedBinTree(root=root)
    assert tree == ThreadedBinTree.from_iterable(["A", "B", "C"], circular=False)
