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


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []
        self._routed: int = 0
        self._rejected: int = 0

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def print_processors_stats(self) -> None:
        for processor in self._processors:
            print(f"{processor.name}: total {len(processor._validated)} processed, {len(processor._validated)} remain on processor.")

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
                    except ValueError as e:
                        print(f"processor rejected '{element}'")
            if not routed:
                self._rejected += 1
                print(f"No processor could handle '{element}'")
        self.print_processors_stats()


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        self._validated: list[tuple[int, str]] = []
        self._processing_rank: int = 0
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
        else:
            self._validated.append((self._processing_rank, str(data)))
    
    def output(self) -> tuple[int, str]:
        if not self._validated:
            raise IndexError("All data extracted from numeric processor")
        return self._validated.pop(0)


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        self._validated: list[tuple[int, str]] = []
        self._processing_rank: int = 0
        self.name = "Text Processor"

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return len(data.strip()) > 0
        if isinstance(data, list) and len(data) > 0:
            return all(isinstance(x, str) and len(x.strip()) > 0 for x in data)

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Got exception: improper text data")
        if isinstance(data, list):
            for i in data:
                self._validated.append((self._processing_rank, str(i)))
                self._processing_rank += 1
        else:
            self._validated.append((self._processing_rank, str(data)))
    
    def output(self) -> tuple[int, str]:
        if not self._validated:
            raise IndexError("All data extracted from text processor")
        return self._validated.pop(0)


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        self._validated: list[tuple[int, str]] = []
        self._processing_rank: int = 0
        self.name = "Log Processor"

    def validate(self, data: Any) -> bool:
        return isinstance(data, dict)

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Got exception: improper log data")
        if isinstance(data, list):
            for i in data:
                self._validated.append((self._processing_rank, str(i)))
                self._processing_rank += 1
        else:
            self._validated.append((self._processing_rank, str(data)))
    
    def output(self) -> tuple[int, str]:
        if not self._validated:
            raise IndexError("All data extracted from log processor")
        return self._validated.pop(0)
    

def main() -> None:
    stream = DataStream()
    stream.register_processor(NumericProcessor())
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())

    stream.process_stream([
        "Hello World",
        [3.14, -1, 2.71],
        {'log_level': 'WARNING', 'log_message': 'Telnet Access! Use ssh instead'},
        {'log_level': 'INFO', 'log_message': 'User wil is connected'},
        42,
        ["Hi", "five"]
    ])


if __name__ == "__main__":
    main()
