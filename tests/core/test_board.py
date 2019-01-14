from core.board import (
    Position,
    Distance,
    Direction,
    line_of_view,
    get_distance,
    generate_movements,
)


def test_line_of_view():
    assert list(line_of_view(Position(5, 5), Position(0, 0))) == [
        Position(x=5, y=5),
        Position(x=4, y=4),
        Position(x=3, y=3),
        Position(x=2, y=2),
        Position(x=1, y=1),
        Position(x=0, y=0),
    ]
    assert list(line_of_view(Position(5, 5), Position(10, 0))) == [
        Position(x=5, y=5),
        Position(x=6, y=4),
        Position(x=7, y=3),
        Position(x=8, y=2),
        Position(x=9, y=1),
        Position(x=10, y=0),
    ]
    assert list(line_of_view(Position(5, 5), Position(10, 5))) == [
        Position(x=5, y=5),
        Position(x=6, y=5),
        Position(x=7, y=5),
        Position(x=8, y=5),
        Position(x=9, y=5),
        Position(x=10, y=5),
    ]
    assert list(line_of_view(Position(8, 5), Position(1, 1))) == [
        Position(x=8, y=5),
        Position(x=7, y=4),
        Position(x=6, y=4),
        Position(x=5, y=3),
        Position(x=4, y=3),
        Position(x=3, y=2),
        Position(x=2, y=2),
        Position(x=1, y=1),
    ]


def test_get_distance():
    assert get_distance(Position(0, 0), Position(0, 0)) == Distance(0)
    assert get_distance(Position(10, 0), Position(0, 0)) == Distance(10)
    assert get_distance(Position(0, 10), Position(0, 0)) == Distance(10)
    assert get_distance(Position(10, 10), Position(0, 0)) == Distance(10)
    assert get_distance(Position(6, 2), Position(12, 10)) == Distance(8)


def test_direction():
    assert Direction.from_positions(Position(5, 5), Position(5, 5)) == Direction(0, 0)
    assert Direction.from_positions(Position(5, 5), Position(1, 3)) == Direction(-1, -1)
    assert Direction.from_positions(Position(3, 6), Position(5, 5)) == Direction(1, -1)


def test_generate_movements():
    assert list(generate_movements(Position(5, 5), Distance(1))) == [
        Position(4, 4),
        Position(4, 5),
        Position(4, 6),
        Position(5, 4),
        Position(5, 6),
        Position(6, 4),
        Position(6, 5),
        Position(6, 6),
    ]
    assert list(generate_movements(Position(5, 5), Distance(2))) == [
        Position(x=3, y=3),
        Position(x=3, y=4),
        Position(x=3, y=5),
        Position(x=3, y=6),
        Position(x=3, y=7),
        Position(x=4, y=3),
        Position(x=4, y=4),
        Position(x=4, y=5),
        Position(x=4, y=6),
        Position(x=4, y=7),
        Position(x=5, y=3),
        Position(x=5, y=4),
        Position(x=5, y=6),
        Position(x=5, y=7),
        Position(x=6, y=3),
        Position(x=6, y=4),
        Position(x=6, y=5),
        Position(x=6, y=6),
        Position(x=6, y=7),
        Position(x=7, y=3),
        Position(x=7, y=4),
        Position(x=7, y=5),
        Position(x=7, y=6),
        Position(x=7, y=7),
    ]
