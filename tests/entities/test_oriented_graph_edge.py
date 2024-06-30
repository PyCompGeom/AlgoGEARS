import pytest
from algogears.core import OrientedGraphEdge


def test_graph_edge_creation():
    edge = OrientedGraphEdge(first=1, second=2, weight=1)

    assert edge.first == 1
    assert edge.second == 2
    assert edge.weight == 1


def test_graph_edge_eq():
    edge1 = OrientedGraphEdge(first=1, second=2, weight=1)
    edge2 = OrientedGraphEdge(first=1, second=2, weight=1)

    assert edge1 == edge2


def test_graph_edge_non_eq_reversed():
    edge1 = OrientedGraphEdge(first=1, second=2, weight=1)
    edge2 = OrientedGraphEdge(first=2, second=1, weight=1)

    assert edge1 != edge2


def test_graph_edge_hash():
    edge1 = OrientedGraphEdge(first=1, second=2, weight=1)
    edge2 = OrientedGraphEdge(first=1, second=2, weight=1)

    assert hash(edge1) == hash(edge2)


def test_graph_edge_other_node():
    edge = OrientedGraphEdge(first=1, second=2)

    assert edge.other_node(1) == 2
    assert edge.other_node(2) == 1
    
    with pytest.raises(ValueError):
        _ = edge.other_node(3)