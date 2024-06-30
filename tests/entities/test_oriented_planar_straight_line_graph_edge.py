import pytest
from algogears.core import Point, OrientedPlanarStraightLineGraphEdge


def test_oriented_planar_straight_line_graph_edge_creation():
    edge = OrientedPlanarStraightLineGraphEdge(first=Point.new(1, 1), second=Point.new(2, 2), weight=1)

    assert edge.first == Point.new(1, 1)
    assert edge.second == Point.new(2, 2)
    assert edge.weight == 1


def test_oriented_planar_straight_line_graph_edge_eq():
    edge1 = OrientedPlanarStraightLineGraphEdge(first=Point.new(1, 1), second=Point.new(2, 2), weight=1)
    edge2 = OrientedPlanarStraightLineGraphEdge(first=Point.new(1, 1), second=Point.new(2, 2), weight=1)

    assert edge1 == edge2


def test_oriented_planar_straight_line_graph_edge_non_eq_reversed():
    edge1 = OrientedPlanarStraightLineGraphEdge(first=Point.new(1, 1), second=Point.new(2, 2), weight=1)
    edge2 = OrientedPlanarStraightLineGraphEdge(first=Point.new(2, 2), second=Point.new(1, 1), weight=1)

    assert edge1 != edge2


def test_oriented_planar_straight_line_graph_edge_hash():
    edge1 = OrientedPlanarStraightLineGraphEdge(first=Point.new(1, 1), second=Point.new(2, 2), weight=1)
    edge2 = OrientedPlanarStraightLineGraphEdge(first=Point.new(1, 1), second=Point.new(2, 2), weight=1)

    assert hash(edge1) == hash(edge2)


def test_oriented_planar_straight_line_graph_edge_other_node():
    edge = OrientedPlanarStraightLineGraphEdge(first=Point.new(1, 1), second=Point.new(2, 2), weight=1)
    
    assert edge.other_node(Point.new(1, 1)) == Point.new(2, 2)
    assert edge.other_node(Point.new(2, 2)) == Point.new(1, 1)
    
    with pytest.raises(ValueError):
        _ = edge.other_node(Point.new(3, 3))