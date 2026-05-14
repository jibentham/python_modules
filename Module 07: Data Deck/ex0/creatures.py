from abc import ABC, abstractmethod


class Creature(ABC):
    creature_name: str = ""
    creature_type: str = ""

    @abstractmethod
    def attack(self) -> str:
        ...
    
    def describe(self) -> str:
        return (f"{self.creature_name} is a {self.creature_type} type Creature")


class Flameling(Creature):
    creature_name = "Flameling"
    creature_type = "Fire"

    def attack(self) -> str:
        return (f"{self.creature_name} uses Ember!")


class Pyrodon(Creature):
    creature_name = "Pyrodon"
    creature_type = "Fire/Flying"

    def attack(self) -> str:
        return (f"{self.creature_name} uses Flamethrower!")


class Aquabub(Creature):
    creature_name = "Aquabub"
    creature_type = "Water"

    def attack(self) -> str:
        return (f"{self.creature_name} uses Water Gun!")


class Torragon(Creature):
    creature_name = "Torragon"
    creature_type = "Water"

    def attack(self) -> str:
        return (f"{self.creature_name} uses Hydro Pump!")
