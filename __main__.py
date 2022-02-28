from __future__ import annotations

import argparse
import json
import random

__CHECK_PERF = False
if __CHECK_PERF:
    import cProfile
    import pstats

from typing import Type

from npuzzle.benchmark import Benchmark
from npuzzle.distance import AVAILABLE_HEURISTICS, DEFAULT_HEURISTIC, Distance
from npuzzle.npuzzle import MAX_N_VALUE, MIN_N_VALUE, Npuzzle
from npuzzle.solver import AVAILABLE_SOLVERS, DEFAULT_SOLVER, Solver, is_informed


def main(args: argparse.Namespace) -> None:
    """Main function."""

    # generate the puzzle
    if args.file:
        try:
            puzzle = Npuzzle.from_file(args.file)
        except Exception as e:
            print(f"Error: {e}")
            return
    else:
        puzzle = Npuzzle.from_random(args.random, solvable=not args.unsolvable)

    # check if the puzzle is solvable
    if not puzzle.is_solvable():
        print(f"This puzzle can't be solved.\n{puzzle}")
        return

    # benchmark if necessary and leave
    if args.report or args.kompare or args.csv:
        benchmark = Benchmark(args.config["solvers"], args.config["heuristics"])

        if args.csv:
            for elem in benchmark.compute_statistics(iter=args.csv):
                author, df = elem
                Benchmark.to_csv(df, author)
                if args.describe:
                    Benchmark.describe(df, author)
            return

        reports = benchmark.run(puzzle, puzzle.goal)
        if args.report:
            for report in reports:
                print(report)
        if args.kompare:
            benchmark.display(reports)
        if not (args.output is None) and puzzle.to_file(args.output):
            print(f"The puzzle has been saved in {args.output}.")

        return

    # create the solver with its heuristic if necessary
    solver = args.solver
    if is_informed(solver):
        heuristic = args.heuristic()
        solver = solver(heuristic)
    else:
        solver = solver()

    # run
    if __CHECK_PERF:
        profile = cProfile.Profile()
        res = profile.runcall(solver.run, puzzle, puzzle.goal)
        ps = pstats.Stats(profile)
        ps.print_stats()
    else:
        res = solver.run(puzzle, puzzle.goal)

    # print the report
    if res is None:
        print("No solution found.")
    else:
        try:
            res.display_genealogy(ascending=False)
        except RecursionError:
            print("The path is too big to be displayed.")
        finally:
            print(solver.report)

    # write the puzzle to a file if necessary
    if not (args.output is None):
        if puzzle.to_file(args.output):
            print(f"The puzzle has been saved in {args.output}.")
        else:
            print(f"Error: {args.output} already exists.")


def get_args() -> argparse.Namespace:
    """Get the arguments from command line."""

    def check_random(value: str) -> int:
        """Check the size of the puzzle."""

        if MIN_N_VALUE <= int(value) <= MAX_N_VALUE:
            return int(value)
        else:
            raise argparse.ArgumentTypeError(
                f"The value of 'random' must be in ({MIN_N_VALUE}, {MAX_N_VALUE}) range. ({value} here)"
            )

    def check_heuristic(value: str) -> Type[Distance]:
        """Check the value of solver."""

        for heuristic in AVAILABLE_HEURISTICS:
            if heuristic.__name__ == value:
                return heuristic
        raise argparse.ArgumentTypeError(
            f"The value of 'heuristic' must be in {([heuristic.__name__ for heuristic in AVAILABLE_HEURISTICS])}. ({value!r} here)"
        )

    def check_solver(value: str) -> Type[Solver]:
        """Check the value of solver."""

        for solver in AVAILABLE_SOLVERS:
            if solver.__name__ == value:
                return solver
        raise argparse.ArgumentTypeError(
            f"The value of 'solver' must be in {([solver.__name__ for solver in AVAILABLE_SOLVERS])}. ({value!r} here)"
        )

    def check_cfg(value: str) -> dict[str, list[Type[Solver]] | list[Type[Distance]]]:
        """Chech the value of the config."""

        try:
            with open(value) as f:
                cfg = json.load(f)
        except Exception:
            raise argparse.ArgumentTypeError(
                f"Something bad happened while trying to load data from {value}"
            )

        if "solvers" not in cfg or "heuristics" not in cfg:
            raise argparse.ArgumentTypeError(
                "'solvers' AND 'heuristics' should be part of your config"
            )

        solvers = [
            solver for solver in AVAILABLE_SOLVERS if solver.__name__ in cfg["solvers"]
        ]
        heuristics = [
            heuristic
            for heuristic in AVAILABLE_HEURISTICS
            if heuristic.__name__ in cfg["heuristics"]
        ]

        if not solvers or not heuristics:
            raise argparse.ArgumentTypeError(
                f"You must provide some solvers/heuristics. ({solvers=} and {heuristics=} here)"
            )

        return {"solvers": solvers, "heuristics": heuristics}

    parser = argparse.ArgumentParser(prog="n-puzzle")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-F",
        "--file",
        type=str,
        metavar="FILENAME",
        help="n-puzzle to load",
    )
    group.add_argument(
        "-R",
        "--random",
        type=check_random,
        metavar="N",
        default=3,
        help="generates a random N puzzle",
    )
    parser.add_argument(
        "-H",
        "--heuristic",
        type=check_heuristic,
        metavar="NAME",
        default=DEFAULT_HEURISTIC,
        help=f"particular way of calculating the distances. {[heuristic.__name__ for heuristic in AVAILABLE_HEURISTICS]}",
    )
    parser.add_argument(
        "-S",
        "--solver",
        type=check_solver,
        metavar="NAME",
        default=DEFAULT_SOLVER,
        help=f"algorithm to use. {[solver.__name__ for solver in AVAILABLE_SOLVERS]}",
    )
    parser.add_argument(
        "-U",
        "--unsolvable",
        action="store_true",
        default=False,
        help="forces generation of an unsolvable puzzle. Ignored when -f",
    )
    parser.add_argument(
        "-k",
        "--kompare",
        action="store_true",
        default=False,
        help="display a nice plot to compare the different solvers (with a config)",
    )
    parser.add_argument(
        "-r",
        "--report",
        action="store_true",
        default=False,
        help="prints out a report for each type of solver/heuristic (with a config)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        metavar="FILENAME",
        default=None,
        help="output the puzzle to a file",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=check_cfg,
        metavar="FILENAME",
        default={"solvers": AVAILABLE_SOLVERS, "heuristics": AVAILABLE_HEURISTICS},
        help="config to load",
    )
    parser.add_argument(
        "--csv",
        type=int,
        metavar="ITER",
        default=None,
        help="perform some tests with ITER puzzles (with a config)",
    )
    parser.add_argument(
        "-d",
        "--describe",
        action="store_true",
        default=False,
        help="when --csv, describe each csv",
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()
    main(args)
