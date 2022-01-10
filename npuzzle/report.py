from __future__ import annotations

import time
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Protocol, TypeVar

T = TypeVar("T")


class Reportable(Protocol):
    report: Report


@dataclass
class Report:
    time_complexity: int = 0
    size_complexity: int = 0
    max_size_complexity: int = 0
    start: int | None = None
    end: int | None = None

    def __str__(self) -> str:
        return f"""Report(
        Complexity in time: {self.time_complexity},
        Complexity in size: {self.max_size_complexity},
        In {self.time_taken * 1e-9:.2f}s\n)"""

    @staticmethod
    def current_time() -> int:
        return time.perf_counter_ns()

    @property
    def time_taken(self) -> float:
        if not self.start is None and self.end is None:
            return Report.current_time() - self.start
        elif self.start is None:
            return float("+inf")
        else:
            return self.end - self.start  # type: ignore


class ReportManager:
    @staticmethod
    def time(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(instance: Reportable, *args: Any, **kwargs: Any) -> T:
            instance.report.start = Report.current_time()
            result = func(instance, *args, **kwargs)
            instance.report.end = Report.current_time()
            return result

        return wrapper

    @staticmethod
    def count(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(instance: Reportable, *args: Any, **kwargs: Any) -> T:
            result = func(instance, *args, **kwargs)
            instance.report.time_complexity += 1
            return result

        return wrapper

    @staticmethod
    def balance(n: int) -> Callable[[Callable[..., T]], Callable[..., T]]:
        def decorator(func: Callable[..., T]) -> Callable[..., T]:
            @wraps(func)
            def wrapper(instance: Reportable, *args: Any, **kwargs: Any) -> T:
                result = func(instance, *args, **kwargs)
                instance.report.size_complexity += n
                if (
                    instance.report.size_complexity
                    > instance.report.max_size_complexity
                ):
                    instance.report.max_size_complexity = (
                        instance.report.size_complexity
                    )
                return result

            return wrapper

        return decorator
