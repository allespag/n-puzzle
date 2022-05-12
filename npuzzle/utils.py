from __future__ import annotations

from enum import Enum, auto
from typing import Any


class Direction(Enum):
    TOP = auto()
    RIGHT = auto()
    BOTTOM = auto()
    LEFT = auto()


def index_in_list(index: int, list: list[Any]) -> bool:
    return 0 <= index < len(list)


def coor_in_list(coor: tuple[int, int], shape: tuple[int, int]) -> bool:
    max_x, max_y = shape
    x, y = coor

    return 0 <= x < max_x and 0 <= y < max_y


def index_to_coor(index: int, shape: tuple[int, int]) -> tuple[int, int]:
    width, _ = shape

    return (index % width, index // width)


def coor_to_index(coor: tuple[int, int], shape: tuple[int, int]) -> int:
    x, y = coor
    width, _ = shape

    return y * width + x


def snail_array(n: int) -> list[int]:
    top_index = 0
    right_index = n - 1
    bottom_index = n - 1
    left_index = 0

    result = [0] * (n * n)
    curr = 1
    dir = Direction.RIGHT

    while curr <= n * n - 1:
        if dir == Direction.RIGHT:
            # left -> right
            for i in range(left_index, right_index + 1):
                result[top_index * n + i] = curr
                curr += 1
            top_index += 1
            dir = Direction.BOTTOM
        elif dir == Direction.BOTTOM:
            # top -> bottom
            for i in range(top_index, bottom_index + 1):
                result[right_index + (n * i)] = curr
                curr += 1
            right_index -= 1
            dir = Direction.LEFT
        elif dir == Direction.LEFT:
            # right -> left
            for i in range(right_index, left_index - 1, -1):
                result[bottom_index * n + i] = curr
                curr += 1
            bottom_index -= 1
            dir = Direction.TOP
        elif dir == Direction.TOP:
            # bottom -> top
            for i in range(bottom_index, top_index - 1, -1):
                result[left_index + (n * i)] = curr
                curr += 1
            left_index += 1
            dir = Direction.RIGHT
    return result
