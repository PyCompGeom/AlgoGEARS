from __future__ import annotations
from math import inf
from typing import Iterable, ClassVar
from pydantic import Field
from algogears.core import PlanarStraightLineGraphPlaneSweep, Point, PlanarStraightLineGraph, PlanarStraightLineGraphEdge, SerializablePydanticModelWithPydanticFields, Turn, BinTree, BinTreeNode, ThreadedBinTree, ThreadedBinTreeNode, PathDirection


class Slab(SerializablePydanticModelWithPydanticFields):
    y_min: float = -inf
    y_max: float = inf
    points: list[Point] = Field(default_factory=list)
    edges: list[PlanarStraightLineGraphEdge] = Field(default_factory=list)
    inserted_edges: list[PlanarStraightLineGraphEdge] = Field(default_factory=list)
    deleted_edges: list[PlanarStraightLineGraphEdge] = Field(default_factory=list)


class SlabPlaneSweep(PlanarStraightLineGraphPlaneSweep):
    swept_objects: list[PlanarStraightLineGraphEdge] = Field(default_factory=list)

    def sweep(self) -> list[Slab]:
        slabs = [Slab(y_max=self.event_points[0].y)]
        slab_points = []
        slab_inserted_edges = []
        slab_deleted_edges = []

        for i, point in enumerate(self.event_points):
            node_inserted_edges = self.graph.outward_edges(point)
            node_deleted_edges = self.graph.inward_edges(point)

            slab_points.append(point)
            slab_inserted_edges.extend(node_inserted_edges)
            slab_deleted_edges.extend(node_deleted_edges)

            insert_at = self.edges_insertion_index_in_swept_edges(node_inserted_edges, point)
            delete_at = self.edges_deletion_index_in_swept_edges(node_deleted_edges, point)

            self.delete_edges_from_swept_edges(node_deleted_edges, delete_at=delete_at)
            self.insert_edges_to_swept_edges(node_inserted_edges, insert_at=insert_at)

            is_last_point = point is self.event_points[-1]
            if is_last_point or point.y != self.event_points[i+1].y:
                y_min = point.y
                y_max = inf if is_last_point else self.event_points[i+1].y

                slabs.append(Slab(y_min=y_min, y_max=y_max, points=slab_points, edges=self.swept_edges[:], inserted_edges=slab_inserted_edges, deleted_edges=slab_deleted_edges))

                slab_points = []
                slab_inserted_edges = []
                slab_deleted_edges = []
        
        return slabs
    
    def edges_insertion_index_in_swept_edges(self, edges: list[PlanarStraightLineGraphEdge], point: Point) -> int:
        try:
            return self.swept_edges.index(edges[0])
        except (IndexError, ValueError):
            return self.edges_insertion_index_in_swept_edges_by_point(point)
    
    def edges_insertion_index_in_swept_edges_by_point(self, point: Point) -> int:
        for i, edge in enumerate(self.swept_edges):
            turn = Turn(edge.vertically_min_node, edge.vertically_max_node, point)
            if turn == Turn.LEFT or turn == Turn.STRAIGHT:
                return i
        
        return len(self.swept_edges)
    
    def edges_deletion_index_in_swept_edges(self, edges: list[PlanarStraightLineGraphEdge], point: Point) -> int:
        try:
            return self.swept_edges.index(edges[0]) if edges else 0
        except (IndexError, ValueError):
            return self.edges_deletion_index_in_swept_edges_by_point(point)
    
    def edges_deletion_index_in_swept_edges_by_point(self, point: Point) -> int:
        for i, edge in enumerate(self.swept_edges):
            if Turn(edge.vertically_min_node, edge.vertically_max_node, point) == Turn.STRAIGHT:
                return i
        
        return len(self.swept_edges)


class SlabBinTreeNode(BinTreeNode):
    data: Slab
    left: SlabBinTreeNode | None = None
    right: SlabBinTreeNode | None = None

    @property
    def slab(self) -> Slab:
        return self.data
    
    @slab.setter
    def slab(self, value: Slab) -> None:
        self.data = value
    
    @slab.deleter
    def slab(self) -> None:
        del self.data
    
    def search_direction(self, value: Point) -> PathDirection:
        if value.y < self.slab.y_min:
            return PathDirection.left
        if value.y >= self.slab.y_max:
            return PathDirection.right
        
        return PathDirection.stop


class SlabBinTree(BinTree):
    node_class: ClassVar[type] = SlabBinTreeNode
    root: SlabBinTreeNode | None = None


class PlanarStraightLineGraphEdgeThreadedBinTreeNode(ThreadedBinTreeNode):
    data: PlanarStraightLineGraphEdge
    left: PlanarStraightLineGraphEdgeThreadedBinTreeNode | None = None
    right: PlanarStraightLineGraphEdgeThreadedBinTreeNode | None = None
    prev: PlanarStraightLineGraphEdgeThreadedBinTreeNode | int | None = None
    next: PlanarStraightLineGraphEdgeThreadedBinTreeNode | int | None = None

    @property
    def edge(self) -> PlanarStraightLineGraphEdge:
        return self.data
    
    @edge.setter
    def edge(self, value: PlanarStraightLineGraphEdge) -> None:
        self.data = value
    
    @edge.deleter
    def edge(self) -> None:
        del self.data
    
    def search_direction(self, value: Point) -> PathDirection:
        turn = Turn(self.edge.vertically_min_node, self.edge.vertically_max_node, value)
        if turn == Turn.LEFT:
            return PathDirection.left
        if turn == Turn.RIGHT:
            return PathDirection.right
        
        return PathDirection.stop


class PlanarStraightLineGraphEdgeThreadedBinTree(ThreadedBinTree):
    node_class: ClassVar[type] = PlanarStraightLineGraphEdgeThreadedBinTreeNode
    root: PlanarStraightLineGraphEdgeThreadedBinTreeNode | None = None


def slab(planar_straight_line_graph: PlanarStraightLineGraph, point: Point):
    nodes_bottom_to_top = sorted(planar_straight_line_graph.nodes, key=lambda node: (node.y, node.x))
    yield nodes_bottom_to_top

    sweep = SlabPlaneSweep(graph=planar_straight_line_graph, event_points=nodes_bottom_to_top)
    slabs = sweep.sweep()
    yield slabs

    yield slabs
    yield slabs
    yield slabs

    slab_tree = SlabBinTree.from_iterable(slabs)
    yield slab_tree

    slab_search_path, node = slab_tree.search(point)
    yield slab_search_path, node.slab

    edge_tree = PlanarStraightLineGraphEdgeThreadedBinTree.from_iterable(node.slab.edges)
    yield edge_tree

    edge_search_path, (left_edge_node, right_edge_node) = edge_tree.search_neighbors(point)
    yield edge_search_path, (left_edge_node.edge if left_edge_node else None, right_edge_node.edge if right_edge_node else None)