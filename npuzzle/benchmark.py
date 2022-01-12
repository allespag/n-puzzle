from __future__ import annotations

from typing import Type

import matplotlib.pyplot as plt
import numpy as np

from npuzzle.distance import Distance
from npuzzle.npuzzle import Npuzzle
from npuzzle.report import Report
from npuzzle.solver import Solver


class Benchmark:
    def __init__(
        self, solvers: list[Type[Solver]], distances: list[Type[Distance]]
    ) -> None:
        self.solvers = solvers
        self.distances = distances

    def run(self, start: Npuzzle, goal: Npuzzle) -> list[Report]:
        reports: list[Report] = []
        for solver in self.solvers:
            for distance in self.distances:
                model: Solver = solver(distance())
                model.run(start, goal)
                reports.append(model.report)

        return reports

    def display(self, reports: list[Report]) -> None:
        categories = ["Time complexity", "Size complexity", "Time taken", "Result"]
        categories = [*categories, categories[0]]

        infos = np.array(  # type: ignore
            [
                [
                    report.time_complexity,
                    report.max_size_complexity,
                    report.time_taken,
                    report.result,
                    report.time_complexity,
                ]
                for report in reports
            ]
        )
        infos = infos / infos.max(axis=0)  # type: ignore

        label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(categories))  # type: ignore

        plt.figure(figsize=(8, 8))
        plt.subplot(polar=True)
        plt.thetagrids(np.degrees(label_loc), labels=categories)

        for info, report in zip(infos, reports):
            plt.plot(label_loc, info, label=report.author)

        plt.legend()
        plt.show()
