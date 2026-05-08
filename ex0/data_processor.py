from typing import Any
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data:Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        pass


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        self._numbers: list[tuple[int, str]] = []
        self._processing_rank: int = 0

    def validate(self, data: Any) -> bool:
        return isinstance(data, (int, float, list[int | float])) and not isinstance (data, bool)
  

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Got exception: improper numeric data")
        if isinstance(data, list):
            for i in data:
                self._numbers.append((self._processing_rank, str(i)))
                self._processing_rank += 1
        else:
            self._numbers.append((self._processing_rank, str(data)))
    
    def output(self) -> tuple[int, str]:
        if not self._numbers:
            raise IndexError("All data extracted from numeric processor")
        return self._numbers.pop(0)


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        self._text: list[tuple[int, str]] = []
        self._processing_rank: int = 0

    def validate(self, data: Any) -> bool:
        return isinstance(data, (str, list[str]))

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Got exception: improper text data")
        if isinstance(data, list):
            for i in data:
                self._text.append((self._processing_rank, str(i)))
                self._processing_rank += 1
        else:
            self._text.append((self._processing_rank, str(data)))
    
    def output(self) -> tuple[int, str]:
        if not self._text:
            raise IndexError("All data extracted from numeric processor")
        return self._text.pop(0)


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        self._logs: list[tuple[int, str]] = []
        self._processing_rank: int = 0

    def validate(self, data: Any) -> bool:
        return isinstance(data, (dict[str, str], list[dict[str, str]]))

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Got exception: improper log data")
        if isinstance(data, list):
            for i in data:
                self._logs.append((self._processing_rank, str(i)))
                self._processing_rank += 1
        else:
            self._logs.append((self._processing_rank, str(data)))
    
    def output(self) -> tuple[int, str]:
        if not self._logs:
            raise IndexError("All data extracted from numeric processor")
        return self._logs.pop(0)