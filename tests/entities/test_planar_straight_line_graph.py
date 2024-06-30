import pytest
from algogears.core import Point, PlanarStraightLineGraph, PlanarStraightLineGraphEdge


def test_planar_straight_line_graph_creation_default_correct():
    planar_straight_line_graph = PlanarStraightLineGraph()
    assert planar_straight_line_graph.nodes == set()
    assert planar_straight_line_graph.edges == set()


def test_planar_straight_line_graph_creation_correct():
    nodes = [Point.new(1, 1), Point.new(2, 2)]
    edges = [PlanarStraightLineGraphEdge(first=nodes[0], second=nodes[1]), PlanarStraightLineGraphEdge(first=nodes[0], second=nodes[1], weight=2)]
    
    planar_straight_line_graph = PlanarStraightLineGraph(nodes=nodes, edges=edges)
    assert planar_straight_line_graph.nodes == set(nodes)
    assert planar_straight_line_graph.edges == set(edges)


def test_planar_straight_line_graph_add_node_correct():
    planar_straight_line_graph = PlanarStraightLineGraph()

    new_node = Point.new(1, 1)
    planar_straight_line_graph.add_node(new_node)

    assert planar_straight_line_graph.nodes == {new_node}


def test_planar_straight_line_graph_add_node_incorrect_type():
    planar_straight_line_graph = PlanarStraightLineGraph()

    with pytest.raises(TypeError):
        planar_straight_line_graph.add_node(42)


def test_planar_straight_line_graph_add_edge_correct():
    nodes = [Point.new(1, 1), Point.new(2, 2)]
    planar_straight_line_graph = PlanarStraightLineGraph(nodes=nodes)

    new_edge = PlanarStraightLineGraphEdge(first=nodes[0], second=nodes[1])
    planar_straight_line_graph.add_edge(new_edge)

    assert planar_straight_line_graph.edges == {new_edge}


def test_planar_straight_line_graph_add_edge_incorrect_type():
    planar_straight_line_graph = PlanarStraightLineGraph()

    with pytest.raises(TypeError):
        planar_straight_line_graph.add_edge(42)


def test_graph_eq_edges_with_same_nodes_in_same_direction():
    graph1 = PlanarStraightLineGraph(nodes={Point.new(1, 1), Point.new(2, 2)}, edges={PlanarStraightLineGraphEdge(first=Point.new(1, 1), second=Point.new(2, 2), weight=1.5)})
    graph2 = PlanarStraightLineGraph(nodes={Point.new(1, 1), Point.new(2, 2)}, edges={PlanarStraightLineGraphEdge(first=Point.new(1, 1), second=Point.new(2, 2), weight=1.5)})

    assert graph1 == graph2


def test_graph_eq_edges_with_same_nodes_in_different_directions():
    graph1 = PlanarStraightLineGraph(nodes={Point.new(1, 1), Point.new(2, 2)}, edges={PlanarStraightLineGraphEdge(first=Point.new(1, 1), second=Point.new(2, 2), weight=1.5)})
    graph2 = PlanarStraightLineGraph(nodes={Point.new(1, 1), Point.new(2, 2)}, edges={PlanarStraightLineGraphEdge(first=Point.new(2, 2), second=Point.new(1, 1), weight=1.5)})

    assert graph1 == graph2