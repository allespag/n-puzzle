from __future__ import annotations

from typing import Type

import matplotlib.pyplot as plt
import numpy as np

from npuzzle.distance import Distance
from npuzzle.npuzzle import Npuzzle
from npuzzle.report import Report
from npuzzle.solver import Solver, is_informed


class Benchmark:
    def __init__(
        self, solvers: list[Type[Solver]], distances: list[Type[Distance]]
    ) -> None:
        self.solvers = solvers
        self.distances = distances

    def run(self, start: Npuzzle, goal: Npuzzle) -> list[Report]:
        reports: list[Report] = []
        for solver in self.solvers:
            if is_informed(solver):
                for distance in self.distances:
                    model = solver(distance())
                    model.run(start, goal)
                    reports.append(model.report)
            else:
                model = solver()
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
                    report.max_size_complexity,
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
