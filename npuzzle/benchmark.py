from __future__ import annotations

import datetime
import os
from typing import Any, Iterator, Type

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from npuzzle.distance import Distance
from npuzzle.npuzzle import Npuzzle
from npuzzle.report import Report
from npuzzle.solver import Solver, is_informed

STATS_DIRECTORY = "data/"


class Benchmark:
    def __init__(
        self, solvers: list[Type[Solver]], distances: list[Type[Distance]]
    ) -> None:
        self.solvers = solvers
        self.distances = distances

    def __iter_solvers(self) -> Iterator[Solver]:
        for solver in self.solvers:
            if is_informed(solver):
                for distance in self.distances:
                    model = solver(distance())
                    yield model
            else:
                model = solver()
                yield model

    def run(self, start: Npuzzle, goal: Npuzzle) -> list[Report]:
        reports: list[Report] = []

        for model in self.__iter_solvers():
            model.run(start, goal)
            reports.append(model.report)

        return reports

    def display(self, reports: list[Report]) -> None:
        plt.style.use("ggplot")

        categories = ["Time complexity", "Size complexity", "Time taken", "Result"]
        categories = [*categories, categories[0]]

        data = np.array(
            [
                [
                    report.time_complexity,
                    report.size_complexity,
                    report.time_taken,
                    report.result,
                    report.time_complexity,
                ]
                for report in reports
            ]
        )
        data = data / data.max(axis=0)

        label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(categories))  # type: ignore

        plt.figure(num="Radar chart", figsize=(8, 8))
        plt.subplot(polar=True)
        plt.thetagrids(np.degrees(label_loc), labels=categories)

        for row, report in zip(data, reports):
            plt.plot(label_loc, row, label=report.author)

        plt.gca().axes.yaxis.set_ticklabels([])
        plt.legend()
        plt.show()

    def compute_statistics(
        self, iter: int = 100, n: int = 3
    ) -> list[tuple[str, pd.DataFrame]]:
        puzzles = [Npuzzle.from_random(n, solvable=True) for _ in range(iter)]
        goal = puzzles[0].goal

        reports: dict[str, list[Any]] = {}
        for solver in self.__iter_solvers():
            reports[solver.report.author] = []

        for puzzle in puzzles:
            for solver in self.__iter_solvers():
                solver.run(puzzle, goal)
                current_report = solver.report
                mini_report = (
                    current_report.size_complexity,
                    current_report.time_complexity,
                    current_report.time_taken_in_s,
                    current_report.result,
                )
                reports[solver.report.author].append(mini_report)

        return [
            (
                author,
                pd.DataFrame(
                    report,
                    columns=[
                        "size complexity",
                        "time complexity",
                        "time taken",
                        "result",
                    ],
                ),
            )
            for author, report in reports.items()
        ]

    @staticmethod
    def to_csv(df: pd.DataFrame, author: str):
        if not os.path.exists(STATS_DIRECTORY):
            os.makedirs(STATS_DIRECTORY)

        df.to_csv(
            f"{STATS_DIRECTORY}{author}_{datetime.datetime.now().isoformat(timespec='minutes')}.csv"
        )

    @staticmethod
    def describe(df: pd.DataFrame, author: str):
        print(f"By {author}:\n{df.describe()}")
