from __future__ import annotations

from dataclasses import dataclass
from queue import PriorityQueue
from typing import Protocol

from npuzzle.distance import Distance
from npuzzle.node import Node
from npuzzle.npuzzle import Npuzzle


@dataclass
class Report:
    time_complexity: int = 0
    size_complexity: int = 0
    path_size: int = 0


class Solver(Protocol):
    def run(self, start: Npuzzle, goal: Npuzzle) -> Node | None:
        ...


class AStar(Solver):
    def __init__(self, distance: Distance):
        self.open: PriorityQueue[Node] = PriorityQueue()
        self.close: set[Node] = set()
        self.distance: Distance = distance
        self.report: Report = Report()

    def run(self, start: Npuzzle, goal: Npuzzle) -> Node | None:
        root = Node(start)
        self.open.put(root)

        while not self.open.empty():
            current = self.open.get()

            if current.state == goal:
                return current

            self.close.add(current)
            successors = current.successors

            for successor in successors:
                if self.__node_in_close(successor):
                    continue
                g = current.g + 1
                if self.__node_in_open(successor):
                    if g < successor.g:
                        successor.g = g
                else:
                    successor.g = g
                    successor.h = self.distance.compute(successor.state, goal)
                    successor.f = successor.g + successor.h
                    successor.parent = current
                    self.open.put(successor)
        return None

    def __node_in_close(self, node: Node) -> bool:
        return node in self.close

    def __node_in_open(self, node: Node) -> bool:
        return any(node.state.tiles == elem.state.tiles for elem in self.open.queue)


AVAILABLE_SOLVERS = [
    AStar,
]

DEFAULT_SOLVER = AStar
