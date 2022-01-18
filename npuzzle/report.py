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
    author: str
    time_complexity: int = 0
    size_complexity: int = 0
    current_size_complexity: int = 0
    start: int | None = None
    end: int | None = None
    result: Any | None = None

    def __str__(self) -> str:
        return f"""Report(
        Result: {self.result}
        Complexity in time: {self.time_complexity},
        Complexity in size: {self.size_complexity},
        In {self.time_taken * 1e-9:.2f}s,
        By {self.author},\n)"""

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
                instance.report.current_size_complexity += n
                if (
                    instance.report.current_size_complexity
                    > instance.report.size_complexity
                ):
                    instance.report.size_complexity = (
                        instance.report.current_size_complexity
                    )
                return result

            return wrapper

        return decorator

    @staticmethod
    def reset(attrs: list[str]) -> Callable[[Callable[..., T]], Callable[..., T]]:
        def decorator(func: Callable[..., T]) -> Callable[..., T]:
            @wraps(func)
            def wrapper(instance: Reportable, *args: Any, **kwargs: Any) -> T:
                result = func(instance, *args, **kwargs)
                for attr in attrs:
                    setattr(instance, attr, 0)
                return result

            return wrapper

        return decorator

    @staticmethod
    def as_result(
        modifier: Callable[..., Any], if_failed: bool = True, default: Any = None
    ) -> Callable[[Callable[..., T]], Callable[..., T]]:
        def decorator(func: Callable[..., T]) -> Callable[..., T]:
            @wraps(func)
            def wrapper(instance: Reportable, *args: Any, **kwargs: Any) -> T:
                result = func(instance, *args, **kwargs)

                if not result is None or if_failed:
                    try:
                        instance.report.result = modifier(result)
                    except Exception:
                        instance.report.result = default
                return result

            return wrapper

        return decorator
