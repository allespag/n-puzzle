from typing import Protocol

from npuzzle.npuzzle import Npuzzle


class Distance(Protocol):
    def compute(self, src: Npuzzle, dst: Npuzzle) -> int:
        ...


class Manhattan(Distance):
    def compute(self, src: Npuzzle, dst: Npuzzle) -> int:
        return 0
