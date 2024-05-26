from pytest import fixture
from algogears.core import Point
from algogears.graham import GrahamStepsTableRow, GrahamStepsTable


@fixture
def table_row():
    return GrahamStepsTableRow(
        point_triple=(
            Point.new(1, 1),
            Point.new(2, 0),
            Point.new(3, 3)
        ),
        is_angle_less_than_pi=True
    )


@fixture
def table(table_row):
    return GrahamStepsTable(
        ordered_points=[Point.new(2, 0), Point.new(3, 3), Point.new(1, 1)],
        rows=[table_row]
    )


def test_steps_table_row_serializaion(table_row):
    serialized_row = table_row.model_dump()
    deserialized_row = GrahamStepsTableRow(**serialized_row)
    assert deserialized_row == table_row


def test_steps_table_serialization(table):
    serialized_table = table.model_dump()
    deserialized_table = GrahamStepsTable(**serialized_table)
    assert deserialized_table == table