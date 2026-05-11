from typing import Any
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        pass


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        self._validated: list[tuple[int, str]] = []
        self._processing_rank: int = 0
        self._total_ingested: int = 0
        self.name = "Numeric Processor"

    def validate(self, data: Any) -> bool:
        def is_valid_number(x: Any) -> bool:
            return isinstance(x, (int, float)) and not isinstance(x, bool)
        if is_valid_number(data):
            return True
        if isinstance(data, list) and len(data) > 0:
            return all(is_valid_number(x) for x in data)
        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Got exception: improper numeric data")
        if isinstance(data, list):
            for i in data:
                self._validated.append((self._processing_rank, str(i)))
                self._processing_rank += 1
                self._total_ingested += 1
        else:
            self._validated.append((self._processing_rank, str(data)))
            self._processing_rank += 1
            self._total_ingested += 1

    def output(self) -> tuple[int, str]:
        if not self._validated:
            raise IndexError("All data extracted from numeric processor")
        return self._validated.pop(0)


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        self._validated: list[tuple[int, str]] = []
        self._processing_rank: int = 0
        self._total_ingested: int = 0
        self.name = "Text Processor"

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return len(data.strip()) > 0
        if isinstance(data, list) and len(data) > 0:
            return all(isinstance(x, str) and len(x.strip()) > 0 for x in data)
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Got exception: improper text data")
        if isinstance(data, list):
            for i in data:
                self._validated.append((self._processing_rank, str(i)))
                self._processing_rank += 1
                self._total_ingested += 1
        else:
            self._validated.append((self._processing_rank, str(data)))
            self._processing_rank += 1
            self._total_ingested += 1

    def output(self) -> tuple[int, str]:
        if not self._validated:
            raise IndexError("All data extracted from text processor")
        return self._validated.pop(0)


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        self._validated: list[tuple[int, str]] = []
        self._processing_rank: int = 0
        self._total_ingested: int = 0
        self.name = "Log Processor"

    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return True
        if isinstance(data, list) and len(data) > 0:
            return all(isinstance(x, dict) for x in data)
        return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Got exception: improper log data")
        if isinstance(data, list):
            for i in data:
                formatted = f"{i['log_level']}: {i['log_message']}"
                self._validated.append((self._processing_rank, formatted))
                self._processing_rank += 1
                self._total_ingested += 1
        else:
            formatted = f"{data['log_level']}: {data['log_message']}"
            self._validated.append((self._processing_rank, formatted))
            self._processing_rank += 1
            self._total_ingested += 1

    def output(self) -> tuple[int, str]:
        if not self._validated:
            raise IndexError("All data extracted from log processor")
        return self._validated.pop(0)


def main() -> None:
    print("=== Code Nexus - Data Processor ===")

    print("Testing Numeric Processor...")
    numeric = NumericProcessor()
    print(f"Trying to validate input '42': {numeric.validate(42)}")
    print(f"Trying to validate input 'Hello': {numeric.validate('Hello')}")
    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        numeric.ingest("foo")
    except ValueError as e:
        print(e)
    data = [1, 2, 3, 4, 5]
    print(f"Processing data: {data}")
    numeric.ingest(data)
    print("Extracting 3 values...")
    for _ in range(3):
        rank, value = numeric.output()
        print(f"Numeric value {rank}: {value}")

    print("Testing Text Processor...")
    text = TextProcessor()
    print(f"Trying to validate input '42': {text.validate(42)}")
    data = ['Hello', 'Nexus', 'World']
    print(f"Processing data: {data}")
    text.ingest(data)
    print("Extracting 1 value...")
    rank, value = text.output()
    print(f"Text value {rank}: {value}")

    print("Testing Log Processor...")
    log = LogProcessor()
    print(f"Trying to validate input 'Hello': {log.validate('Hello')}")
    data = [
        {'log_level': 'NOTICE', 'log_message': 'Connection to server'},
        {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}
    ]
    print(f"Processing data: {data}")
    log.ingest(data)
    print("Extracting 2 values...")
    for _ in range(2):
        rank, value = log.output()
        print(f"Log entry {rank}: {value}")


if __name__ == "__main__":
    main()
