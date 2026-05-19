from abc import ABC, abstractmethod
from ex0 import Creature
from ex1 import HealCapability, TransformCapability


class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        ...

    @abstractmethod
    def act(self, creature: Creature) -> str:
        ...


class NormalStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return callable(creature.attack)

    def act(self, creature: Creature) -> str:
        if self.is_valid(creature):
            return creature.attack()
        return f"Aborting tournament: creature {creature.creature_name} cannot use this strategy."


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> str:
        if self.is_valid(creature):
            return f"{creature.transform()} {creature.attack()} {creature.revert()}"
        return f"Aborting tournament: creature {creature.creature_name} cannot use this strategy."


class DefensiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, HealCapability)

    def act(self, creature: Creature) -> str:
        if self.is_valid(creature):
            return f"{creature.attack()} {creature.heal()}"
        return f"Aborting tournament: creature {creature.creature_name} cannot use this strategy."
