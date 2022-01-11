from __future__ import annotations

from queue import PriorityQueue
from typing import Protocol

from npuzzle.distance import Distance
from npuzzle.node import Node
from npuzzle.npuzzle import Npuzzle
from npuzzle.report import Report, ReportManager


class Solver(Protocol):
    report: Report

    def run(self, start: Npuzzle, goal: Npuzzle) -> Node | None:
        ...


class AStar:
    def __init__(self, distance: Distance) -> None:
        self.open: PriorityQueue[Node] = PriorityQueue()
        self.__open_hash: set[Node] = set()
        self.close: set[Node] = set()
        self.distance: Distance = distance
        self.report: Report = Report()

    @ReportManager.time
    def run(self, start: Npuzzle, goal: Npuzzle) -> Node | None:
        root = Node(start)
        self.__add_to_open(root)

        while not self.open.empty():
            current = self.__remove_from_open()

            if current.state == goal:
                return current

            self.__add_to_close(current)
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
                    self.__add_to_open(successor)
        return None

    @ReportManager.balance(1)
    def __add_to_open(self, node: Node) -> None:
        self.open.put(node)
        self.__open_hash.add(node)

    @ReportManager.balance(1)
    def __add_to_close(self, node: Node) -> None:
        self.close.add(node)

    @ReportManager.balance(-1)
    @ReportManager.count
    def __remove_from_open(self) -> Node:
        result = self.open.get()
        self.__open_hash.remove(result)
        return result

    def __node_in_close(self, node: Node) -> bool:
        return node in self.close

    def __node_in_open(self, node: Node) -> bool:
        return node in self.__open_hash


class GreedySearch:
    def __init__(self, distance: Distance) -> None:
        self.distance: Distance = distance
        self.report: Report = Report()

    def run(self, start: Npuzzle, goal: Npuzzle) -> Node | None:
        return None


class JumpPointSearch:
    def __init__(self, distance: Distance) -> None:
        self.distance: Distance = distance
        self.report: Report = Report()

    def run(self, start: Npuzzle, goal: Npuzzle) -> Node | None:
        return None


AVAILABLE_SOLVERS: list[Solver] = [
    AStar,
]

DEFAULT_SOLVER: Solver = AStar
