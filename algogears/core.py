from __future__ import annotations
from copy import deepcopy
from enum import Enum
from math import inf, pi, acos, atan2, isclose
from typing import Iterable, Generator, Any, ClassVar
from pydantic import BaseModel, Extra, Field


class SerializablePydanticModelWithPydanticFields(BaseModel):
    """
        A class to ensure correct serialization of Pydantic models that have fields also being Pydantic models,
        with possible cyclic references whose custom serialization is specified in those models.
    """
    def model_dump(self, *args, **kwargs):
        tmp_fields_dict = {}
        this_utility_class = SerializablePydanticModelWithPydanticFields

        for field, value in self.__dict__.items():
            tmp_fields_dict[field] = value
            
            if isinstance(value, this_utility_class):
                setattr(self, field, value.model_dump())
            elif isinstance(value, dict):
                setattr(
                    self,
                    field,
                    {
                        (k.model_dump() if isinstance(k, this_utility_class) else k): (v.model_dump() if isinstance(v, this_utility_class) else v)
                        for k, v in value.items()
                    }
                )
            elif not isinstance(value, str) and not isinstance(value, BaseModel) and isinstance(value, Iterable): # BaseModel's are Iterables, but we don't need them to be checked here 
                generator = (item.model_dump() if isinstance(item, this_utility_class) else item for item in value)
                setattr(self, field, generator if isinstance(value, Generator) else value.__class__(generator))
                
        result = super().model_dump(*args, **kwargs)

        for field, value in tmp_fields_dict.items():
            setattr(self, field, value)
        
        return result


class Vector(BaseModel):
    coords: tuple[float, ...]
    
    @classmethod
    def new(cls, *coords):
        return cls(coords=coords)

    @property
    def x(self) -> float:
        return self.coords[0]
    
    @property
    def y(self) -> float:
        return self.coords[1]
    
    @property
    def z(self) -> float:
        return self.coords[2]
    
    @classmethod
    def from_points(cls, point1, point2) -> Vector:
        return cls(coords=(point2 - point1).coords)
    
    @classmethod
    def dot_product(cls, vector1: Vector, vector2: Vector) -> float:
        if not isinstance(vector1, Vector) or not isinstance(vector2, Vector):
            raise TypeError(f"operands must be of type {Vector}")

        return sum(coord1 * coord2 for coord1, coord2 in zip(vector1.coords, vector2.coords))

    @classmethod
    def cross_product(cls, vector1: Vector, vector2: Vector) -> float:
        if not isinstance(vector1, Vector) or not isinstance(vector2, Vector):
            raise TypeError(f"operands must be of type {Vector}")

        return vector1.x * vector2.y - vector1.y * vector2.x

    def norm(self, metric: str = 'euclidean') -> float:
        try:
            p = {
                'octahedral': 1,
                'euclidean': 2,
                'cubic': inf
            }[metric]
        except KeyError:
            raise ValueError(f'unknown metric "{metric}"')

        if p == inf:
            return max(abs(c) for c in self.coords)
        
        return sum(abs(c**p) for c in self.coords) ** (1 / p)
    
    def normalize(self, metric: str = 'euclidean') -> None:
        self.coords = tuple(c / self.norm(metric) for c in self.coords)
    
    def __str__(self) -> str:
        return f"({', '.join(str(c) for c in self.coords)})"


class Point(BaseModel):
    coords: tuple[float, ...]
    
    @classmethod
    def new(cls, *coords):
        return cls(coords=coords)

    @property
    def x(self) -> float:
        return self.coords[0]
    
    @property
    def y(self) -> float:
        return self.coords[1]
    
    @property
    def z(self) -> float:
        return self.coords[2]
    
    @classmethod
    def centroid(cls, *points: Iterable[Point]) -> Point:
        return cls.new(*(sum(coords) / len(coords) for coords in zip(*[p.coords for p in points])))
    
    @staticmethod
    def angle(point1: Point, point2: Point, point3: Point) -> float:
        v1 = Vector.from_points(point2, point1)
        v2 = Vector.from_points(point2, point3)
        v1.normalize()
        v2.normalize()

        return acos(Vector.dot_product(v1, v2) / (v1.norm() * v2.norm()))

    @staticmethod
    def polar_angle(point: Point, origin: Point) -> float:
        return atan2(point.y - origin.y, point.x - origin.x)
    
    @classmethod
    def nonnegative_polar_angle(cls, point: Point, origin: Point) -> float:
        angle = cls.polar_angle(point, origin)
        return angle if angle >= 0 else 2 * pi + angle

    @classmethod
    def dist(cls, point: Point, obj: Point | Line2D, metric: str ="euclidean") -> float:
        if isinstance(obj, Point):
            try:
                p = {
                    "manhattan": 1,
                    "euclidean": 2,
                    "chebyshev": inf
                }[metric]
            except KeyError:
                raise ValueError(f'unknown metric "{metric}"')
            
            if p == inf:
                return max(abs(c1-c2) for c1, c2 in zip(point.coords, obj.coords))
            
            return sum(abs((c1-c2)**p) for c1, c2 in zip(point.coords, obj.coords)) ** (1 / p)
        
        if isinstance(obj, Line2D):
            try:
                p = {
                    "euclidean": 2,
                    "manhattan": inf
                }[metric]
            except KeyError:
                raise ValueError(f'unknown metric "{metric}"')
            
            denominator = max(abs(obj.a, obj.b)) if p == inf else (obj.a**2 + obj.b**2) ** 0.5
            return abs(obj.a*point.x+obj.b*point.y+obj.c) / denominator

    @staticmethod
    def direction(point1: Point, point2: Point, point3: Point) -> float:
        v1 = Vector.from_points(point1, point3)
        v2 = Vector.from_points(point1, point2)

        return Vector.cross_product(v1, v2)

    def __len__(self) -> int:
        return len(self.coords)
    
    def __getitem__(self, key: int) -> float:
        return self.coords[key]
    
    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, self.__class__)
            and all(isclose(c1, c2, abs_tol=1e-3, rel_tol=0) for c1, c2 in zip(self.coords, other.coords))
        )
    
    def __lt__(self, other: Point) -> bool:
        if not isinstance(other, self.__class__):
            raise TypeError(f'right operand of "<" must be of {self.__class__} type')
        
        return self.coords < other.coords
    
    def __gt__(self, other: Point) -> bool:
        if not isinstance(other, self.__class__):
            raise TypeError(f'right operand of ">" must be of {self.__class__} type')

        return self.coords > other.coords
    
    def __le__(self, other: Point) -> bool:
        if not isinstance(other, self.__class__):
            raise TypeError(f'right operand of "<=" must be of {self.__class__} type')
        
        return self < other or self == other
    
    def __ge__(self, other: Point) -> bool:
        if not isinstance(other, self.__class__):
            raise TypeError(f'right operand of ">=" must be of {self.__class__} type')
        
        return self > other or self == other

    def __add__(self, other: Point) -> bool:
        if not isinstance(other, self.__class__):
            raise TypeError(f"right operand of addition must be of {self.__class__} type")
        
        return self.__class__.new(*(c1 + c2 for c1, c2 in zip(self.coords, other.coords)))
    
    def __sub__(self, other: Point) -> bool:
        if not isinstance(other, self.__class__):
            raise TypeError(f"right operand of subtraction must be of {self.__class__} type")
        
        return self.__class__.new(*(c1 - c2 for c1, c2 in zip(self.coords, other.coords)))
    
    def __hash__(self) -> int:
        return hash(self.coords)
    
    def __str__(self) -> str:
        return f"({', '.join(str(c) for c in self.coords)})"


class Turn:
    LEFT = 'left'
    RIGHT = 'right'
    STRAIGHT = 'straight'

    def __new__(cls, start_point: Point, intermediary_point: Point, end_point: Point) -> Turn:
        vector_start_to_end = Vector.from_points(start_point, end_point)
        vector_start_to_intermediary = Vector.from_points(start_point, intermediary_point)

        direction = Vector.cross_product(vector_start_to_end, vector_start_to_intermediary)

        if direction < 0:
            return cls.LEFT
        if direction > 0:
            return cls.RIGHT
        
        return cls.STRAIGHT


class Line2D(SerializablePydanticModelWithPydanticFields):
    """A 2D line represented by the equation ax + by + c = 0 or y = slope * x + y_intercept."""
    point1: Point
    point2: Point

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if len(self.point1) != 2 or len(self.point2) != 2:
            raise ValueError(f"2D line must be initialized with two 2D points")

        if self.point1 == self.point2:
            raise ValueError(f"2D line must be initialized with two distinct points")
    
    @property
    def a(self) -> float:
        return self.point1.y - self.point2.y
    
    @property
    def b(self) -> float:
        return self.point2.x - self.point1.x
    
    @property
    def c(self) -> float:
        return self.point1.x * self.point2.y - self.point2.x * self.point1.y
    
    @property
    def slope(self) -> float:
        return -inf if self.b == 0 else -self.a / self.b
    
    @property
    def y_intercept(self) -> float:
        return -inf if self.b == 0 else -self.c / self.b


class GraphEdge(SerializablePydanticModelWithPydanticFields):
    first: object
    second: object
    weight: float = 0
    name: str | None = None

    def __repr__(self) -> str:
        return self.name if self.name else f"{str(self.first)}->{str(self.second)}"

    def __hash__(self) -> int:
        return hash((self.first, self.second)) + hash((self.second, self.first)) + hash(self.weight)
    
    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)
            and (
                self.first == other.first and self.second == other.second
                or self.first == other.second and self.second == other.first
            )
        )

    @property
    def reversed(self) -> GraphEdge:
        return self.__class__(first=self.second, second=self.first, weight=self.weight)
    
    def other_node(self, node: object):
        if self.first == node:
            return self.second
        if self.second == node:
            return self.first

        raise ValueError(f"node {node} is absent in this edge")


class Graph(SerializablePydanticModelWithPydanticFields):
    nodes: set[object] = Field(default_factory=set)
    edges: set[GraphEdge] = Field(default_factory=set)
    node_class: ClassVar[type] = object
    edge_class: ClassVar[type] = GraphEdge

    def add_node(self, node: object) -> None:
        if not isinstance(node, self.node_class):
            raise TypeError(f"nodes of {self.__class__.__name__} must be of {self.node_class.__name__} type")

        self.nodes.add(node)

    def add_edge(self, edge: GraphEdge) -> None:
        if not isinstance(edge, self.edge_class):
            raise TypeError(f"edges of {self.__class__.__name__} must be of {self.edge_class.__name__} type")

        if edge.reversed not in self.edges:
            self.edges.add(edge)
            
            self.add_node(edge.first)
            self.add_node(edge.second)
    
    def has_node(self, node: object) -> bool:
        return node in self.nodes
    
    def has_edge(self, edge: GraphEdge) -> bool:
        return edge in self.edges or edge.reversed in self.edges

    def remove_node(self, node: object) -> None:
        self.nodes.remove(node)

        for edge in self.edges.copy():
            if edge.first == node or edge.second == node:
                self.remove_edge(edge)
    
    def remove_edge(self, edge: GraphEdge) -> None:
        self.edges.remove(edge)
    
    def edges_of(self, node: object) -> list[GraphEdge]:
        return [edge for edge in self.edges if edge.first == node or edge.second == node]


class OrientedGraphEdge(GraphEdge):
    def __hash__(self) -> int:
        return hash((self.first, self.second, self.weight))

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.first == other.first
            and self.second == other.second
        )


class OrientedGraph(Graph):
    def add_edge(self, edge: GraphEdge) -> None:
        if not isinstance(edge, self.edge_class):
            raise TypeError(f"edges of {self.__class__.__name__} must be of {self.edge_class.__name__} type")
        
        self.edges.add(edge)

        if edge.first not in self.nodes:
            self.add_node(edge.first)
        if edge.second not in self.nodes:
            self.add_node(edge.second)
    
    def has_edge(self, edge: GraphEdge) -> bool:
        return edge in self.edges


class PlanarStraightLineGraphEdge(GraphEdge):
    first: Point
    second: Point


class PlanarStraightLineGraph(Graph):
    nodes: set[Point] = Field(default_factory=set)
    edges: set[PlanarStraightLineGraphEdge] = Field(default_factory=set)
    node_class: ClassVar[type] = Point
    edge_class: ClassVar[type] = PlanarStraightLineGraphEdge

    def inward_edges(self, node: Point) -> list[PlanarStraightLineGraphEdge]:
        inward_edges = (edge for edge in self.edges_of(node) if max(edge.first, edge.second, key=lambda e: (e.y, e.x)) is node)
        return sorted(inward_edges, key=lambda edge: Point.nonnegative_polar_angle(edge.other_node(node), node))
    
    def outward_edges(self, node: Point) -> list[PlanarStraightLineGraphEdge]:
        outward_edges = (edge for edge in self.edges_of(node) if min(edge.first, edge.second, key=lambda e: (e.y, e.x)) is node)
        return sorted(outward_edges, key=lambda edge: -Point.polar_angle(edge.other_node(node), node))


class OrientedPlanarStraightLineGraphEdge(OrientedGraphEdge):
    first: Point
    second: Point


class OrientedPlanarStraightLineGraph(OrientedGraph):
    nodes: set[Point] = Field(default_factory=set)
    edges: set[OrientedPlanarStraightLineGraphEdge] = Field(default_factory=set)
    node_class: ClassVar[type] = Point
    edge_class: ClassVar[type] = OrientedPlanarStraightLineGraphEdge

    @classmethod
    def from_planar_straight_line_graph(cls, planar_straight_line_graph: PlanarStraightLineGraph) -> OrientedPlanarStraightLineGraph:
        nodes = planar_straight_line_graph.nodes
        edges = {cls.upward_oriented_planar_straight_line_graph_edge(edge) for edge in planar_straight_line_graph.edges}
        return cls(nodes=nodes, edges=edges)

    @classmethod
    def upward_oriented_planar_straight_line_graph_edge(cls, edge: PlanarStraightLineGraphEdge) -> OrientedPlanarStraightLineGraphEdge:
        lower_node = min(edge.first, edge.second, key=lambda e: (e.y, e.x))
        upper_node = edge.other_node(lower_node)
        return OrientedPlanarStraightLineGraphEdge(first=lower_node, second=upper_node, weight=edge.weight)

    def is_regular(self) -> bool:
        min_node = min(self.nodes, key=lambda node: (node.y, node.x))
        max_node = max(self.nodes, key=lambda node: (node.y, node.x))
        
        return all(
            (node is min_node or self.inward_edges(node))
            and
            (node is max_node or self.outward_edges(node))
            for node in self.nodes
        )

    def regularize(self) -> None:
        nodes_bottom_to_top = sorted(self.nodes, key=lambda node: (node.y, node.x))
        self.regularize_bottom_to_top(nodes_bottom_to_top)

        nodes_top_to_bottom = reversed(nodes_bottom_to_top)
        self.regularize_top_to_bottom(nodes_top_to_bottom)

    def regularize_bottom_to_top(self, nodes: Iterable[Point]) -> None:
        swept_edges = []

        for i, node in enumerate(nodes):
            inward_edges = self.inward_edges(node)
            outward_edges = self.outward_edges(node)

            insert_outward_edges_at = self.outward_edges_insertion_index_in_swept_edges(node, swept_edges, inward_edges)

            if i != 0 and not inward_edges:
                self.add_regularizing_inward_edge(node, swept_edges, insert_outward_edges_at)

            self.delete_edges_from_swept_edges(inward_edges, swept_edges, delete_at=insert_outward_edges_at)
            self.insert_edges_to_swept_edges(outward_edges, swept_edges, insert_at=insert_outward_edges_at)
    
    def inward_edges(self, node: Point) -> list[OrientedPlanarStraightLineGraphEdge]:
        inward_edges = (edge for edge in self.edges_of(node) if edge.second == node)
        return sorted(inward_edges, key=lambda edge: Point.nonnegative_polar_angle(edge.other_node(node), node))
    
    def outward_edges(self, node: Point) -> list[OrientedPlanarStraightLineGraphEdge]:
        outward_edges = (edge for edge in self.edges_of(node) if edge.first == node)
        return sorted(outward_edges, key=lambda edge: -Point.polar_angle(edge.other_node(node), node))

    @classmethod
    def outward_edges_insertion_index_in_swept_edges(cls, node: Point, swept_edges: list[OrientedPlanarStraightLineGraphEdge], inward_edges: list[OrientedPlanarStraightLineGraphEdge]) -> int:
        try:
            return swept_edges.index(inward_edges[0])
        except (IndexError, ValueError):
            return cls.outward_edges_insertion_index_in_swept_edges_by_current_node(node, swept_edges)

    @classmethod
    def outward_edges_insertion_index_in_swept_edges_by_current_node(cls, current_node: Point, swept_edges: list[PlanarStraightLineGraphEdge]) -> int:
        for i, edge in enumerate(swept_edges):
            turn = Turn(edge.first, edge.second, current_node)
            if turn == Turn.LEFT or (turn == Turn.STRAIGHT and current_node < edge.first):
                return i
        
        return len(swept_edges) # if there are no edges, insert at position 0

    def add_regularizing_inward_edge(self, current_node: Point, swept_edges: list[OrientedPlanarStraightLineGraphEdge], outward_edges_insertion_index_in_swept_edges: int) -> None:
        is_left_edge_missing = outward_edges_insertion_index_in_swept_edges != 0
        is_right_edge_missing = outward_edges_insertion_index_in_swept_edges != len(swept_edges)

        left_edge = swept_edges[outward_edges_insertion_index_in_swept_edges-1] if is_left_edge_missing else None
        right_edge = swept_edges[outward_edges_insertion_index_in_swept_edges] if is_right_edge_missing else None

        lower_node_vertically_closest_to_current = self.uppermost_lower_node(left_edge, right_edge)
        self.add_edge(OrientedPlanarStraightLineGraphEdge(first=lower_node_vertically_closest_to_current, second=current_node))

    @classmethod
    def uppermost_lower_node(cls, left_edge: OrientedPlanarStraightLineGraphEdge = None, right_edge: OrientedPlanarStraightLineGraphEdge = None):
        if left_edge is None:
            return right_edge.first
        if right_edge is None:
            return left_edge.first
        
        return max(left_edge, right_edge, key=lambda edge: (edge.first.y, edge.first.x)).first
    
    @classmethod
    def delete_edges_from_swept_edges(cls, edges: list[OrientedPlanarStraightLineGraphEdge], swept_edges: list[OrientedPlanarStraightLineGraphEdge], delete_at: int) -> None:
        del swept_edges[delete_at : delete_at+len(edges)]

    @classmethod
    def insert_edges_to_swept_edges(cls, edges: list[OrientedPlanarStraightLineGraphEdge], swept_edges: list[OrientedPlanarStraightLineGraphEdge], insert_at: int) -> None:
        swept_edges[insert_at : insert_at] = edges
    
    def regularize_top_to_bottom(self, nodes: Iterable[Point]) -> None:
        swept_edges = []

        for i, node in enumerate(nodes):
            inward_edges = self.inward_edges(node)
            outward_edges = self.outward_edges(node)

            insert_inward_edges_at = self.inward_edges_insertion_index_in_swept_edges(node, swept_edges, outward_edges) # probably wrong, should be other index before deletion

            if i != 0 and not outward_edges:
                self.add_regularizing_outward_edge(node, swept_edges, insert_inward_edges_at)
            
            self.delete_edges_from_swept_edges(outward_edges, swept_edges, delete_at=insert_inward_edges_at)
            self.insert_edges_to_swept_edges(inward_edges, swept_edges, insert_at=insert_inward_edges_at)
    
    @classmethod
    def inward_edges_insertion_index_in_swept_edges(cls, node: Point, swept_edges: list[OrientedPlanarStraightLineGraphEdge], outward_edges: list[OrientedPlanarStraightLineGraphEdge]) -> int:
        try:
            return swept_edges.index(outward_edges[0])
        except (IndexError, ValueError):
            return cls.inward_edges_insertion_index_in_swept_edges_by_current_node(node, swept_edges)
    
    @classmethod
    def inward_edges_insertion_index_in_swept_edges_by_current_node(cls, current_node: Point, swept_edges: list[PlanarStraightLineGraphEdge]) -> int:
        for i, edge in enumerate(swept_edges):
            turn = Turn(edge.first, edge.second, current_node)
            if turn == Turn.LEFT or (turn == Turn.STRAIGHT and current_node < edge.first):
                return i
        
        return len(swept_edges) # if there are no edges, insert at position 0
    
    def add_regularizing_outward_edge(self, current_node: Point, swept_edges: list[OrientedPlanarStraightLineGraphEdge], inward_edges_insertion_index_in_swept_edges: int) -> None:
        is_left_edge_missing = inward_edges_insertion_index_in_swept_edges != 0
        is_right_edge_missing = inward_edges_insertion_index_in_swept_edges != len(swept_edges)

        left_edge = swept_edges[inward_edges_insertion_index_in_swept_edges-1] if is_left_edge_missing else None
        right_edge = swept_edges[inward_edges_insertion_index_in_swept_edges] if is_right_edge_missing else None

        upper_node_vertically_closest_to_current = self.lowermost_upper_node(left_edge, right_edge)
        self.add_edge(OrientedPlanarStraightLineGraphEdge(first=current_node, second=upper_node_vertically_closest_to_current))
    
    @classmethod
    def lowermost_upper_node(cls, left_edge: OrientedPlanarStraightLineGraphEdge = None, right_edge: OrientedPlanarStraightLineGraphEdge = None):
        if left_edge is None:
            return right_edge.second
        if right_edge is None:
            return left_edge.second
        
        return min(left_edge, right_edge, key=lambda edge: (edge.second.y, edge.second.x)).second


class BinTreeNode(SerializablePydanticModelWithPydanticFields):
    data: Any
    left: BinTreeNode | None = None
    right: BinTreeNode | None = None
    height: int = 0
    
    @property
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None
    
    @property
    def leftmost_node(self) -> BinTreeNode:
        res = self
        while res.left:
            res = res.left
        
        return res

    @property
    def rightmost_node(self) -> BinTreeNode:
        res = self
        while res.right:
            res = res.right
        
        return res
    
    @property
    def balance_factor(self) -> int:
        return (self.right.height if self.right else 0) - (self.left.height if self.left else 0)

    @classmethod
    def copy_contents_without_children(cls, source: BinTreeNode, destination: BinTreeNode) -> None:
        if not isinstance(source, cls) or not isinstance(destination, cls):
            raise TypeError(f"operands must be of type {cls}")
        if source is destination:
            return

        tmp_source_left, tmp_source_right = source.left, source.right
        tmp_dest_left, tmp_dest_right = destination.left, destination.right
        
        source.left, source.right = None, None
        destination.__dict__.update(source.__dict__)

        source.left, source.right = tmp_source_left, tmp_source_right
        destination.left, destination.right = tmp_dest_left, tmp_dest_right

    def traverse_preorder(self, node: BinTreeNode | None = None, nodes: list[BinTreeNode] | None = None) -> list[BinTreeNode]:
        if node is None:
            node = self
        if nodes is None:
            nodes = []
        
        nodes.append(node)

        if node.left:
            self.traverse_preorder(node.left, nodes)
        if node.right:
            self.traverse_preorder(node.right, nodes)
        
        return nodes

    def traverse_inorder(self, node: BinTreeNode | None = None, nodes: list[BinTreeNode] | None = None) -> list[BinTreeNode]:
        if node is None:
            node = self
        if nodes is None:
            nodes = []
        
        if node.left:
            self.traverse_inorder(node.left, nodes)
        
        nodes.append(node)

        if node.right:
            self.traverse_inorder(node.right, nodes)
        
        return nodes

    def traverse_postorder(self, node: BinTreeNode | None = None, nodes: list[BinTreeNode] | None = None) -> list[BinTreeNode]:
        if node is None:
            node = self
        if nodes is None:
            nodes = []
        
        if node.left:
            self.traverse_postorder(node.left, nodes)
        if node.right:
            self.traverse_postorder(node.right, nodes)
        
        nodes.append(node)
        return nodes

    def set_height(self) -> None:
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        self.height = max(left_height, right_height) + 1 if self.left or self.right else 0        

    def weak_equal(self, other: Any) -> bool:
        """Weak (non-recursive) equality that only checks whether the nodes are of the same type and their contents match."""
        return isinstance(other, self.__class__) and self.data == other.data

    def __eq__(self, other: Any) -> bool:
        """Strong (recursive) equality that checks whether the nodes are of the same type and their trees are equal."""
        return (
            isinstance(other, self.__class__)
            and self.weak_equal(other)
            and self.left == other.left
            and self.right == other.right
        )
    

class BinTree(SerializablePydanticModelWithPydanticFields):
    node_class: ClassVar[type] = BinTreeNode
    root: BinTreeNode | None = None

    @classmethod
    def from_iterable(cls, iterable: Iterable) -> BinTree:
        if isinstance(iterable, Generator):
            iterable = list(iterable)
        
        return cls(root=cls._from_iterable(iterable)) if iterable else cls(root=None)
    
    @classmethod
    def _from_iterable(cls, iterable: Iterable, left: int = 0, right: int | None = None) -> BinTreeNode:
        if right is None:
            right = len(iterable) - 1
        if left > right:
            return None
        
        mid = (left + right) // 2
        node = cls.node_class(data=iterable[mid])
        node.left = cls._from_iterable(iterable, left, mid-1)
        node.right = cls._from_iterable(iterable, mid+1, right)
        node.set_height()

        return node
    
    @classmethod
    def empty(cls) -> BinTree:
        return cls.from_iterable([])

    def traverse_preorder(self) -> Iterable[BinTreeNode]:
        return self.root.traverse_preorder() if self.root else []

    def traverse_inorder(self) -> Iterable[BinTreeNode]:
        return self.root.traverse_inorder() if self.root else []
    
    def traverse_postorder(self) -> Iterable[BinTreeNode]:
        return self.root.traverse_postorder() if self.root else []
    
    def leaves_preorder(self) -> Iterable[BinTreeNode]:
        return [node for node in self.traverse_preorder() if node.is_leaf]
    
    def leaves_inorder(self) -> Iterable[BinTreeNode]:
        return [node for node in self.traverse_inorder() if node.is_leaf]
    
    def leaves_postorder(self) -> Iterable[BinTreeNode]:
        return [node for node in self.traverse_postorder() if node.is_leaf]
    
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self.root == other.root


class AVLTree(BinTree):
    def insert(self, data: Any, starting_node: BinTreeNode | None = None) -> None:
        if starting_node is None:
            starting_node = self.root

        self.root = self._insert(data, starting_node)
    
    def delete(self, data: Any, starting_node: BinTreeNode | None = None) -> None:
        if starting_node is None:
            starting_node = self.root

        self.root = self._delete(data, starting_node)

    def _insert(self, data: Any, node: BinTreeNode | None = None) -> BinTreeNode:
        data_is_node = isinstance(data, self.node_class)
        if node is None:
            return data if data_is_node else BinTreeNode(data=data)
        
        value = data.data if data_is_node else data
        if value < node.data:
            node.left = self._insert(data, node.left)
        else:
            node.right = self._insert(data, node.right)
        
        node.set_height()
        return self.rebalance(node)

    def _delete(self, data: Any, node: BinTreeNode | None = None) -> BinTreeNode:
        if node is None:
            return None
        
        if data < node.data:
            node.left = self._delete(data, node.left)
        elif data > node.data:
            node.right = self._delete(data, node.right)
        else:
            if not node.left or not node.right:
                child = node.left if node.left else node.right
                node = None
                return child
            
            inorder_successor = node.right.leftmost_node
            BinTreeNode.copy_contents_without_children(inorder_successor, node)
            
            node.right = self._delete(inorder_successor.data, node.right)

        if node is None:
            return None

        node.set_height()
        return self.rebalance(node)
    
    def rebalance(self, node: BinTreeNode) -> BinTreeNode:
        balance_factor = node.balance_factor

        if balance_factor == -2:
            if node.left.balance_factor == 1:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)
            
            return self._rotate_right(node)
        if balance_factor == 2:
            if node.right.balance_factor == -1:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)

            return self._rotate_left(node)
        
        # No imbalance
        return node

    def _rotate_left(self, node: BinTreeNode) -> BinTreeNode:
        heavy_node = node.right
        swapped_subnode = heavy_node.left
        heavy_node.left = node
        node.right = swapped_subnode

        node.set_height()
        heavy_node.set_height()

        return heavy_node
    
    def _rotate_right(self, node: BinTreeNode) -> BinTreeNode:
        heavy_node = node.left
        swapped_subnode = heavy_node.right
        heavy_node.right = node
        node.left = swapped_subnode

        node.set_height()
        heavy_node.set_height()

        return heavy_node


class ThreadedBinTreeNode(BinTreeNode, extra=Extra.allow):
    left: ThreadedBinTreeNode | None = None
    right: ThreadedBinTreeNode | None = None
    prev: ThreadedBinTreeNode | int | None = None
    next: ThreadedBinTreeNode | int | None = None

    def model_dump(self, *args, **kwargs) -> dict[str, Any]:
        if kwargs.get('can_serialize', False):
            kwargs.pop('can_serialize')
            return BaseModel.model_dump(self, *args, **kwargs)
        
        return serialize_threaded_bin_tree_or_its_root(self, *args, **kwargs)


class ThreadedBinTree(AVLTree):
    node_class: ClassVar[type] = ThreadedBinTreeNode
    root: ThreadedBinTreeNode | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        if self.root and (isinstance(self.root.prev, int) or isinstance(self.root.next, int)):
            deserialize_threaded_bin_tree_root(self.root)

    def model_dump(self, *args, **kwargs):
        if kwargs.get('can_serialize', False):
            kwargs.pop('can_serialize')
            return BaseModel.model_dump(self, *args, **kwargs)
        
        return serialize_threaded_bin_tree_or_its_root(self, *args, **kwargs)

    @classmethod
    def from_iterable(cls, iterable: Iterable[ThreadedBinTreeNode], circular: bool = True) -> ThreadedBinTree:
        tree = super().from_iterable(iterable)
        nodes = tree.traverse_inorder()
        
        for i, node in enumerate(nodes):            
            node.prev = node.left if node.left else nodes[i-1]
            node.next = node.right if node.right else nodes[(i+1)%len(nodes)]
        
        if not circular and nodes:
            nodes[0].prev = None
            nodes[-1].next = None
        
        return tree


def serialize_threaded_bin_tree_or_its_root(root_or_tree: ThreadedBinTreeNode | ThreadedBinTree, *args, **kwargs) -> dict[str, Any]:
    """
        Serializes a threaded bin tree or its root. To correctly serialize potentially circular references to prev & next nodes, we store their inorder traversal indices instead.
    """
    copy = deepcopy(root_or_tree)
    nodes_inorder = copy.traverse_inorder() if isinstance(copy, ThreadedBinTreeNode) else copy.root.traverse_inorder()
    
    for i, node in enumerate(nodes_inorder):
        node.inorder_index = i
    
    for i, node in enumerate(nodes_inorder):
        node.prev = node.prev.inorder_index if node.prev is not None else node.prev
        node.next = node.next.inorder_index if node.next is not None else node.next

    return copy.model_dump(*args, **(kwargs | {'can_serialize': True}))


def deserialize_threaded_bin_tree_root(root: ThreadedBinTreeNode) -> None:
    """
        Deserializes a threaded bin tree's root, assuming that potentially circular references to prev & next nodes in its subtree are stored as their inorder traversal indices.
    """
    nodes_inorder = root.traverse_inorder()

    for i, node in enumerate(nodes_inorder):
        node.inorder_index = i
        node.prev_index = int(node.prev) if node.prev is not None else node.prev
        node.prev = nodes_inorder[int(node.prev)] if node.prev is not None else node.prev
        node.next_index = int(node.next) if node.next is not None else node.next
        node.next = nodes_inorder[int(node.next)] if node.next is not None else node.next


class PathDirection(str, Enum):
    left = "left"
    right = "right"
    prev = "prev"
    next = "next"
    stop = "stop"


class PointType(Enum):
    convex = 0
    reflex = 1
    left_supporting = 2
    right_supporting = 3

    @classmethod
    def by_nodes(cls, source: BinTreeNode, target: BinTreeNode) -> PointType:
        if target.prev is None:
            direction = Point.direction(source.data, target.data, target.next.data)
            if source.data.x < target.data.x:
                return cls.left_supporting if direction > 0 else cls.convex
            
            return cls.right_supporting if direction >= 0 else cls.reflex
        
        if target.next is None:
            direction = Point.direction(source.data, target.data, target.prev.data)
            if source.data.x < target.data.x:
                return cls.left_supporting if direction >= 0 else cls.reflex
            
            return cls.right_supporting if direction > 0 else cls.convex
        
        return cls.by_points(source.data, target.data, target.prev.data, target.next.data)

    @classmethod
    def by_points(cls, source: BinTreeNode, target: BinTreeNode, left: BinTreeNode, right: BinTreeNode) -> PointType:
        def polar_angle(point):
            """[0, 2*pi) polar angle in coordinate system with axis target -> source (rotated against x axis by rot)"""
            rot = Point.nonnegative_polar_angle(source, target)
            angle = Point.nonnegative_polar_angle(point, target)
            return angle - rot + (2 * pi if angle < rot else 0)
        
        angles = polar_angle(left), polar_angle(right)
        angle1 = min(angles)
        angle2 = max(angles)

        convex_or_reflex = 0 < angle1 <= pi <= angle2 < 2 * pi

        # Convex
        if convex_or_reflex and angle2 < angle1 + pi:
            return cls.convex
        
        # Reflex
        if convex_or_reflex and angle2 > angle1 + pi:
            return cls.reflex

        # Left supporting
        if 0 <= angle1 < angle2 < pi:
            return cls.left_supporting
        
        # Right supporting
        if angle1 == 0:
            angle1 = 2 * pi
            angle1, angle2 = angle2, angle1
        
        if pi < angle1 < angle2 <= 2 * pi:
            return cls.right_supporting
        
        raise ValueError