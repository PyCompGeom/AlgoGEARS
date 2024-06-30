import pytest
from algogears.core import Point, PlanarStraightLineGraph, PlanarStraightLineGraphEdge, OrientedPlanarStraightLineGraph, OrientedPlanarStraightLineGraphEdge


def test_oriented_planar_straight_line_graph_creation_default_correct():
    planar_straight_line_graph = OrientedPlanarStraightLineGraph()
    assert planar_straight_line_graph.nodes == set()
    assert planar_straight_line_graph.edges == set()


def test_oriented_planar_straight_line_graph_creation_correct():
    nodes = [Point.new(1, 1), Point.new(2, 2)]
    edges = [OrientedPlanarStraightLineGraphEdge(first=nodes[0], second=nodes[1]), OrientedPlanarStraightLineGraphEdge(first=nodes[0], second=nodes[1], weight=2)]
    
    planar_straight_line_graph = OrientedPlanarStraightLineGraph(nodes=nodes, edges=edges)
    assert planar_straight_line_graph.nodes == set(nodes)
    assert planar_straight_line_graph.edges == set(edges)


def test_oriented_planar_straight_line_graph_add_node_correct():
    planar_straight_line_graph = OrientedPlanarStraightLineGraph()

    new_node = Point.new(1, 1)
    planar_straight_line_graph.add_node(new_node)

    assert planar_straight_line_graph.nodes == {new_node}


def test_oriented_planar_straight_line_graph_add_node_incorrect_type():
    planar_straight_line_graph = OrientedPlanarStraightLineGraph()

    with pytest.raises(TypeError):
        planar_straight_line_graph.add_node(42)


def test_oriented_planar_straight_line_graph_add_edge_correct():
    nodes = [Point.new(1, 1), Point.new(2, 2)]
    planar_straight_line_graph = OrientedPlanarStraightLineGraph(nodes=nodes)

    new_edge = OrientedPlanarStraightLineGraphEdge(first=nodes[0], second=nodes[1])
    planar_straight_line_graph.add_edge(new_edge)

    assert planar_straight_line_graph.edges == {new_edge}


def test_oriented_planar_straight_line_graph_add_edge_incorrect_type():
    planar_straight_line_graph = OrientedPlanarStraightLineGraph()

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
    inward_edges = [OrientedPlanarStraightLineGraphEdge(first=node, second=nodes[0]) for node in nodes[1:5]]
    outward_edges = [OrientedPlanarStraightLineGraphEdge(first=nodes[0], second=node) for node in nodes[5:]]
    edges = inward_edges + outward_edges
    planar_straight_line_graph = OrientedPlanarStraightLineGraph(nodes=nodes, edges=edges)    
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
    inward_edges = [OrientedPlanarStraightLineGraphEdge(first=node, second=nodes[0]) for node in nodes[1:5]]
    outward_edges = [OrientedPlanarStraightLineGraphEdge(first=nodes[0], second=node) for node in nodes[5:]]
    edges = inward_edges + outward_edges
    planar_straight_line_graph = OrientedPlanarStraightLineGraph(nodes=nodes, edges=edges)
    target_node = nodes[0]

    assert planar_straight_line_graph.outward_edges(target_node) == outward_edges


def test_oriented_planar_straight_line_graph_eq_edges_with_same_nodes_in_same_direction():
    graph1 = OrientedPlanarStraightLineGraph(nodes={Point.new(1, 1), Point.new(2, 2)}, edges={OrientedPlanarStraightLineGraphEdge(first=Point.new(1, 1), second=Point.new(2, 2), weight=1.5)})
    graph2 = OrientedPlanarStraightLineGraph(nodes={Point.new(1, 1), Point.new(2, 2)}, edges={OrientedPlanarStraightLineGraphEdge(first=Point.new(1, 1), second=Point.new(2, 2), weight=1.5)})

    assert graph1 == graph2


def test_oriented_planar_straight_line_graph_non_eq_edges_with_same_nodes_in_different_directions():
    graph1 = OrientedPlanarStraightLineGraph(nodes={Point.new(1, 1), Point.new(2, 2)}, edges={OrientedPlanarStraightLineGraphEdge(first=Point.new(1, 1), second=Point.new(2, 2), weight=1.5)})
    graph2 = OrientedPlanarStraightLineGraph(nodes={Point.new(1, 1), Point.new(2, 2)}, edges={OrientedPlanarStraightLineGraphEdge(first=Point.new(2, 2), second=Point.new(1, 1), weight=1.5)})

    assert graph1 != graph2


def test_oriented_planar_straight_line_graph_from_planar_straight_line_graph():
    nodes = [
        Point.new(6, 0),
        Point.new(10, 0),
        Point.new(0, 1),
        Point.new(4, 3),
        Point.new(2, 4),
        Point.new(1, 5),
        Point.new(2, 6),
        Point.new(4, 6),
        Point.new(8, 6),
        Point.new(10, 7),
        Point.new(5, 9),
    ]
    edges = [
        PlanarStraightLineGraphEdge(first=nodes[0], second=nodes[2]),
        PlanarStraightLineGraphEdge(first=nodes[0], second=nodes[3]),
        PlanarStraightLineGraphEdge(first=nodes[0], second=nodes[8]),
        PlanarStraightLineGraphEdge(first=nodes[1], second=nodes[8]),
        PlanarStraightLineGraphEdge(first=nodes[2], second=nodes[3]),
        PlanarStraightLineGraphEdge(first=nodes[2], second=nodes[5]),
        PlanarStraightLineGraphEdge(first=nodes[3], second=nodes[7]),
        PlanarStraightLineGraphEdge(first=nodes[3], second=nodes[8]),
        PlanarStraightLineGraphEdge(first=nodes[4], second=nodes[5]),
        PlanarStraightLineGraphEdge(first=nodes[4], second=nodes[7]),
        PlanarStraightLineGraphEdge(first=nodes[5], second=nodes[6]),
        PlanarStraightLineGraphEdge(first=nodes[6], second=nodes[7]),
        PlanarStraightLineGraphEdge(first=nodes[6], second=nodes[10]),
        PlanarStraightLineGraphEdge(first=nodes[7], second=nodes[8]),
        PlanarStraightLineGraphEdge(first=nodes[7], second=nodes[10]),
        PlanarStraightLineGraphEdge(first=nodes[9], second=nodes[10]),
    ]
    oriented_edges = [OrientedPlanarStraightLineGraphEdge(first=edge.first, second=edge.second) for edge in edges]

    pslg = PlanarStraightLineGraph(nodes=nodes, edges=edges)
    oriented_pslg = OrientedPlanarStraightLineGraph(nodes=nodes, edges=oriented_edges)

    assert oriented_pslg == OrientedPlanarStraightLineGraph.from_planar_straight_line_graph(pslg)
