import pytest
from algogears.core import Point, PlanarStraightLineGraph, PlanarStraightLineGraphEdge


def test_planar_straight_line_graph_edge_creation():
    edge = PlanarStraightLineGraphEdge(first=Point.new(1, 1), second=Point.new(2, 2), weight=1)

    assert edge.first == Point.new(1, 1)
    assert edge.second == Point.new(2, 2)
    assert edge.weight == 1


def test_planar_straight_line_grap_edge_hash():
    edge1 = PlanarStraightLineGraphEdge(first=Point.new(1, 1), second=Point.new(2, 2), weight=1)
    edge2 = PlanarStraightLineGraphEdge(first=Point.new(1, 1), second=Point.new(2, 2), weight=1)

    assert hash(edge1) == hash(edge2)


def test_planar_straight_line_grap_creation_default_correct():
    planar_straight_line_grap = PlanarStraightLineGraph()
    assert planar_straight_line_grap.nodes == set()
    assert planar_straight_line_grap.edges == set()


def test_planar_straight_line_grap_creation_correct():
    nodes = [Point.new(1, 1), Point.new(2, 2)]
    edges = [PlanarStraightLineGraphEdge(first=nodes[0], second=nodes[1]), PlanarStraightLineGraphEdge(first=nodes[0], second=nodes[1], weight=2)]
    
    planar_straight_line_grap = PlanarStraightLineGraph(nodes=nodes, edges=edges)
    assert planar_straight_line_grap.nodes == set(nodes)
    assert planar_straight_line_grap.edges == set(edges)


def test_planar_straight_line_grap_creation_incorrect_nodes_in_edge():
    nodes = [Point.new(1, 1), Point.new(2, 2)]
    edges = [PlanarStraightLineGraphEdge(first=Point.new(100, 100), second=nodes[1])]

    with pytest.raises(ValueError):
        _ = PlanarStraightLineGraph(nodes=nodes, edges=edges)


def test_planar_straight_line_grap_add_node_correct():
    planar_straight_line_grap = PlanarStraightLineGraph()

    new_node = Point.new(1, 1)
    planar_straight_line_grap.add_node(new_node)

    assert planar_straight_line_grap.nodes == {new_node}


def test_planar_straight_line_grap_add_node_incorrect_type():
    planar_straight_line_grap = PlanarStraightLineGraph()

    with pytest.raises(TypeError):
        planar_straight_line_grap.add_node(42)


def test_planar_straight_line_grap_add_edge_correct():
    nodes = [Point.new(1, 1), Point.new(2, 2)]
    planar_straight_line_grap = PlanarStraightLineGraph(nodes=nodes)

    new_edge = PlanarStraightLineGraphEdge(first=nodes[0], second=nodes[1])
    planar_straight_line_grap.add_edge(new_edge)

    assert planar_straight_line_grap.edges == {new_edge}


def test_planar_straight_line_grap_add_edge_incorrect_type():
    planar_straight_line_grap = PlanarStraightLineGraph()

    with pytest.raises(TypeError):
        planar_straight_line_grap.add_edge(42)


def test_graph_add_edge_incorrect_nodes_in_edge():
    nodes = [Point.new(1, 1), Point.new(2, 2)]
    graph = PlanarStraightLineGraph(nodes=nodes)

    with pytest.raises(ValueError):
        new_edge = PlanarStraightLineGraphEdge(first=Point.new(100, 100), second=Point.new(200, 200))
        graph.add_edge(new_edge)