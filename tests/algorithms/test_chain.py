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


def test_chain2():
    nodes = [
        Point.new(7, 5),
        Point.new(5, 6),
        Point.new(4, 1),
        Point.new(3, 8),
        Point.new(9, 3),
        Point.new(9, 7),
        Point.new(9, 10),
        Point.new(6, 8),
        Point.new(1, 5),
        Point.new(6, 11),
    ]
    p4, p5, p1, p7, p2, p6, p9, p8, p3, p10 = nodes

    edges = [
        PlanarStraightLineGraphEdge(first=p1, second=p3, name='e1'),
        PlanarStraightLineGraphEdge(first=p5, second=p1, name='e2'),
        PlanarStraightLineGraphEdge(first=p2, second=p1, name='e3'),
        PlanarStraightLineGraphEdge(first=p2, second=p4, name='e4'),
        PlanarStraightLineGraphEdge(first=p7, second=p3, name='e5'),
        PlanarStraightLineGraphEdge(first=p3, second=p5, name='e6'),
        PlanarStraightLineGraphEdge(first=p4, second=p5, name='e7'),
        PlanarStraightLineGraphEdge(first=p6, second=p4, name='e8'),
        PlanarStraightLineGraphEdge(first=p6, second=p9, name='e9'),
        PlanarStraightLineGraphEdge(first=p10, second=p7, name='e10'),
        PlanarStraightLineGraphEdge(first=p10, second=p8, name='e11'),
        PlanarStraightLineGraphEdge(first=p10, second=p9, name='e12'),
    ]
    oriented_edges = [
        OrientedPlanarStraightLineGraphEdge(first=p1, second=p3, name='e1'),
        OrientedPlanarStraightLineGraphEdge(first=p1, second=p5, name='e2'),
        OrientedPlanarStraightLineGraphEdge(first=p1, second=p2, name='e3'),
        OrientedPlanarStraightLineGraphEdge(first=p2, second=p4, name='e4'),
        OrientedPlanarStraightLineGraphEdge(first=p3, second=p7, name='e5'),
        OrientedPlanarStraightLineGraphEdge(first=p3, second=p5, name='e6'),
        OrientedPlanarStraightLineGraphEdge(first=p4, second=p5, name='e7'),
        OrientedPlanarStraightLineGraphEdge(first=p4, second=p6, name='e8'),
        OrientedPlanarStraightLineGraphEdge(first=p6, second=p9, name='e9'),
        OrientedPlanarStraightLineGraphEdge(first=p7, second=p10, name='e10'),
        OrientedPlanarStraightLineGraphEdge(first=p8, second=p10, name='e11'),
        OrientedPlanarStraightLineGraphEdge(first=p9, second=p10, name='e12'),
    ]
    e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12 = oriented_edges

    pslg = PlanarStraightLineGraph(nodes=nodes, edges=edges)
    target_point = Point.new(7, 8)

    y_sorted_points = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]
    oriented_pslg = OrientedPlanarStraightLineGraph(nodes=nodes, edges=oriented_edges)

    inward_edges_lists = [
        [],
        [e3],
        [e1],
        [e4],
        [e6, e2, e7],
        [e8],
        [e5],
        [],
        [e9],
        [e10, e11, e12]
    ]
    outward_edges_lists = [
        [e1, e2, e3],
        [e4],
        [e5, e6],
        [e7, e8],
        [],
        [e9],
        [e10],
        [e11],
        [e12],
        []
    ]

    regularizing_edges = [
        OrientedPlanarStraightLineGraphEdge(first=p7, second=p8, name='e1*'),
        OrientedPlanarStraightLineGraphEdge(first=p5, second=p6, name='e1**'),
    ]
    e1_reg_up, e1_reg_down = regularizing_edges
    oriented_edges_with_regularizing_edges = oriented_edges + regularizing_edges
    regularized_oriented_pslg = OrientedPlanarStraightLineGraph(nodes=nodes, edges=oriented_edges_with_regularizing_edges)
    
    weighted_oriented_edges = [OrientedPlanarStraightLineGraphEdge(first=edge.first, second=edge.second, weight=1, name=edge.name) for edge in oriented_edges_with_regularizing_edges]
    weighted_regularized_oriented_pslg = OrientedPlanarStraightLineGraph(nodes=nodes, edges=weighted_oriented_edges)

    balanced_upward_weighted_oriented_edges = deepcopy(weighted_oriented_edges)
    e9_w, e12_w = balanced_upward_weighted_oriented_edges[8], balanced_upward_weighted_oriented_edges[11]
    e1_reg_down_w = balanced_upward_weighted_oriented_edges[-1]

    e9_w.weight = 4
    e12_w.weight = 4
    e1_reg_down_w.weight = 3

    balanced_upward_weighted_regularized_oriented_pslg = OrientedPlanarStraightLineGraph(nodes=nodes, edges=balanced_upward_weighted_oriented_edges)

    balanced_downward_weighted_oriented_edges = deepcopy(balanced_upward_weighted_oriented_edges)
    e1_w = balanced_downward_weighted_oriented_edges[0]
    e3_w = balanced_downward_weighted_oriented_edges[2]
    e4_w = balanced_downward_weighted_oriented_edges[3]
    e5_w = balanced_downward_weighted_oriented_edges[4]

    e1_w.weight = 3
    e3_w.weight = 2
    e4_w.weight = 2
    e5_w.weight = 2

    balanced_weighted_regularized_oriented_pslg = OrientedPlanarStraightLineGraph(nodes=nodes, edges=balanced_downward_weighted_oriented_edges)
    
    chains = [
        [e1, e5, e10],
        [e1, e5, e1_reg_up, e11],
        [e1, e6, e1_reg_down, e9, e12],
        [e2, e1_reg_down, e9, e12],
        [e3, e4, e7, e1_reg_down, e9, e12],
        [e3, e4, e8, e9, e12]
    ]

    chains_tree = ChainsThreadedBinTree.from_iterable(chains)
    search_path = [PathDirection.left, PathDirection.right, PathDirection.next]
    chains_target_point_is_between = chains[1], chains[2]

    ans = chain(pslg, target_point)
    assert next(ans) == y_sorted_points
    assert next(ans) == oriented_pslg
    assert next(ans) == inward_edges_lists
    assert next(ans) == outward_edges_lists
    assert next(ans) == regularized_oriented_pslg
    assert next(ans) == weighted_regularized_oriented_pslg
    assert next(ans) == balanced_upward_weighted_regularized_oriented_pslg
    assert next(ans) == balanced_weighted_regularized_oriented_pslg
    assert next(ans) == chains
    assert next(ans) == chains_tree
    assert next(ans) == (search_path, chains_target_point_is_between)


def test_chain3():
    """
        A test where we assign additional weight to the leftmost edge of several ones while balancing the graph.

        Also, the chains tree has '`node`, `node.right`, `node.right.right`' subtree
        where, with the target point between chains `node` and `node.right`, we go from `node` to `node.right` and then backwards.
    """
    nodes = [
        Point.new(4, 4),
        Point.new(4, 1),
        Point.new(1, 5),
        Point.new(7, 8),
        Point.new(4, 8),
        Point.new(4, 12),
        Point.new(8, 10),
    ]
    p2, p1, p3, p5, p4, p7, p6 = nodes

    edges = [
        PlanarStraightLineGraphEdge(first=p3, second=p1, name='e1'),
        PlanarStraightLineGraphEdge(first=p3, second=p2, name='e2'),
        PlanarStraightLineGraphEdge(first=p5, second=p2, name='e3'),
        PlanarStraightLineGraphEdge(first=p3, second=p7, name='e4'),
        PlanarStraightLineGraphEdge(first=p3, second=p4, name='e5'),
        PlanarStraightLineGraphEdge(first=p3, second=p5, name='e6'),
        PlanarStraightLineGraphEdge(first=p5, second=p4, name='e7'),
        PlanarStraightLineGraphEdge(first=p7, second=p5, name='e8'),
        PlanarStraightLineGraphEdge(first=p5, second=p6, name='e9'),
    ]
    oriented_edges = [
        OrientedPlanarStraightLineGraphEdge(first=p1, second=p3, name='e1'),
        OrientedPlanarStraightLineGraphEdge(first=p2, second=p3, name='e2'),
        OrientedPlanarStraightLineGraphEdge(first=p2, second=p5, name='e3'),
        OrientedPlanarStraightLineGraphEdge(first=p3, second=p7, name='e4'),
        OrientedPlanarStraightLineGraphEdge(first=p3, second=p4, name='e5'),
        OrientedPlanarStraightLineGraphEdge(first=p3, second=p5, name='e6'),
        OrientedPlanarStraightLineGraphEdge(first=p4, second=p5, name='e7'),
        OrientedPlanarStraightLineGraphEdge(first=p5, second=p7, name='e8'),
        OrientedPlanarStraightLineGraphEdge(first=p5, second=p6, name='e9'),
    ]
    e1, e2, e3, e4, e5, e6, e7, e8, e9 = oriented_edges

    pslg = PlanarStraightLineGraph(nodes=nodes, edges=edges)
    target_point = Point.new(4, 7)

    y_sorted_points = [p1, p2, p3, p4, p5, p6, p7]
    oriented_pslg = OrientedPlanarStraightLineGraph(nodes=nodes, edges=oriented_edges)

    inward_edges_lists = [
        [],
        [],
        [e1, e2],
        [e5],
        [e7, e6, e3],
        [e9],
        [e4, e8]
    ]
    outward_edges_lists = [
        [e1],
        [e2, e3],
        [e4, e5, e6],
        [e7],
        [e8, e9],
        [],
        []
    ]

    regularizing_edges = [
        OrientedPlanarStraightLineGraphEdge(first=p1, second=p2, name='e1*'),
        OrientedPlanarStraightLineGraphEdge(first=p6, second=p7, name='e1**'),
    ]
    e1_reg_up, e1_reg_down = regularizing_edges
    oriented_edges_with_regularizing_edges = oriented_edges + regularizing_edges
    regularized_oriented_pslg = OrientedPlanarStraightLineGraph(nodes=nodes, edges=oriented_edges_with_regularizing_edges)
    
    weighted_oriented_edges = [OrientedPlanarStraightLineGraphEdge(first=edge.first, second=edge.second, weight=1, name=edge.name) for edge in oriented_edges_with_regularizing_edges]
    weighted_regularized_oriented_pslg = OrientedPlanarStraightLineGraph(nodes=nodes, edges=weighted_oriented_edges)

    balanced_upward_weighted_oriented_edges = deepcopy(weighted_oriented_edges)
    e8_w = balanced_upward_weighted_oriented_edges[7]
    e8_w.weight = 2

    balanced_upward_weighted_regularized_oriented_pslg = OrientedPlanarStraightLineGraph(nodes=nodes, edges=balanced_upward_weighted_oriented_edges)

    balanced_downward_weighted_oriented_edges = deepcopy(balanced_upward_weighted_oriented_edges)
    e1_w = balanced_downward_weighted_oriented_edges[0]
    e1_reg_up_w = balanced_downward_weighted_oriented_edges[-2]

    e1_w.weight = 2
    e1_reg_up_w.weight = 2

    balanced_weighted_regularized_oriented_pslg = OrientedPlanarStraightLineGraph(nodes=nodes, edges=balanced_downward_weighted_oriented_edges)
    
    chains = [
        [e1, e4],
        [e1, e5, e7, e8],
        [e1_reg_up, e2, e6, e8],
        [e1_reg_up, e3, e9, e1_reg_down],
    ]

    chains_tree = ChainsThreadedBinTree.from_iterable(chains)
    search_path = [PathDirection.right, PathDirection.prev]
    chains_target_point_is_between = chains[1], chains[2]

    ans = chain(pslg, target_point)
    assert next(ans) == y_sorted_points
    assert next(ans) == oriented_pslg
    assert next(ans) == inward_edges_lists
    assert next(ans) == outward_edges_lists
    assert next(ans) == regularized_oriented_pslg
    assert next(ans) == weighted_regularized_oriented_pslg
    assert next(ans) == balanced_upward_weighted_regularized_oriented_pslg
    assert next(ans) == balanced_weighted_regularized_oriented_pslg
    assert next(ans) == chains
    assert next(ans) == chains_tree
    assert next(ans) == (search_path, chains_target_point_is_between)


def test_chain4():
    """Trivial case with two chains."""
    nodes = [Point.new(3, 1), Point.new(1, 4), Point.new(3, 7)]
    p1, p2, p3 = nodes

    edges = [PlanarStraightLineGraphEdge(first=p1, second=p2, name='e1'), PlanarStraightLineGraphEdge(first=p1, second=p3, name='e2')]
    oriented_edges = [OrientedPlanarStraightLineGraphEdge(first=edge.first, second=edge.second, name=edge.name) for edge in edges]
    e1, e2 = oriented_edges

    pslg = PlanarStraightLineGraph(nodes=nodes, edges=edges)
    target_point = Point.new(2, 4)

    y_sorted_points = nodes
    oriented_pslg = OrientedPlanarStraightLineGraph(nodes=nodes, edges=oriented_edges)

    inward_edges_lists = [[], [e1], [e2]]
    outward_edges_lists = [[e1, e2], [], []]

    regularizing_edges = [OrientedPlanarStraightLineGraphEdge(first=p2, second=p3, name='e1**')]
    e1_reg_down = regularizing_edges[0]
    oriented_edges_with_regularizing_edges = oriented_edges + regularizing_edges
    regularized_oriented_pslg = OrientedPlanarStraightLineGraph(nodes=nodes, edges=oriented_edges_with_regularizing_edges)
    
    weighted_oriented_edges = [OrientedPlanarStraightLineGraphEdge(first=edge.first, second=edge.second, weight=1, name=edge.name) for edge in oriented_edges_with_regularizing_edges]
    balanced_weighted_regularized_oriented_pslg = OrientedPlanarStraightLineGraph(nodes=nodes, edges=weighted_oriented_edges)
    
    chains = [[e1, e1_reg_down], [e2]]
    chains_tree = ChainsThreadedBinTree.from_iterable(chains)
    search_path = [PathDirection.right, PathDirection.prev]
    chains_target_point_is_between = chains[0], chains[1]

    ans = chain(pslg, target_point)
    assert next(ans) == y_sorted_points
    assert next(ans) == oriented_pslg
    assert next(ans) == inward_edges_lists
    assert next(ans) == outward_edges_lists
    assert next(ans) == regularized_oriented_pslg
    assert next(ans) == balanced_weighted_regularized_oriented_pslg
    assert next(ans) == balanced_weighted_regularized_oriented_pslg
    assert next(ans) == balanced_weighted_regularized_oriented_pslg
    assert next(ans) == chains
    assert next(ans) == chains_tree
    assert next(ans) == (search_path, chains_target_point_is_between)