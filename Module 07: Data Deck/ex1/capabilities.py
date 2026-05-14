from abc import ABC, abstractmethod


class HealCapability(ABC):

    @abstractmethod
    def heal(self) -> str:
        ...


class TransformCapability(ABC):
    creature_morphed: int = 0

    @abstractmethod
    def transform(self) -> str:
        ...

    @abstractmethod
    def revert(self) -> str:
        ...