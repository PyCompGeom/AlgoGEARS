from algogears.core import PathDirection, Point, PlanarStraightLineGraph, PlanarStraightLineGraphEdge
from algogears.slab import PlanarStraightLineGraphEdgeThreadedBinTree, slab, Slab, SlabBinTree, SlabBinTreeNode


def test_slab1():
    """Graph adapted from 'Computational Geometry: An Introduction' by Franco P. Preparata and Michael Ian Shamos."""
    nodes = [
        Point.new(1, 1),
        Point.new(7, 1),
        Point.new(16, 1),
        Point.new(4, 2),
        Point.new(13, 3),
        Point.new(5, 4),
        Point.new(4, 6),
        Point.new(18, 7),
        Point.new(15, 8),
        Point.new(10, 9),
        Point.new(1, 10),
        Point.new(14, 11),
        Point.new(7, 12),
    ]
    p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13 = nodes
    edges = [
        PlanarStraightLineGraphEdge(first=p1, second=p2, name='e1'),
        PlanarStraightLineGraphEdge(first=p2, second=p5, name='e2'),
        PlanarStraightLineGraphEdge(first=p3, second=p5, name='e3'),
        PlanarStraightLineGraphEdge(first=p6, second=p7, name='e4'),
        PlanarStraightLineGraphEdge(first=p3, second=p8, name='e5'),
        PlanarStraightLineGraphEdge(first=p4, second=p9, name='e6'),
        PlanarStraightLineGraphEdge(first=p2, second=p9, name='e7'),
        PlanarStraightLineGraphEdge(first=p6, second=p10, name='e8'),
        PlanarStraightLineGraphEdge(first=p9, second=p10, name='e9'),
        PlanarStraightLineGraphEdge(first=p1, second=p11, name='e10'),
        PlanarStraightLineGraphEdge(first=p4, second=p11, name='e11'),
        PlanarStraightLineGraphEdge(first=p7, second=p11, name='e12'),
        PlanarStraightLineGraphEdge(first=p9, second=p12, name='e13'),
        PlanarStraightLineGraphEdge(first=p8, second=p12, name='e14'),
        PlanarStraightLineGraphEdge(first=p7, second=p13, name='e15'),
        PlanarStraightLineGraphEdge(first=p12, second=p13, name='e16'),
    ]
    e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16 = edges

    pslg = PlanarStraightLineGraph(nodes=nodes, edges=edges)
    target_point = Point.new(7, 5)

    y_sorted_points = nodes
    slabs = [
        Slab(y_min=float('-inf'), y_max=p1.y, points=[], edges=[], inserted_edges=[], deleted_edges=[]),
        Slab(y_min=p1.y, y_max=p4.y, points=[p1, p2, p3], edges=[e10, e7, e2, e3, e5], inserted_edges=[e10, e1, e7, e2, e3, e5], deleted_edges=[e1]),
        Slab(y_min=p4.y, y_max=p5.y, points=[p4], edges=[e10, e11, e6, e7, e2, e3, e5], inserted_edges=[e11, e6], deleted_edges=[]),
        Slab(y_min=p5.y, y_max=p6.y, points=[p5], edges=[e10, e11, e6, e7, e5], inserted_edges=[], deleted_edges=[e2, e3]),
        Slab(y_min=p6.y, y_max=p7.y, points=[p6], edges=[e10, e11, e4, e8, e6, e7, e5], inserted_edges=[e4, e8], deleted_edges=[]),
        Slab(y_min=p7.y, y_max=p8.y, points=[p7], edges=[e10, e11, e12, e15, e8, e6, e7, e5], inserted_edges=[e12, e15], deleted_edges=[e4]),
        Slab(y_min=p8.y, y_max=p9.y, points=[p8], edges=[e10, e11, e12, e15, e8, e6, e7, e14], inserted_edges=[e14], deleted_edges=[e5]),
        Slab(y_min=p9.y, y_max=p10.y, points=[p9], edges=[e10, e11, e12, e15, e8, e9, e13, e14], inserted_edges=[e9, e13], deleted_edges=[e6, e7]),
        Slab(y_min=p10.y, y_max=p11.y, points=[p10], edges=[e10, e11, e12, e15, e13, e14], inserted_edges=[], deleted_edges=[e8, e9]),
        Slab(y_min=p11.y, y_max=p12.y, points=[p11], edges=[e15, e13, e14], inserted_edges=[], deleted_edges=[e10, e11, e12]),
        Slab(y_min=p12.y, y_max=p13.y, points=[p12], edges=[e15, e16], inserted_edges=[e16], deleted_edges=[e13, e14]),
        Slab(y_min=p13.y, y_max=float('inf'), points=[p13], edges=[], inserted_edges=[], deleted_edges=[e15, e16]),
    ]
    slab_tree = SlabBinTree.from_iterable(slabs)
    slab_search_path = [PathDirection.left, PathDirection.right, PathDirection.right]
    target_slab = slabs[4]
    edge_tree = PlanarStraightLineGraphEdgeThreadedBinTree.from_iterable(target_slab.edges)
    edge_search_path = [PathDirection.right, PathDirection.left, PathDirection.prev]
    target_edges = e8, e6

    ans = slab(pslg, target_point)
    assert next(ans) == y_sorted_points
    assert next(ans) == slabs
    assert next(ans) == slabs
    assert next(ans) == slabs
    assert next(ans) == slabs
    assert next(ans) == slab_tree
    assert next(ans) == (slab_search_path, target_slab)
    assert next(ans) == edge_tree
    assert next(ans) == (edge_search_path, target_edges)


def test_slab2():
    """Target point at the left of the graph."""
    nodes = [
        Point.new(2, 1),
        Point.new(6, 3),
        Point.new(2, 5),
        Point.new(8, 5),
        Point.new(4, 7),
        Point.new(7, 9),
        Point.new(4, 10),
    ]
    p1, p2, p3, p4, p5, p6, p7 = nodes
    edges = [
        PlanarStraightLineGraphEdge(first=p1, second=p3, name='e1'),
        PlanarStraightLineGraphEdge(first=p1, second=p2, name='e2'),
        PlanarStraightLineGraphEdge(first=p2, second=p3, name='e3'),
        PlanarStraightLineGraphEdge(first=p2, second=p5, name='e4'),
        PlanarStraightLineGraphEdge(first=p2, second=p4, name='e5'),
        PlanarStraightLineGraphEdge(first=p3, second=p7, name='e6'),
        PlanarStraightLineGraphEdge(first=p4, second=p6, name='e7'),
        PlanarStraightLineGraphEdge(first=p5, second=p7, name='e8'),
        PlanarStraightLineGraphEdge(first=p5, second=p6, name='e9'),
        PlanarStraightLineGraphEdge(first=p6, second=p7, name='e10'),
    ]
    e1, e2, e3, e4, e5, e6, e7, e8, e9, e10 = edges

    pslg = PlanarStraightLineGraph(nodes=nodes, edges=edges)
    target_point = Point.new(1, 6)

    y_sorted_points = nodes
    slabs = [
        Slab(y_min=float('-inf'), y_max=p1.y, points=[], edges=[], inserted_edges=[], deleted_edges=[]),
        Slab(y_min=p1.y, y_max=p2.y, points=[p1], edges=[e1, e2], inserted_edges=[e1, e2], deleted_edges=[]),
        Slab(y_min=p2.y, y_max=p3.y, points=[p2], edges=[e1, e3, e4, e5], inserted_edges=[e3, e4, e5], deleted_edges=[e2]),
        Slab(y_min=p3.y, y_max=p5.y, points=[p3, p4], edges=[e6, e4, e7], inserted_edges=[e6, e7], deleted_edges=[e1, e3, e5]),
        Slab(y_min=p5.y, y_max=p6.y, points=[p5], edges=[e6, e8, e9, e7], inserted_edges=[e8, e9], deleted_edges=[e4]),
        Slab(y_min=p6.y, y_max=p7.y, points=[p6], edges=[e6, e8, e10], inserted_edges=[e10], deleted_edges=[e9, e7]),
        Slab(y_min=p7.y, y_max=float('inf'), points=[p7], edges=[], inserted_edges=[], deleted_edges=[e6, e8, e10]),
    ]
    slab_tree = SlabBinTree.from_iterable(slabs)
    slab_search_path = []
    target_slab = slabs[3]
    edge_tree = PlanarStraightLineGraphEdgeThreadedBinTree.from_iterable(target_slab.edges)
    edge_search_path = [PathDirection.left]
    target_edges = None, e6

    ans = slab(pslg, target_point)
    assert next(ans) == y_sorted_points
    assert next(ans) == slabs
    assert next(ans) == slabs
    assert next(ans) == slabs
    assert next(ans) == slabs
    assert next(ans) == slab_tree
    assert next(ans) == (slab_search_path, target_slab)
    assert next(ans) == edge_tree
    assert next(ans) == (edge_search_path, target_edges)


def test_slab3():
    """Trivial case with one edge and target point at the right of the graph."""
    nodes = [Point.new(1, 1), Point.new(1, 3)]
    p1, p2 = nodes
    edges = [PlanarStraightLineGraphEdge(first=p1, second=p2)]
    e1 = edges[0]
    
    pslg = PlanarStraightLineGraph(nodes=nodes, edges=edges)
    target_point = Point.new(2, 2)

    y_sorted_points = nodes
    slabs = [
        Slab(y_min=float('-inf'), y_max=p1.y, points=[], edges=[], inserted_edges=[], deleted_edges=[]),
        Slab(y_min=p1.y, y_max=p2.y, points=[p1], edges=[e1], inserted_edges=[e1], deleted_edges=[]),
        Slab(y_min=p2.y, y_max=float('inf'), points=[p2], edges=[], inserted_edges=[], deleted_edges=[e1])
    ]
    slab_tree = SlabBinTree.from_iterable(slabs)
    slab_search_path = []
    target_slab = slabs[1]
    edge_tree = PlanarStraightLineGraphEdgeThreadedBinTree.from_iterable(target_slab.edges)
    edge_search_path = []
    target_edges = e1, None

    ans = slab(pslg, target_point)
    assert next(ans) == y_sorted_points
    assert next(ans) == slabs
    assert next(ans) == slabs
    assert next(ans) == slabs
    assert next(ans) == slabs
    assert next(ans) == slab_tree
    assert next(ans) == (slab_search_path, target_slab)
    assert next(ans) == edge_tree
    assert next(ans) == (edge_search_path, target_edges)