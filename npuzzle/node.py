from __future__ import annotations

from npuzzle.npuzzle import Npuzzle


# note: dataclass ? __lt__ ?
class Node:
    def __init__(self, state: Npuzzle) -> None:
        self.state = state
        self.f = 0  # total cost of the node
        self.g = 0  # distance between the current node and the start node
        self.h = 0  # estimated distance from the current node to the end node
        self.parent: Node | None = None

    def __lt__(self, other: Node) -> bool:
        return self.f < other.f

    @property
    def successors(self) -> list[Node]:
        return [Node(state) for state in self.state.successors]
