import pytest
from algogears.core import Graph, GraphEdge


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


def test_graph_add_node_correct():
    graph = Graph()
    graph.add_node(1)

    assert graph.nodes == {1}


def test_graph_add_edge_with_old_nodes_correct():
    nodes = [1, 2]
    graph = Graph(nodes=nodes)

    new_edge = GraphEdge(first=1, second=2)
    graph.add_edge(new_edge)

    assert graph.edges == {new_edge}


def test_graph_add_edge_with_new_nodes_correct():
    nodes = [1, 2]
    graph = Graph(nodes=nodes)

    new_edge = GraphEdge(first=3, second=4)
    graph.add_edge(new_edge)

    assert graph.edges == {new_edge}


def test_graph_add_edge_incorrect_type():
    graph = Graph()
    
    with pytest.raises(TypeError):
        graph.add_edge(42)


def test_graph_has_node():
    graph = Graph(nodes={1, 2})
    assert graph.has_node(1)


def test_graph_has_edge_same_direction():
    graph = Graph(nodes={1, 2}, edges={GraphEdge(first=1, second=2)})
    assert graph.has_edge(GraphEdge(first=1, second=2))


def test_graph_has_edge_reverse_direction():
    graph = Graph(nodes={1, 2}, edges={GraphEdge(first=2, second=1)})
    assert graph.has_edge(GraphEdge(first=2, second=1))


def test_graph_remove_node():
    nodes = [1, 2, 3]
    edges = [
        GraphEdge(first=1, second=2),
        GraphEdge(first=2, second=3),
        GraphEdge(first=1, second=3),
    ]
    graph = Graph(nodes=nodes, edges=edges)
    
    graph.remove_node(2)
    
    assert graph.nodes == {1, 3}
    assert graph.edges == {GraphEdge(first=1, second=3)}


def test_graph_remove_edge():
    nodes = [1, 2, 3]
    edges = [
        GraphEdge(first=1, second=2),
        GraphEdge(first=2, second=3),
    ]
    graph = Graph(nodes=nodes, edges=edges)

    graph.remove_edge(edges[0])
    
    assert graph.nodes == set(nodes)
    assert graph.edges == {GraphEdge(first=2, second=3)}


def test_graph_eq_edges_with_same_nodes_in_same_direction():
    graph1 = Graph(nodes={1, 2}, edges={GraphEdge(first=1, second=2, weight=1.5)})
    graph2 = Graph(nodes={1, 2}, edges={GraphEdge(first=1, second=2, weight=1.5)})

    assert graph1 == graph2


def test_graph_eq_edges_with_same_nodes_in_different_directions():
    graph1 = Graph(nodes={1, 2}, edges={GraphEdge(first=1, second=2, weight=1.5)})
    graph2 = Graph(nodes={1, 2}, edges={GraphEdge(first=2, second=1, weight=1.5)})

    assert graph1 == graph2