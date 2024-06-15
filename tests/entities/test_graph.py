import pytest
from algogears.core import Graph, GraphEdge, Point


def test_graph_edge_creation():
    edge = GraphEdge(first=Point.new(1, 1), second=Point.new(2, 2), weight=1)

    assert edge.first == Point.new(1, 1)
    assert edge.second == Point.new(2, 2)
    assert edge.weight == 1


def test_graph_edge_hash():
    edge1 = GraphEdge(first=Point.new(1, 1), second=Point.new(2, 2), weight=1)
    edge2 = GraphEdge(first=Point.new(1, 1), second=Point.new(2, 2), weight=2)

    assert hash(edge1) == hash(edge2)


def test_graph_creation_correct():
    nodes = [Point.new(1, 1), Point.new(2, 2)]
    edges = [GraphEdge(first=nodes[0], second=nodes[1]), GraphEdge(first=nodes[0], second=nodes[1], weight=2)]
    
    graph = Graph(nodes=nodes, edges=edges)
    assert graph.nodes == set(nodes)
    assert graph.edges == set(edges)


def test_graph_creation_incorrect():
    nodes = [Point.new(1, 1), Point.new(2, 2)]
    edges = [GraphEdge(first=Point.new(100, 100), second=nodes[1])]

    with pytest.raises(ValueError):
        _ = Graph(nodes=nodes, edges=edges)


def test_graph_add_node():
    graph = Graph()

    new_node = Point.new(1, 1)
    graph.add_node(new_node)

    assert graph.nodes == {new_node}


def test_graph_add_edge():
    nodes = [Point.new(1, 1), Point.new(2, 2)]
    graph = Graph(nodes=nodes)

    new_edge = GraphEdge(first=nodes[0], second=nodes[1])
    graph.add_edge(new_edge)

    assert graph.edges == {new_edge}