from typing import Any, Protocol
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


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class CSVExport:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print(",".join([x[1] for x in data]))


class JSONExport:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        pass

class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []
        self._routed: int = 0
        self._rejected: int = 0

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

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

    def print_processors_stats(self) -> None:
        for processor in self._processors:
            print(f"{processor}: total {self._routed} processed, {self._rejected} remain on processor.")
    
    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self._processors:
            data_batch: list[tuple[int, str]] = []
            for _ in range(nb):
                try:
                    data_batch.append(proc.output())
                except IndexError:
                    break
            if data_batch:
                plugin.process_output(data_batch)


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        self._validated: list[tuple[int, str]] = []
        self._processing_rank: int = 0

    def validate(self, data: Any) -> bool:
        return isinstance(data, (int, float, list[int | float])) and not isinstance (data, bool)

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

    def validate(self, data: Any) -> bool:
        return isinstance(data, (str, list[str]))

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
            raise IndexError("All data extracted from numeric processor")
        return self._validated.pop(0)


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        self._validated: list[tuple[int, str]] = []
        self._processing_rank: int = 0

    def validate(self, data: Any) -> bool:
        return isinstance(data, (dict[str, str], list[dict[str, str]]))

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
            raise IndexError("All data extracted from numeric processor")
        return self._validated.pop(0)


def main() -> None:
    stream = DataStream()
    stream.register_processor(NumericProcessor())
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())

    stream.process_stream([
        "Hello World",
        [3.14, -1, 2.71],
        [{'log_level': 'WARNING', 'log_message': 'User wil is connected'}],
        42,
        ['Hi', 'five']
    ])
    print("=== Data Stream Statistics ===")
    stream.print_processors_stats()
    stream.output_pipeline(3, CSVExport)


if __name__ == "__main__":
    main()
