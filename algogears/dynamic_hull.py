from __future__ import annotations
from copy import deepcopy
from typing import ClassVar, Iterable
from pydantic import Field
from .core import PathDirection, BinTreeNode, AVLTree, ThreadedBinTree, ThreadedBinTreeNode, PointType, Point
from .jarvis import jarvis


class DynamicHullNode(BinTreeNode):
    data: Point
    left: DynamicHullNode | None = None
    right: DynamicHullNode | None = None
    subhull: list[Point]
    optimized_subhull: list[Point] = Field(default_factory=list)
    left_supporting_index: int = 0
    left_supporting: Point
    right_supporting: Point
    
    @property
    def point(self) -> Point:
        return self.data
    
    @point.setter
    def point(self, value: Point) -> None:
        self.data = value
    
    @point.deleter
    def point(self) -> None:
        del self.data

    @property
    def is_point(self) -> bool:
        return len(self.subhull) == 1

    @property
    def is_segment(self) -> bool:
        return len(self.subhull) == 2
    
    @classmethod
    def leaf(cls, point: Point) -> DynamicHullNode:
        return cls(data=point, subhull=[point], left_supporting=point, right_supporting=point)

    def weak_equal(self, other: object) -> bool:
        return (
            super().weak_equal(other)
            and self.subhull == other.subhull
            and self.left_supporting_index == other.left_supporting_index
            and self.left_supporting == other.left_supporting
            and self.right_supporting == other.right_supporting
            and self.optimized_subhull == other.optimized_subhull
        )


class DynamicHullTree(AVLTree):
    node_class: ClassVar[type] = DynamicHullNode
    root: DynamicHullNode | None = None

    @classmethod
    def from_iterable(cls, iterable: Iterable[Point]) -> DynamicHullTree:
        return cls(root=cls._from_iterable(iterable))
    
    @classmethod
    def _from_iterable(cls, iterable: Iterable[Point], i: list[int] | None = None, n: int | None = None) -> DynamicHullNode:
        if i is None:
            i = [0]
        if n is None:
            n = len(iterable)
        if n == 1:
            point = iterable[i[0]]
            i[0] += 1
            return DynamicHullNode.leaf(point)

        n_right = n // 2
        n_left = n - n_right
        left, right = cls._from_iterable(iterable, i, n_left), cls._from_iterable(iterable, i, n_right)
        node = merge(left, right)

        return node
    
    def insert(self, point: Point, starting_node: DynamicHullNode | None = None, path: list[PathDirection] | None = None) -> None:
        if starting_node is None:
            starting_node = self.root
        if path is None:
            path = []
        
        self.root = self._insert(point, starting_node, path)
    
    def _insert(self, point: Point, node: DynamicHullNode, path: list[PathDirection]) -> DynamicHullNode:
        if node.is_leaf:
            node_copy = deepcopy(node)
            new_node = DynamicHullNode.leaf(point)
            node.left = new_node if point < node.point else node_copy
            node.right = node_copy if point < node.point else new_node
        elif point < node.point:
            path.append(PathDirection.left)
            node.left = self._insert(point, node.left, path)
        else:
            path.append(PathDirection.right)
            node.right = self._insert(point, node.right, path)

        return self._merge_with_rebalance(node)
    
    def delete(self, point: Point, starting_node: DynamicHullNode | None = None, path: list[PathDirection] | None = None) -> None:
        if starting_node is None:
            starting_node = self.root
        if path is None:
            path = []
        
        self.root = self._delete(point, starting_node, path)
    
    def _delete(self, point: Point, node: DynamicHullNode, path: list[PathDirection]) -> DynamicHullNode | None:
        if node.is_leaf:
            return None
        elif point <= node.point:
            path.append(PathDirection.left)
            node.left = self._delete(point, node.left, path)
        else:
            path.append(PathDirection.right)
            node.right = self._delete(point, node.right, path)
        
        if node.left is None:
            return node.right
        if node.right is None:
            return node.left
        
        return self._merge_with_rebalance(node)
    
    def _merge_with_rebalance(self, node: DynamicHullNode) -> DynamicHullNode:
        node.set_height()

        if node.balance_factor == -2 or node.balance_factor == 2:
            bf, left_bf, right_bf = node.balance_factor, node.left.balance_factor, node.right.balance_factor
            node = self.rebalance(node)

            # Re-evaluate lower subhulls affected by rebalancing
            if (bf == 2) or (bf == -2 and left_bf == 1):
                node.left = merge(node.left.left, node.left.right)
            if (bf == -2) or (bf == 2 and right_bf == -1):
                node.right = merge(node.right.left, node.right.right)

        return merge(node.left, node.right)


class SubhullNode(ThreadedBinTreeNode):
    data: Point
    left: SubhullNode | None = None
    right: SubhullNode | None = None
    prev: SubhullNode | int | None = None
    next: SubhullNode | int | None = None

    @property
    def point(self) -> Point:
        return self.data
    
    @point.setter
    def point(self, value: Point) -> None:
        self.data = value
    
    @point.deleter
    def point(self) -> None:
        del self.data


class SubhullThreadedBinTree(ThreadedBinTree):
    node_class: ClassVar[type] = SubhullNode
    root: SubhullNode | None = None

    @classmethod
    def from_iterable(cls, iterable):
        return super().from_iterable(iterable, circular=False)


def upper_dynamic_hull(points: Iterable[Point], point_to_insert_or_delete: Point):
    points.sort()

    tree = DynamicHullTree.from_iterable(points)
    optimize_dynamic_hull_tree(tree.root)
    yield tree.leaves_inorder()
    yield tree
    yield tree
    yield tree
    yield tree
    yield tree

    path = []
    modified_tree = deepcopy(tree)
    if point_to_insert_or_delete in points:
        modified_tree.delete(point_to_insert_or_delete, path=path)
    else:
        modified_tree.insert(point_to_insert_or_delete, path=path)
    
    yield path

    optimize_dynamic_hull_tree(modified_tree.root)
    hull = modified_tree.root.subhull

    yield modified_tree, hull
    yield hull


def merge(node1: DynamicHullNode, node2: DynamicHullNode) -> DynamicHullNode:
    if node1.is_point or node2.is_point or node1.is_segment or node2.is_segment:
        return merge_trivial(node1, node2)

    # Find supporting points in subhull TBTs
    subhull_tbt1, subhull_tbt2 = SubhullThreadedBinTree.from_iterable(node1.subhull), SubhullThreadedBinTree.from_iterable(node2.subhull)
    subhull_node1, subhull_node2 = subhull_tbt1.root, subhull_tbt2.root
    prev_node1, prev_node2 = None, None
    while prev_node1 is not subhull_node1 or prev_node2 is not subhull_node2:
        prev_node1, prev_node2 = subhull_node1, subhull_node2
        subhull_node1, subhull_node2 = next_nodes(subhull_node1, subhull_node2)
    
    # Merge two subhulls into a new subhull
    subhull = node1.subhull[:node1.subhull.index(prev_node1.point)+1] + node2.subhull[node2.subhull.index(prev_node2.point):]
    
    # Construct a parent node containing the new subhull
    joint_node = DynamicHullNode(
        data=node1.rightmost_node.point,
        subhull=subhull,
        left_supporting_index=subhull.index(prev_node1.point),
        left_supporting=prev_node1.point,
        right_supporting=prev_node2.point
    )
    joint_node.left, joint_node.right = node1, node2
    joint_node.set_height()
    
    return joint_node


def merge_trivial(node1: DynamicHullNode, node2: DynamicHullNode) -> DynamicHullNode:
    """
        Merge two nodes by constructing the convex hull of their points with Jarvis' algorithm and extracting its upper part.
        
        For efficiency's sake, only use in trivial cases, such as point & point, segment & point, and segment & segment.
    """
    points = node1.subhull + node2.subhull
    subhull = (
        ([] if len(points) == 2 and points[0].x == points[1].x else [points[0]]) +
        [p for p in jarvis(points) if Point.direction(points[0], points[-1], p) < 0] +
        [points[-1]]
    )
    
    rightmost_point_in_left_subtree = node1.rightmost_node.point
    left_supporting = subhull[0] if len(subhull) == 1 else next(p for p in reversed(node1.subhull) if p in subhull)
    left_supporting_index = subhull.index(left_supporting)
    right_supporting = subhull[0] if len(subhull) == 1 else subhull[left_supporting_index+1]
    
    joint_node = DynamicHullNode(
        data=rightmost_point_in_left_subtree,
        subhull=subhull,
        left_supporting_index=left_supporting_index,
        left_supporting=left_supporting,
        right_supporting=right_supporting
    )
    joint_node.left, joint_node.right = node1, node2
    joint_node.set_height()

    return joint_node


def next_nodes(node1: DynamicHullNode, node2: DynamicHullNode) -> DynamicHullNode:
    type1, type2 = PointType.by_nodes(node2, node1), PointType.by_nodes(node1, node2)
    return next_left_node(node1, type1), next_right_node(node2, type2)


def next_left_node(node: DynamicHullNode, point_type: PointType) -> DynamicHullNode:
    return {
        PointType.reflex: node.right,
        PointType.right_supporting: node,
        PointType.convex: node.left
    }[point_type]


def next_right_node(node: DynamicHullNode, point_type: PointType) -> DynamicHullNode:
    return {
        PointType.reflex: node.left,
        PointType.left_supporting: node,
        PointType.convex: node.right
    }[point_type]


def optimize_dynamic_hull_tree(node: DynamicHullNode, parent_node: DynamicHullNode | None = None) -> None:
    node.optimized_subhull = node.subhull
    _optimize_dynamic_hull_tree(node, parent_node)


def _optimize_dynamic_hull_tree(node: DynamicHullNode, parent_node: DynamicHullNode | None) -> None:
    if node.left:
        optimize_dynamic_hull_tree(node.left, node)
    if node.right:
        optimize_dynamic_hull_tree(node.right, node)
    if parent_node:
        optimize_subhull(node, parent_node)


def optimize_subhull(node: DynamicHullNode, parent_node: DynamicHullNode) -> None:
    node_points = node.subhull
    parent_points = set(parent_node.subhull)
    node.optimized_subhull = [p for p in node_points if p not in parent_points]
