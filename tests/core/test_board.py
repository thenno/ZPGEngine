from core.board import (
    Position,
    line_of_view,
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
