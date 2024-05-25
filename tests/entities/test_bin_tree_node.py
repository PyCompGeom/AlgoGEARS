from algogears.core import BinTreeNode


def test_bin_tree_node_weak_eq():
    root1 = BinTreeNode(data=1, left=BinTreeNode(data=2), right=BinTreeNode(data=3))
    root2 = BinTreeNode(data=1, left=BinTreeNode(data=2), right=BinTreeNode(data=3))

    assert root1.weak_equal(root2)
    assert root1.left.weak_equal(root2.left)
    assert root1.right.weak_equal(root2.right)


def test_bin_tree_node_strong_eq():
    root1 = BinTreeNode(data=1, left=BinTreeNode(data=2), right=BinTreeNode(data=3))
    root2 = BinTreeNode(data=1, left=BinTreeNode(data=2), right=BinTreeNode(data=3))

    assert root1 == root2
    assert root1.left == root2.left
    assert root1.right == root2.right