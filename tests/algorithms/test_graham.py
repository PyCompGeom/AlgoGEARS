from math import isclose
from algogears.core import Point
from algogears.graham import graham, GrahamStepsTable, GrahamStepsTableRow


def test_graham1():
    pts = [Point.new(7, 0), Point.new(3, 3), Point.new(0, 0)]
    centroid = Point.new(3.3333333333333335, 1.0)
    ordered = [Point.new(7, 0), Point.new(3, 3), Point.new(0, 0)]
    origin = Point.new(7, 0)

    triples = [
        (ordered[0], ordered[1], ordered[2]),
        (ordered[1], ordered[2], ordered[0])
    ]
    are_angles_less_than_pi = [True, True]

    steps_table = GrahamStepsTable(ordered_points=ordered)
    steps_table.extend(
        GrahamStepsTableRow(point_triple=triple, is_angle_less_than_pi=is_angle_lt_pi)
        for triple, is_angle_lt_pi in zip(triples, are_angles_less_than_pi)
    )
    
    hull = [Point.new(7, 0), Point.new(3, 3), Point.new(0, 0)]
    
    ans = graham(pts)
    assert next(ans) == centroid
    assert next(ans) == ordered
    assert next(ans) == origin
    
    assert next(ans) == triples
    assert next(ans) == are_angles_less_than_pi

    assert next(ans) == steps_table
    assert next(ans) == steps_table
    assert next(ans) == steps_table
    
    assert next(ans) == hull


def test_graham2():
    pts = [
        Point.new(3, 10),
        Point.new(6, 8),
        Point.new(3, 5),
        Point.new(2, 8),
        Point.new(4, 8),
        Point.new(5, 5),
        Point.new(3, 3),
        Point.new(7, 7),
        Point.new(5, 0),
        Point.new(0, 0),
        Point.new(10, 3),
    ]
    centroid = Point.new(4.0, 7.666666666666667)
    ordered = [
        Point.new(5, 0),
        Point.new(5, 5),
        Point.new(10, 3),
        Point.new(7, 7),
        Point.new(6, 8),
        Point.new(4, 8),
        Point.new(3, 10),
        Point.new(2, 8),
        Point.new(0, 0),
        Point.new(3, 5),
        Point.new(3, 3),
    ]
    origin = Point.new(5, 0)
    triples = [
        (ordered[0], ordered[1], ordered[2]),
        (ordered[0], ordered[2], ordered[3]),
        (ordered[2], ordered[3], ordered[4]),
        (ordered[3], ordered[4], ordered[5]),
        (ordered[4], ordered[5], ordered[6]),
        (ordered[3], ordered[4], ordered[6]),
        (ordered[4], ordered[6], ordered[7]),
        (ordered[6], ordered[7], ordered[8]),
        (ordered[7], ordered[8], ordered[9]),
        (ordered[8], ordered[9], ordered[10]),
        (ordered[7], ordered[8], ordered[10]),
        (ordered[8], ordered[10], ordered[0]),
        (ordered[7], ordered[8], ordered[0])
    ]
    are_angles_less_than_pi = [False, True, True, True, False, True, True, True, True, False, True, False, True]
    
    steps_table = GrahamStepsTable(ordered_points=ordered)
    steps_table.extend(
        GrahamStepsTableRow(point_triple=triple, is_angle_less_than_pi=is_angle_lt_pi)
        for triple, is_angle_lt_pi in zip(triples, are_angles_less_than_pi)
    )
    
    hull = [
        Point.new(5, 0),
        Point.new(10, 3),
        Point.new(7, 7),
        Point.new(6, 8),
        Point.new(3, 10),
        Point.new(2, 8),
        Point.new(0, 0)
    ]
    
    ans = graham(pts)
    assert next(ans) == centroid
    assert next(ans) == ordered
    assert next(ans) == origin
    
    assert next(ans) == triples
    assert next(ans) == are_angles_less_than_pi

    assert next(ans) == steps_table
    assert next(ans) == steps_table
    assert next(ans) == steps_table
    
    assert next(ans) == hull


def test_graham3():
    pts = [
        Point.new(2, 8),
        Point.new(5, 6),
        Point.new(7, 8),
        Point.new(8, 11),
        Point.new(7, 5),
        Point.new(10, 7),
        Point.new(11, 5),
        Point.new(8, 2),
        Point.new(1, 3),
        Point.new(5, 2),
    ]
    centroid = Point.new(4.666666666666667, 7.333333333333333)
    ordered = [
        Point.new(8, 2),
        Point.new(7, 5),
        Point.new(11, 5),
        Point.new(10, 7),
        Point.new(7, 8),
        Point.new(8, 11),
        Point.new(2, 8),
        Point.new(1, 3),
        Point.new(5, 2),
        Point.new(5, 6)
    ]
    origin = Point.new(8, 2)
    triples = [
        (ordered[0], ordered[1], ordered[2]),
        (ordered[0], ordered[2], ordered[3]),
        (ordered[2], ordered[3], ordered[4]),
        (ordered[3], ordered[4], ordered[5]),
        (ordered[2], ordered[3], ordered[5]),
        (ordered[0], ordered[2], ordered[5]),
        (ordered[2], ordered[5], ordered[6]),
        (ordered[5], ordered[6], ordered[7]),
        (ordered[6], ordered[7], ordered[8]),
        (ordered[7], ordered[8], ordered[9]),
        (ordered[8], ordered[9], ordered[0]),
        (ordered[7], ordered[8], ordered[0])
    ]
    are_angles_less_than_pi = [False, True, True, False, False, True, True, True, True, True, False, True]
    
    steps_table = GrahamStepsTable(ordered_points=ordered)
    steps_table.extend(
        GrahamStepsTableRow(point_triple=triple, is_angle_less_than_pi=is_angle_lt_pi)
        for triple, is_angle_lt_pi in zip(triples, are_angles_less_than_pi)
    )

    hull = [
        Point.new(8, 2),
        Point.new(11, 5),
        Point.new(8, 11),
        Point.new(2, 8),
        Point.new(1, 3),
        Point.new(5, 2)
    ]
    
    ans = graham(pts)
    assert next(ans) == centroid
    assert next(ans) == ordered
    assert next(ans) == origin
    
    assert next(ans) == triples
    assert next(ans) == are_angles_less_than_pi

    assert next(ans) == steps_table
    assert next(ans) == steps_table
    assert next(ans) == steps_table
    
    assert next(ans) == hull
