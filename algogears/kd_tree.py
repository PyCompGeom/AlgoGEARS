from __future__ import annotations
from typing import ClassVar, Iterable
from pydantic import Field
from .core import BinTreeNode, BinTree, Point


class KDTreeNode(BinTreeNode):
    data: Point
    left: KDTreeNode | None = None
    right: KDTreeNode | None = None


class KDTree(BinTree):
    node_class: ClassVar[type] = KDTreeNode
    root: KDTreeNode | None = None
    x_range: tuple[float, float]
    y_range: tuple[float, float]
    partition: list[tuple[Point, bool]] = Field(default_factory=list)
    search_list: list[tuple[Point, bool, bool]] = Field(default_factory=list)

    def build_tree(self, points: Iterable, node: KDTreeNode, vertical: bool = True) -> None:
        mid = len(points) // 2
        part = (points[mid], vertical)
        
        if all(p[0] != part[0] for p in self.partition):
            self.partition.append(part)

        if mid == 0:
            return

        if vertical:
            sort_key = lambda p: p.y
        else:
            sort_key = lambda p: p.x
        
        list_l = sorted(points[:mid], key=sort_key)
        list_r = sorted(points[-mid:], key=sort_key)
        left, right = list_l[mid // 2], list_r[mid // 2]

        node.left = KDTreeNode(data=left)
        if node.data != right:
            node.right = KDTreeNode(data=right)

        self.build_tree(list_l, node.left, not vertical)
        self.build_tree(list_r, node.right, not vertical)

    def region_search(self, node: KDTreeNode, vertical: bool = True) -> list[Point]:
        if vertical:
            left, right, coord = self.x_range[0], self.x_range[1], node.data.x
        else:
            left, right, coord = self.y_range[0], self.y_range[1], node.data.y

        points = []
        to_add = self.point_in_region(node.data)

        if to_add:
            points.append(node.data)

        intersection = left <= coord <= right        
        self.search_list.append((node.data, to_add, intersection))

        if node.left and left < coord:
            points.extend(self.region_search(node.left, not vertical))
        if node.right and coord < right:
            points.extend(self.region_search(node.right, not vertical))

        return points

    def point_in_region(self, point: Point) -> bool:
        return self.x_range[0] <= point.x <= self.x_range[1] and self.y_range[0] <= point.y <= self.y_range[1]
    
    def __eq__(self, other: object) -> bool:
        return super().__eq__(other) and self.x_range == other.x_range and self.y_range == other.y_range


def kd_tree(points: Iterable[Point], x_range: list[Point, Point], y_range: list[Point, Point]):
    ordered_x = sorted(points)
    ordered_y = sorted(points, key=lambda p: (p.y, p.x))
    yield ordered_x, ordered_y

    root = KDTreeNode(data=ordered_x[len(ordered_x) // 2])
    tree = KDTree(root=root, x_range=x_range, y_range=y_range)
    tree.build_tree(ordered_x, root)
    yield tree.partition
    yield tree

    result = tree.region_search(root, vertical=True)
    yield tree.search_list
    yield result
