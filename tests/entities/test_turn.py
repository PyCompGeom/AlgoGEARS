from algogears.core import Point, Turn


def test_turn_left():
    start_point = Point.new(1, 1)
    intermediary_point = Point.new(2, 2)
    end_point = Point.new(0, 2)

    assert Turn(start_point, intermediary_point, end_point) == Turn.LEFT


def test_turn_right():
    start_point = Point.new(1, 1)
    intermediary_point = Point.new(2, 2)
    end_point = Point.new(2, 0)

    assert Turn(start_point, intermediary_point, end_point) == Turn.RIGHT


def test_turn_straight_endpoint_after_intermediary_point():
    start_point = Point.new(1, 1)
    intermediary_point = Point.new(2, 2)
    end_point = Point.new(3, 3)

    assert Turn(start_point, intermediary_point, end_point) == Turn.STRAIGHT


def test_turn_straight_endpoint_before_start_point():
    start_point = Point.new(1, 1)
    intermediary_point = Point.new(2, 2)
    end_point = Point.new(0, 0)

    assert Turn(start_point, intermediary_point, end_point) == Turn.STRAIGHT


def test_turn_straight_endpoint_between_start_and_intermediary_points():
    start_point = Point.new(1, 1)
    intermediary_point = Point.new(2, 2)
    end_point = Point.new(1.5, 1.5)

    assert Turn(start_point, intermediary_point, end_point) == Turn.STRAIGHT