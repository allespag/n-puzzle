from __future__ import annotations

from typing import Any


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


# TODO
def snail_array(n: int) -> list[int]:
    return [ord(c) for c in "TODO"]
