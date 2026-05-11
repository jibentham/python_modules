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


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []
        self._routed: int = 0

    def register_processor(self, proc: DataProcessor) -> None:
        print(f"Registering {proc.name}\n")
        self._processors.append(proc)

    def print_processors_stats(self) -> None:
        print("=== Data Stream Statistics ===")
        if not self._processors:
            print("No processor found, no data\n")
            return
        for processor in self._processors:
            print(
                f"""{processor.name}:
                 total {processor._total_ingested} processed,
                 {len(processor._validated)} remain on processor."""
                )
        print("\n")

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            routed = False
            for proc in self._processors:
                if proc.validate(element):
                    try:
                        proc.ingest(element)
                        self._routed += 1
                        routed = True
                        break
                    except ValueError:
                        pass
            if not routed:
                print(f"No processor could handle '{element}'")
        self.print_processors_stats()


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
    stream = DataStream()
    batch = [
        "Hello World",
        [3.14, -1, 2.71],
        {'log_level': 'WARNING', 'log_message':
         'Telnet Access! Use ssh instead'},
        {'log_level': 'INFO', 'log_message': 'User wil is connected'},
        42,
        ["Hi", "five"]
    ]

    print("=== Code Nexus - Data Stream ===\n")
    print("Initializing Data Stream...")
    stream.process_stream(batch)
    stream.register_processor(NumericProcessor())
    stream.process_stream(batch)
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())
    stream.process_stream(batch)

    print(
        """Consume some elements from the data processors:
         Numeric 3, Text 2, Log 1"""
        )
    for _ in range(3):
        stream._processors[0].output()
    for _ in range(2):
        stream._processors[1].output()
    for _ in range(1):
        stream._processors[2].output()

    stream.print_processors_stats()


if __name__ == "__main__":
    main()
