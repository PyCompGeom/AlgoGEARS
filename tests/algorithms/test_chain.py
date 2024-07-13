from copy import deepcopy
from algogears.core import Point, PlanarStraightLineGraphEdge, PlanarStraightLineGraph, OrientedPlanarStraightLineGraphEdge, OrientedPlanarStraightLineGraph, PathDirection
from algogears.chain import chain, ChainsThreadedBinTreeNode, ChainsThreadedBinTree


def test_chain1():
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
        Point.new(7, 12)
    ]
    edges = [
        PlanarStraightLineGraphEdge(first=nodes[0], second=nodes[1], name='e1'),
        PlanarStraightLineGraphEdge(first=nodes[1], second=nodes[4], name='e2'),
        PlanarStraightLineGraphEdge(first=nodes[2], second=nodes[4], name='e3'),
        PlanarStraightLineGraphEdge(first=nodes[5], second=nodes[6], name='e4'),
        PlanarStraightLineGraphEdge(first=nodes[2], second=nodes[7], name='e5'),
        PlanarStraightLineGraphEdge(first=nodes[3], second=nodes[8], name='e6'),
        PlanarStraightLineGraphEdge(first=nodes[1], second=nodes[8], name='e7'),
        PlanarStraightLineGraphEdge(first=nodes[5], second=nodes[9], name='e8'),
        PlanarStraightLineGraphEdge(first=nodes[8], second=nodes[9], name='e9'),
        PlanarStraightLineGraphEdge(first=nodes[0], second=nodes[10], name='e10'),
        PlanarStraightLineGraphEdge(first=nodes[3], second=nodes[10], name='e11'),
        PlanarStraightLineGraphEdge(first=nodes[6], second=nodes[10], name='e12'),
        PlanarStraightLineGraphEdge(first=nodes[8], second=nodes[11], name='e13'),
        PlanarStraightLineGraphEdge(first=nodes[7], second=nodes[11], name='e14'),
        PlanarStraightLineGraphEdge(first=nodes[6], second=nodes[12], name='e15'),
        PlanarStraightLineGraphEdge(first=nodes[11], second=nodes[12], name='e16'),
    ]
    oriented_edges = [OrientedPlanarStraightLineGraphEdge(first=edge.first, second=edge.second, name=edge.name) for edge in edges]
    e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16 = oriented_edges
    
    pslg = PlanarStraightLineGraph(nodes=nodes, edges=edges)
    target_point = Point.new(16, 6)

    y_sorted_points = nodes
    oriented_pslg = OrientedPlanarStraightLineGraph(nodes=nodes, edges=oriented_edges)
    
    inward_edges_lists = [
        [],
        [e1],
        [],
        [],
        [e2, e3],
        [],
        [e4],
        [e5],
        [e6, e7],
        [e8, e9],
        [e10, e11, e12],
        [e13, e14],
        [e15, e16],
    ]
    outward_edges_lists = [
        [e10, e1],
        [e7, e2],
        [e3, e5],
        [e11, e6],
        [],
        [e4, e8],
        [e12, e15],
        [e14],
        [e9, e13],
        [],
        [],
        [e16],
        [],
    ]

    regularizing_edges = [
        OrientedPlanarStraightLineGraphEdge(first=nodes[1], second=nodes[2], name='e1*'),
        OrientedPlanarStraightLineGraphEdge(first=nodes[1], second=nodes[3], name='e2*'),
        OrientedPlanarStraightLineGraphEdge(first=nodes[3], second=nodes[5], name='e3*'),
        OrientedPlanarStraightLineGraphEdge(first=nodes[10], second=nodes[12], name='e1**'),
        OrientedPlanarStraightLineGraphEdge(first=nodes[9], second=nodes[11], name='e2**'),
        OrientedPlanarStraightLineGraphEdge(first=nodes[4], second=nodes[7], name='e3**'),
    ]
    e1_reg_up, e2_reg_up, e3_reg_up, e1_reg_down, e2_reg_down, e3_reg_down = regularizing_edges
    oriented_edges_with_regularizing_edges = oriented_edges + regularizing_edges
    regularized_oriented_pslg = OrientedPlanarStraightLineGraph(nodes=nodes, edges=oriented_edges_with_regularizing_edges)
    
    weighted_oriented_edges = [OrientedPlanarStraightLineGraphEdge(first=edge.first, second=edge.second, weight=1, name=edge.name) for edge in oriented_edges_with_regularizing_edges]
    weighted_regularized_oriented_pslg = OrientedPlanarStraightLineGraph(nodes=nodes, edges=weighted_oriented_edges)

    balanced_upward_weighted_oriented_edges = deepcopy(weighted_oriented_edges)
    e14_w, e16_w = balanced_upward_weighted_oriented_edges[13], balanced_upward_weighted_oriented_edges[15]
    e1_w_reg_down, e2_w_reg_down, e3_w_reg_down = balanced_upward_weighted_oriented_edges[-3:]

    e14_w.weight = 3
    e16_w.weight = 6
    e1_w_reg_down.weight = 3
    e2_w_reg_down.weight = 2
    e3_w_reg_down.weight = 2

    balanced_upward_weighted_regularized_oriented_pslg = OrientedPlanarStraightLineGraph(nodes=nodes, edges=balanced_upward_weighted_oriented_edges)

    balanced_downward_weighted_oriented_edges = deepcopy(balanced_upward_weighted_oriented_edges)
    e1_w, e4_w = balanced_downward_weighted_oriented_edges[0], balanced_downward_weighted_oriented_edges[3]
    e1_w_reg_up, e2_w_reg_up, e3_w_reg_up = balanced_downward_weighted_oriented_edges[-6:-3]

    e1_w.weight = 9
    e4_w.weight = 2
    e1_w_reg_up.weight = 2
    e2_w_reg_up.weight = 5
    e3_w_reg_up.weight = 3

    balanced_downward_weighted_regularized_oriented_pslg = OrientedPlanarStraightLineGraph(nodes=nodes, edges=balanced_downward_weighted_oriented_edges)

    chains = [
        [e10, e1_reg_down],
        [e1, e2_reg_up, e11, e1_reg_down],
        [e1, e2_reg_up, e3_reg_up, e4, e12, e1_reg_down],
        [e1, e2_reg_up, e3_reg_up, e4, e15],
        [e1, e2_reg_up, e3_reg_up, e8, e2_reg_down, e16],
        [e1, e2_reg_up, e6, e9, e2_reg_down, e16],
        [e1, e7, e13, e16],
        [e1, e2, e3_reg_down, e14, e16],
        [e1, e1_reg_up, e3, e3_reg_down, e14, e16],
        [e1, e1_reg_up, e5, e14, e16],
    ]
    chains_tree = ChainsThreadedBinTree.from_iterable(chains)
    search_path = [PathDirection.right, PathDirection.left, PathDirection.right, PathDirection.next]
    chains_target_point_is_between = chains[6], chains[7]

    ans = chain(pslg, target_point)
    assert next(ans) == y_sorted_points
    assert next(ans) == oriented_pslg
    assert next(ans) == inward_edges_lists
    assert next(ans) == outward_edges_lists
    assert next(ans) == regularized_oriented_pslg
    assert next(ans) == weighted_regularized_oriented_pslg
    assert next(ans) == balanced_upward_weighted_regularized_oriented_pslg
    assert next(ans) == balanced_downward_weighted_regularized_oriented_pslg
    assert next(ans) == chains
    assert next(ans) == chains_tree
    assert next(ans) == (search_path, chains_target_point_is_between)