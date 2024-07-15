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


def test_oriented_planar_straight_line_graph_node_inward_edges():
    nodes = [
        Point.new(3, 3),
        Point.new(1, 3),
        Point.new(2, 1),
        Point.new(3, 1),
        Point.new(5, 2),
        Point.new(0, 4),
        Point.new(3, 5),
        Point.new(5, 5),
        Point.new(5, 3),
    ]
    inward_edges = [
        PlanarStraightLineGraphEdge(first=nodes[1], second=nodes[0]),
        PlanarStraightLineGraphEdge(first=nodes[0], second=nodes[2]),
        PlanarStraightLineGraphEdge(first=nodes[3], second=nodes[0]),
        PlanarStraightLineGraphEdge(first=nodes[0], second=nodes[4]),
    ]
    outward_edges = [PlanarStraightLineGraphEdge(first=nodes[0], second=node) for node in nodes[5:]]
    edges = inward_edges + outward_edges
    planar_straight_line_graph = PlanarStraightLineGraph(nodes=nodes, edges=edges)    
    target_node = nodes[0]

    assert planar_straight_line_graph.inward_edges(target_node) == inward_edges


def test_oriented_planar_straight_line_graph_node_outward_edges():
    nodes = [
        Point.new(3, 3),
        Point.new(1, 3),
        Point.new(2, 1),
        Point.new(3, 1),
        Point.new(5, 2),
        Point.new(0, 4),
        Point.new(3, 5),
        Point.new(5, 5),
        Point.new(5, 3),
    ]
    inward_edges = [PlanarStraightLineGraphEdge(first=node, second=nodes[0]) for node in nodes[1:5]]
    outward_edges = [
        PlanarStraightLineGraphEdge(first=nodes[0], second=nodes[5]),
        PlanarStraightLineGraphEdge(first=nodes[6], second=nodes[0]),
        PlanarStraightLineGraphEdge(first=nodes[0], second=nodes[7]),
        PlanarStraightLineGraphEdge(first=nodes[8], second=nodes[0]),
    ]
    edges = inward_edges + outward_edges
    planar_straight_line_graph = PlanarStraightLineGraph(nodes=nodes, edges=edges)
    target_node = nodes[0]

    assert planar_straight_line_graph.outward_edges(target_node) == outward_edges


def test_graph_eq_edges_with_same_nodes_in_same_direction():
    graph1 = PlanarStraightLineGraph(nodes={Point.new(1, 1), Point.new(2, 2)}, edges={PlanarStraightLineGraphEdge(first=Point.new(1, 1), second=Point.new(2, 2), weight=1.5)})
    graph2 = PlanarStraightLineGraph(nodes={Point.new(1, 1), Point.new(2, 2)}, edges={PlanarStraightLineGraphEdge(first=Point.new(1, 1), second=Point.new(2, 2), weight=1.5)})

    assert graph1 == graph2


def test_graph_eq_edges_with_same_nodes_in_different_directions():
    graph1 = PlanarStraightLineGraph(nodes={Point.new(1, 1), Point.new(2, 2)}, edges={PlanarStraightLineGraphEdge(first=Point.new(1, 1), second=Point.new(2, 2), weight=1.5)})
    graph2 = PlanarStraightLineGraph(nodes={Point.new(1, 1), Point.new(2, 2)}, edges={PlanarStraightLineGraphEdge(first=Point.new(2, 2), second=Point.new(1, 1), weight=1.5)})

    assert graph1 == graph2