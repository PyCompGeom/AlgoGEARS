import pytest
from algogears.core import Graph, GraphEdge, PlanarStraightLineGraph, PlanarStraightLineGraphEdge


def test_graph_edge_creation():
    edge = GraphEdge(first=1, second=2, weight=1)

    assert edge.first == 1
    assert edge.second == 2
    assert edge.weight == 1


def test_graph_edge_hash():
    edge1 = GraphEdge(first=1, second=2, weight=1)
    edge2 = GraphEdge(first=1, second=2, weight=1)

    assert hash(edge1) == hash(edge2)


def test_graph_creation_default_correct():
    graph = Graph()
    assert graph.nodes == set()
    assert graph.edges == set()


def test_graph_creation_correct():
    nodes = [1, 2]
    edges = [GraphEdge(first=1, second=2), GraphEdge(first=1, second=2, weight=2)]
    
    graph = Graph(nodes=nodes, edges=edges)
    assert graph.nodes == set(nodes)
    assert graph.edges == set(edges)


def test_graph_creation_incorrect_nodes_in_edge():
    nodes = [1, 2]
    edges = [GraphEdge(first=100, second=2)]

    with pytest.raises(ValueError):
        _ = Graph(nodes=nodes, edges=edges)


def test_graph_add_node_correct():
    graph = Graph()
    graph.add_node(1)

    assert graph.nodes == {1}


def test_graph_add_edge_correct():
    nodes = [1, 2]
    graph = Graph(nodes=nodes)

    new_edge = GraphEdge(first=1, second=2)
    graph.add_edge(new_edge)

    assert graph.edges == {new_edge}


def test_graph_add_edge_incorrect_type():
    graph = Graph()
    
    with pytest.raises(TypeError):
        graph.add_edge(42)


def test_graph_add_edge_incorrect_nodes_in_edge():
    nodes = [1, 2]
    graph = Graph(nodes=nodes)

    with pytest.raises(ValueError):
        new_edge = GraphEdge(first=100, second=200)
        graph.add_edge(new_edge)