from math import pi
from typing import Iterable
from pydantic import BaseModel, Field
from .core import Point


class GrahamStepsTableRow(BaseModel):
    point_triple: tuple[Point, Point, Point]
    is_angle_less_than_pi: bool
    
    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.point_triple == other.point_triple and
            self.is_angle_less_than_pi == other.is_angle_less_than_pi
        )

    def __str__(self) -> str:
        return f"[{str(self.point_triple)}, {str(self.is_angle_less_than_pi)}]"


class GrahamStepsTable(BaseModel):
    ordered_points: list[Point]
    rows: list[GrahamStepsTableRow] = Field(default_factory=list)
    
    def append(self, item: GrahamStepsTableRow) -> None:
        self.rows.append(item)
    
    def extend(self, iterable: Iterable[GrahamStepsTableRow]) -> None:
        self.rows.extend(iterable)

    def __getitem__(self, key: int) -> GrahamStepsTableRow:
        return self.rows[key]
    
    def __setitem__(self, key: int, value: GrahamStepsTableRow) -> None:
        self.rows[key] = value

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.ordered_points == other.ordered_points and
            self.rows == other.rows
        )

    def __str__(self):
        return f"[{', '.join(str(row) for row in self)}]"


def graham(points: Iterable[Point]):
    if len(points) < 3:
        yield sorted(points, key=lambda p: (p.y, -p.x))
    else:
        i = 2
        while Point.direction(points[0], points[1], points[i]) == 0:
            i += 1
        
        centroid = Point.centroid(points[0], points[1], points[i])
        yield centroid

        origin = min(points, key=lambda p: (p.y, -p.x))
        ordered_points = sorted_points(points, centroid, origin)
        yield ordered_points
        yield origin

        ordered_points.append(origin)
        steps_table = GrahamStepsTable(ordered_points=ordered_points)
        hull = make_hull(steps_table, ordered_points)
        ordered_points.pop()
        steps_table.ordered_points.pop()
        
        yield [row.point_triple for row in steps_table.rows]
        yield [row.is_angle_less_than_pi for row in steps_table.rows]
        yield steps_table
        yield steps_table
        yield steps_table
        
        yield hull


def sorted_points(points: list[Point], centroid: Point, origin: Point) -> list[Point]:
    min_angle = Point.polar_angle(origin, centroid)

    def angle_and_dist(p):
        p_angle = Point.polar_angle(p, centroid)
        angle = p_angle if p_angle >= min_angle else 2 * pi + p_angle
        return (angle, Point.dist(p, centroid))

    return sorted(points, key=angle_and_dist)


def make_hull(steps_table: GrahamStepsTable, ordered_points: list[Point]) -> list[Point]:
    res = ordered_points[:2]

    for point in ordered_points[2:]:
        while len(res) > 1 and Point.direction(res[-2], res[-1], point) >= 0:
            steps_table.append(GrahamStepsTableRow(point_triple=(res[-2], res[-1], point), is_angle_less_than_pi=False))
            res.pop()

        if len(res) > 1:
            steps_table.append(GrahamStepsTableRow(point_triple=(res[-2], res[-1], point), is_angle_less_than_pi=True))
        
        res.append(point)

    return res[:-1]
