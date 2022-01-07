from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Protocol, TypeVar

RT = TypeVar("RT")


class Reportable(Protocol):
    report: Report


@dataclass
class Report:
    time_complexity: int = 0
    size_complexity: int = 0
    result_size: int = 0
    start: datetime | None = None
    end: datetime | None = None


class ReportManager:
    @staticmethod
    def time(func: Callable[..., RT]) -> Callable[..., RT]:
        def wrapper(instance: Reportable, *args: Any, **kwargs: Any) -> RT:
            instance.report.start = datetime.now()
            result = func(instance, *args, **kwargs)
            instance.report.end = datetime.now()
            return result

        return wrapper

    @staticmethod
    def count(func: Callable[..., RT]) -> Callable[..., RT]:
        def wrapper(instance: Reportable, *args: Any, **kwargs: Any) -> RT:
            result = func(instance, *args, **kwargs)
            instance.report.time_complexity += 1
            return result

        return wrapper

    # @staticmethod
    # def
