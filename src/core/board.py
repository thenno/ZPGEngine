from typing import NewType, Iterable, Callable

from core.components import Position


Distance = NewType('Distance', int)


def generate_movements(pos: Position, distance: Distance) -> Iterable[Position]:
    for mx in range(-distance, distance + 1):
        for my in range(-distance, distance + 1):
            new_pos = Position(mx + pos.x, my + pos.y)
            yield new_pos


def get_fov_mask(position: Position, fow_size: int, board_size: int, is_full: Callable):
    def is_visible(pos_to: Position) -> bool:
        line = list(get_line_of_view(position, pos_to))
        for i, pos_for_check in enumerate(line):
            if i not in (0, len(line) - 1) and is_full(pos_for_check):
                return False
        return True

    positions = generate_movements(position, distance=Distance(fow_size))
    result = set()
    for pos in positions:
        if not (0 <= pos.x < board_size and 0 <= pos.y < board_size):
            continue
        if not is_visible(pos):
            continue
        result.add(pos)
    return result


def get_distance(pos1, pos2) -> Distance:
    return Distance(
        max(abs(pos1.x - pos2.x), abs(pos1.y - pos2.y)),
    )


def get_line_of_view(pos1: Position, pos2: Position) -> Iterable[Position]:
    """
    Bresenham's line algorithm

    There may be some problems, check it again and add tests
    """

    # TODO: check it again and add tests
    delta_x = abs(pos2.x - pos1.x)
    delta_y = abs(pos2.y - pos1.y)
    if delta_x > delta_y:
        a1, b1, a2, b2 = pos1.x, pos1.y, pos2.x, pos2.y
    else:
        a1, b1, a2, b2 = pos1.y, pos1.x, pos2.y, pos2.x
    delta_a = abs(a2 - a1)
    delta_b = abs(b2 - b1)
    error = 0.0
    delta_err = delta_b / delta_a if delta_a != 0 else 0
    b = b1
    direction = b2 - b1
    if direction > 0:
        direction = 1
    if direction < 0:
        direction = -1
    if a1 < a2:
        range_a = range(a1, a2 + 1)
    else:
        range_a = range(a2, a1 + 1)[::-1]
    for a in range_a:
        if delta_x > delta_y:
            yield Position(a, b)
        else:
            yield Position(b, a)
        error = error + delta_err
        if error >= 0.5:
            b = b + direction
            error = error - 1.0
