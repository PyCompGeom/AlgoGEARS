from __future__ import annotations
from typing import Any, Callable, ClassVar, Iterable
from .core import Line2D, BinTreeNode, BinTree, Point


sort_left_to_right = lambda p: (p.x, -p.y)
sort_right_to_left = lambda p: (-p.x, p.y)


class QuickhullNode(BinTreeNode):
    data: list[Point]
    left: QuickhullNode | None = None
    right: QuickhullNode | None = None
    h: Point | None = None
    subhull: list[Point] | None = None

    def weak_equal(self, other: Any) -> bool:
        return (
            super().weak_equal(other)
            and self.h == other.h
            and self.subhull == other.subhull
        )

    @property
    def points(self) -> list[Point]:
        return self.data
    
    @points.setter
    def points(self, value: list[Point]) -> None:
        self.data = value
    
    @points.deleter
    def points(self) -> None:
        del self.data


class QuickhullTree(BinTree):
    node_class: ClassVar[type] = QuickhullNode
    root: QuickhullNode | None = None


def quickhull(points: Iterable[Point]):
    leftmost_point = min(points, key=lambda p: p.coords)
    rightmost_point = max(points, key=lambda p: p.coords)

    subset1 = make_subset(points, leftmost_point, rightmost_point, sort_key=sort_left_to_right)
    subset2 = make_subset(points, rightmost_point, leftmost_point, sort_key=sort_right_to_left)

    tree = QuickhullTree(root=QuickhullNode(data=(subset1 + subset2[1:-1])))
    tree.root.left, tree.root.right = QuickhullNode(data=subset1), QuickhullNode(data=subset2)

    hull = (
        partition(subset1, leftmost_point, rightmost_point, tree.root.left) +
        partition(subset2, rightmost_point, leftmost_point, tree.root.right)[1:-1]
    )
    tree.root.subhull = hull

    yield leftmost_point, rightmost_point, subset1, subset2
    yield tree
    yield tree
    yield tree
    yield tree

    yield hull


def partition(points: Iterable[Point], left_point: Point, right_point: Point, node: QuickhullNode) -> list[Point]:
    if len(points) == 2:
        node.subhull = [left_point, right_point]
        return node.subhull

    lr_line = Line2D(point1=left_point, point2=right_point)
    pts = filter(lambda p: p != left_point and p != right_point, points)

    h = max(pts, key=lambda p: (Point.dist(p, lr_line), Point.angle(left_point, p, right_point)))
    s1 = left_points(points, left_point, h)
    s2 = left_points(points, h, right_point)

    node.h, node.left, node.right = h, QuickhullNode(data=s1), QuickhullNode(data=s2)
    node.subhull = partition(s1, left_point, h, node.left) + partition(s2, h, right_point, node.right)[1:]
    
    return node.subhull


def make_subset(points: Iterable[Point], left_point: Point, right_point: Point, sort_key: Callable[[Point], Any]) -> list[Point]:
    return sorted(left_points(points, left_point, right_point), key=sort_key)


def left_points(points: Iterable[Point], p1: Point, p2: Point) -> list[Point]:
    """Points p1, p2 and those at the left of the vector p1->p2."""
    return (
        [p1] +
        [p for p in points if Point.direction(p1, p2, p) < 0] +
        [p2]
    )
