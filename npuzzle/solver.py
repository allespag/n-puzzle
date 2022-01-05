from __future__ import annotations

from queue import PriorityQueue
from typing import Protocol

from npuzzle.distance import Distance
from npuzzle.node import Node
from npuzzle.npuzzle import Npuzzle


class Solver(Protocol):
    def run(self, start: Npuzzle, goal: Npuzzle) -> Node | None:
        ...


# note: i think A* should not be here
#       so i can move import out
class AStar(Solver):
    def __init__(self, distance: Distance):
        self.open: PriorityQueue[Node] = PriorityQueue()
        self.close: list[Node] = []
        self.distance = distance

    def run(self, start: Npuzzle, goal: Npuzzle) -> Node | None:
        root = Node(start)

        self.open.put(root)
        while not self.open.empty():
            current_node = self.open.get()

            if current_node.state == goal:
                print(f"{current_node.state=}")
                return current_node
            else:
                self.close.append(current_node)

            successors = current_node.successors
            # print(f"{successors=!r}")
            for successor in successors:
                ########
                if self.__node_in_close(successor):
                    continue
                else:
                    successor.g = current_node.g + 1
                    successor.h = self.distance.compute(successor.state, goal)
                    successor.f = successor.g + successor.h
                    successor.parent = current_node
                    self.open.put(successor)
                #######
            # print(f"CURRENT = {current_node}")
            # open_str = (
            #     "[\n\t" + "\n\t".join(repr(elem) for elem in self.open.queue) + "\n]"
            # )
            # close_str = "[\n\t" + "\n\t".join(repr(elem) for elem in self.close) + "\n]"
            # print(f"OPEN = {open_str}")
            # print(f"CLOSE = {close_str}")
        return None

    def __node_in_open(self, node: Node) -> bool:
        return any(node.state.tiles == elem.state.tiles for elem in self.open.queue)

    def __node_in_close(self, node: Node) -> bool:
        return any(node.state.tiles == elem.state.tiles for elem in self.close)


AVAILABLE_SOLVERS = [
    AStar,
]

DEFAULT_SOLVER = AStar
