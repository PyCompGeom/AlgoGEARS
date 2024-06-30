import pytest
from algogears.core import OrientedGraph, OrientedGraphEdge


def test_oriented_graph_creation_default_correct():
    graph = OrientedGraph()
    assert graph.nodes == set()
    assert graph.edges == set()


def test_oriented_graph_creation_correct():
    nodes = [1, 2]
    edges = [OrientedGraphEdge(first=1, second=2), OrientedGraphEdge(first=1, second=2, weight=2)]
    
    graph = OrientedGraph(nodes=nodes, edges=edges)
    assert graph.nodes == set(nodes)
    assert graph.edges == set(edges)


def test_oriented_graph_add_node_correct():
    graph = OrientedGraph()
    graph.add_node(1)

    assert graph.nodes == {1}


def test_oriented_graph_add_edge_correct():
    nodes = [1, 2]
    graph = OrientedGraph(nodes=nodes)

    new_edge = OrientedGraphEdge(first=1, second=2)
    graph.add_edge(new_edge)

    assert graph.edges == {new_edge}


def test_oriented_graph_add_edge_with_new_nodes_correct():
    nodes = [1, 2]
    graph = OrientedGraph(nodes=nodes)

    new_edge = OrientedGraphEdge(first=3, second=4)
    graph.add_edge(new_edge)

    assert graph.edges == {new_edge}


def test_oriented_graph_add_edge_incorrect_type():
    graph = OrientedGraph()
    
    with pytest.raises(TypeError):
        graph.add_edge(42)


def test_oriented_graph_eq_edges_with_same_nodes_in_same_direction():
    graph1 = OrientedGraph(nodes={1, 2}, edges={OrientedGraphEdge(first=1, second=2, weight=1.5)})
    graph2 = OrientedGraph(nodes={1, 2}, edges={OrientedGraphEdge(first=1, second=2, weight=1.5)})

    assert graph1 == graph2


def test_oriented_graph_non_eq_edges_with_same_nodes_in_different_directions():
    graph1 = OrientedGraph(nodes={1, 2}, edges={OrientedGraphEdge(first=1, second=2, weight=1.5)})
    graph2 = OrientedGraph(nodes={1, 2}, edges={OrientedGraphEdge(first=2, second=1, weight=1.5)})

    assert graph1 != graph2