from __future__ import annotations

import inspect
from queue import LifoQueue, PriorityQueue, Queue
from typing import Protocol, Type

from npuzzle.distance import Distance
from npuzzle.node import COST, Node
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
        self.report: Report = Report(f"AStar with {type(self.distance).__name__}")

    @ReportManager.as_result(Node.get_genealogy_size, if_failed=False)
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
                g = current.g + COST
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

    @ReportManager.balance(2)
    def __add_to_open(self, node: Node) -> None:
        self.open.put(node)
        self.__open_hash.add(node)

    @ReportManager.balance(1)
    def __add_to_close(self, node: Node) -> None:
        self.close.add(node)

    @ReportManager.balance(-2)
    @ReportManager.count
    def __remove_from_open(self) -> Node:
        result = self.open.get()
        self.__open_hash.remove(result)
        return result

    def __node_in_close(self, node: Node) -> bool:
        return node in self.close

    def __node_in_open(self, node: Node) -> bool:
        return node in self.__open_hash


class Dijkstra:
    def __init__(self) -> None:
        self.open: PriorityQueue[Node] = PriorityQueue()
        self.__open_hash: set[Node] = set()
        self.close: set[Node] = set()
        self.report: Report = Report(f"Dijkstra")

    @ReportManager.as_result(Node.get_genealogy_size, if_failed=False)
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
                g = current.g + COST
                if self.__node_in_open(successor):
                    if g < successor.g:
                        successor.g = g
                else:
                    successor.g = g
                    successor.f = successor.g + successor.h
                    successor.parent = current
                    self.__add_to_open(successor)
        return None

    @ReportManager.balance(2)
    def __add_to_open(self, node: Node) -> None:
        self.open.put(node)
        self.__open_hash.add(node)

    @ReportManager.balance(1)
    def __add_to_close(self, node: Node) -> None:
        self.close.add(node)

    @ReportManager.balance(-2)
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
        self.open: PriorityQueue[Node] = PriorityQueue()
        self.close: set[Node] = set()
        self.distance: Distance = distance
        self.report: Report = Report(
            f"GreedySearch with {type(self.distance).__name__}"
        )

    @ReportManager.as_result(Node.get_genealogy_size, if_failed=False)
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
                else:
                    successor.h = self.distance.compute(successor.state, goal)
                    successor.f = successor.h
                    successor.parent = current
                    self.__add_to_open(successor)
        return None

    @ReportManager.balance(1)
    def __add_to_open(self, node: Node) -> None:
        self.open.put(node)

    @ReportManager.balance(1)
    def __add_to_close(self, node: Node) -> None:
        self.close.add(node)

    @ReportManager.balance(-1)
    @ReportManager.count
    def __remove_from_open(self) -> Node:
        result = self.open.get()
        return result

    def __node_in_close(self, node: Node) -> bool:
        return node in self.close


class BFS:
    def __init__(self) -> None:
        self.queue: Queue[Node] = Queue()
        self.visited: set[Node] = set()
        self.report: Report = Report(author="BFS")

    @ReportManager.as_result(Node.get_genealogy_size, if_failed=False)
    @ReportManager.time
    def run(self, start: Npuzzle, goal: Npuzzle) -> Node | None:
        root = Node(start)
        self.__add_to_visited(root)
        self.__add_to_queue(root)

        while not self.queue.empty():
            current = self.__remove_from_queue()

            if current.state == goal:
                return current

            successors = current.successors

            for successor in successors:
                if not successor in self.visited:
                    successor.parent = current
                    self.__add_to_visited(successor)
                    self.__add_to_queue(successor)

    @ReportManager.balance(1)
    def __add_to_queue(self, node: Node) -> None:
        self.queue.put(node)

    @ReportManager.balance(-1)
    @ReportManager.count
    def __remove_from_queue(self) -> Node:
        return self.queue.get()

    @ReportManager.balance(1)
    def __add_to_visited(self, node: Node) -> None:
        self.visited.add(node)


class DFS:
    def __init__(self) -> None:
        self.stack: LifoQueue[Node] = LifoQueue()
        self.visited: set[Node] = set()
        self.report: Report = Report(author="DFS")

    @ReportManager.as_result(Node.get_genealogy_size, if_failed=False)
    @ReportManager.time
    def run(self, start: Npuzzle, goal: Npuzzle) -> Node | None:
        root = Node(start)
        self.__add_to_stack(root)

        while not self.stack.empty():
            current = self.__remove_from_stack()

            if current.state == goal:
                return current

            if not current in self.visited:
                self.__add_to_visited(current)

                successors = current.successors
                for successor in successors:
                    successor.parent = current
                    self.__add_to_stack(successor)

    @ReportManager.balance(1)
    def __add_to_stack(self, node: Node) -> None:
        self.stack.put(node)

    @ReportManager.balance(-1)
    @ReportManager.count
    def __remove_from_stack(self) -> Node:
        return self.stack.get()

    @ReportManager.balance(1)
    def __add_to_visited(self, node: Node) -> None:
        self.visited.add(node)


# Not finished, results are weird
class IDAStar:
    def __init__(self, distance: Distance) -> None:
        self.path: set[Node] = set()
        self.distance: Distance = distance
        self.report: Report = Report(f"IDAStar with {type(self.distance).__name__}")

    @ReportManager.count
    def __search(
        self, node: Node, g: int, threshold: int, goal: Npuzzle
    ) -> Node | int | float:
        node.g = g
        node.h = self.distance.compute(node.state, goal)
        node.f = node.g + node.h

        self.__add_to_path(node)

        if node.f > threshold:
            return node.f
        if node.state == goal:
            return node

        min_ = float("+inf")
        successors = node.successors
        for successor in successors:
            if not self.__node_in_path(successor):
                successor.parent = node
                self.__add_to_path(successor)
                temp = self.__search(successor, node.g + COST, threshold, goal)
                if isinstance(temp, Node):
                    return temp
                if temp < min_:
                    min_ = temp

        return min_

    @ReportManager.as_result(Node.get_genealogy_size, if_failed=False)
    @ReportManager.time
    def run(self, start: Npuzzle, goal: Npuzzle) -> Node | None:
        root = Node(start)
        threshold = self.distance.compute(root.state, goal)

        while True:
            self.__reset_path()
            self.__add_to_path(root)
            temp = self.__search(root, 0, threshold, goal)
            if isinstance(temp, Node):
                return temp
            if temp == float("+inf"):
                return None
            threshold = temp

    @ReportManager.balance(1)
    def __add_to_path(self, node: Node) -> None:
        self.path.add(node)

    @ReportManager.reset(["current_size_complexity"])
    def __reset_path(self) -> None:
        self.path = set()

    def __node_in_path(self, node: Node) -> bool:
        return node in self.path


# TODO
class JumpPointSearch:
    def __init__(self, distance: Distance) -> None:
        self.distance: Distance = distance
        self.report: Report = Report("TODO")

    def run(self, start: Npuzzle, goal: Npuzzle) -> Node | None:
        raise NotImplementedError


AVAILABLE_SOLVERS: list[Type[Solver]] = [
    AStar,
    Dijkstra,
    GreedySearch,
    BFS,
    DFS,
    IDAStar,
]

DEFAULT_SOLVER: Type[Solver] = AStar


def is_informed(solver: Type[Solver]) -> bool:
    return "distance" in inspect.signature(solver).parameters
