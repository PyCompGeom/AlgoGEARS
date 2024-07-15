from __future__ import annotations
from copy import deepcopy
from typing import Iterable, ClassVar
from algogears.core import Point, ThreadedBinTree, ThreadedBinTreeNode, PlanarStraightLineGraph, OrientedPlanarStraightLineGraph, OrientedPlanarStraightLineGraphEdge, Turn, PathDirection


class ChainsThreadedBinTreeNode(ThreadedBinTreeNode):
    data: list[OrientedPlanarStraightLineGraphEdge]
    left: ChainsThreadedBinTreeNode | None = None
    right: ChainsThreadedBinTreeNode | None = None
    prev: ChainsThreadedBinTreeNode | int | None = None
    next: ChainsThreadedBinTreeNode | int | None = None

    @property
    def chain(self) -> list[OrientedPlanarStraightLineGraphEdge]:
        return self.data
    
    @chain.setter
    def chain(self, value: list[OrientedPlanarStraightLineGraphEdge]) -> None:
        self.data = value
    
    @chain.deleter
    def chain(self) -> None:
        del self.data

    def turn(self, point: Point) -> Turn:
        for edge in self.chain:
            if edge.first.y == point.y == edge.second.y:
                    if point.x < edge.first.x:
                        return Turn.LEFT
                    if point.x > edge.second.x:
                        return Turn.RIGHT
                    
                    return Turn.STRAIGHT
            
            if edge.first.y <= point.y <= edge.second.y:                
                return Turn(edge.first, edge.second, point)
    

class ChainsThreadedBinTree(ThreadedBinTree):
    node_class: ClassVar[type] = ChainsThreadedBinTreeNode
    root: ChainsThreadedBinTreeNode | None = None


def chain(planar_straight_line_graph: PlanarStraightLineGraph, point: Point):
    nodes_bottom_to_top = sorted(planar_straight_line_graph.nodes, key=lambda node: (node.y, node.x))
    yield nodes_bottom_to_top

    oriented_planar_straight_line_graph = OrientedPlanarStraightLineGraph.from_planar_straight_line_graph(planar_straight_line_graph)
    yield deepcopy(oriented_planar_straight_line_graph)

    yield [oriented_planar_straight_line_graph.inward_edges(node) for node in nodes_bottom_to_top]
    yield [oriented_planar_straight_line_graph.outward_edges(node) for node in nodes_bottom_to_top]

    if not oriented_planar_straight_line_graph.is_regular():
        oriented_planar_straight_line_graph.regularize()
    
    yield deepcopy(oriented_planar_straight_line_graph)

    for edge in oriented_planar_straight_line_graph.edges:
        edge.weight = 1
    
    yield deepcopy(oriented_planar_straight_line_graph)

    nodes_bottom_to_top = sorted(oriented_planar_straight_line_graph.nodes, key=lambda node: (node.y, node.x))
    balance_bottom_to_top(oriented_planar_straight_line_graph, nodes_bottom_to_top)
    yield deepcopy(oriented_planar_straight_line_graph)

    nodes_top_to_bottom = reversed(nodes_bottom_to_top)
    balance_top_to_bottom(oriented_planar_straight_line_graph, nodes_top_to_bottom)
    yield deepcopy(oriented_planar_straight_line_graph)

    monotone_chains = construct_monotone_chains(oriented_planar_straight_line_graph, nodes_bottom_to_top)
    yield monotone_chains

    chain_bin_tree = ChainsThreadedBinTree.from_iterable(monotone_chains)
    yield chain_bin_tree

    search_path, chains_target_point_is_between = search(point, chain_bin_tree, monotone_chains)
    yield search_path, chains_target_point_is_between
    

def balance_bottom_to_top(oriented_planar_straight_line_graph: OrientedPlanarStraightLineGraph, nodes: Iterable[Point]) -> None:
    for node in nodes:
        inward_edges = oriented_planar_straight_line_graph.inward_edges(node)
        outward_edges = oriented_planar_straight_line_graph.outward_edges(node)

        weight_in = sum(edge.weight for edge in inward_edges)
        weight_out = sum(edge.weight for edge in outward_edges)

        if outward_edges and weight_in > weight_out:
            outward_edges[0].weight += weight_in - weight_out


def balance_top_to_bottom(oriented_planar_straight_line_graph: OrientedPlanarStraightLineGraph, nodes: Iterable[Point]) -> None:
    for node in nodes:
        inward_edges = oriented_planar_straight_line_graph.inward_edges(node)
        outward_edges = oriented_planar_straight_line_graph.outward_edges(node)

        weight_in = sum(edge.weight for edge in inward_edges)
        weight_out = sum(edge.weight for edge in outward_edges)

        if inward_edges and weight_out > weight_in:
            inward_edges[0].weight += weight_out - weight_in


def construct_monotone_chains(oriented_planar_straight_line_graph: OrientedPlanarStraightLineGraph, nodes: Iterable[Point]) -> list[list[OrientedPlanarStraightLineGraphEdge]]:
    monotone_chains = []
    while (starting_edge := leftmost_available_outward_edge(nodes[0], oriented_planar_straight_line_graph)) is not None:
        monotone_chains.append([starting_edge])

        node = starting_edge.second
        while node is not nodes[-1]:
            edge = leftmost_available_outward_edge(node, oriented_planar_straight_line_graph)
            monotone_chains[-1].append(edge)
            edge.weight -= 1
            node = edge.second
        
        starting_edge.weight -= 1
    
    return monotone_chains


def leftmost_available_outward_edge(node: Point, oriented_planar_straight_line_graph: OrientedPlanarStraightLineGraph) -> OrientedPlanarStraightLineGraphEdge | None:
    for edge in oriented_planar_straight_line_graph.outward_edges(node):
        if edge.weight > 0:
            return edge
    
    return None


def search(point: Point, chain_bin_tree: ChainsThreadedBinTree, monotone_chains: list[list[OrientedPlanarStraightLineGraphEdge]]) -> tuple[list[ChainsThreadedBinTreeNode], tuple[OrientedPlanarStraightLineGraphEdge, OrientedPlanarStraightLineGraphEdge]]:
    chain_node = chain_bin_tree.root
    search_path = []
    while not chain_node.is_leaf:
        turn = chain_node.turn(point)
        if turn == Turn.STRAIGHT:
            return search_path, (chain_node.chain, chain_node.chain)
        elif turn == Turn.LEFT:
            if chain_node is monotone_chains[0]:
                return search_path, (None, chain_node.chain)

            # For floor-based chain trees, here we should go to prev node, not left
            if chain_node.left is None:
                break

            search_path.append(PathDirection.left)
            chain_node = chain_node.left
        else:
            if chain_node is monotone_chains[-1]:
                return search_path, (chain_node.chain, None)

            # For ceil-based chain trees, here we should go to next node, not right
            if chain_node.right is None:
                break

            search_path.append(PathDirection.right)
            chain_node = chain_node.right

    turn = chain_node.turn(point)
    if turn == Turn.LEFT:
        search_path.append(PathDirection.prev)
        return search_path, (chain_node.prev.chain, chain_node.chain)
    if turn == Turn.RIGHT:
        search_path.append(PathDirection.next)
        return search_path, (chain_node.chain, chain_node.next.chain)
    
    return search_path, (chain_node.chain, chain_node.chain)