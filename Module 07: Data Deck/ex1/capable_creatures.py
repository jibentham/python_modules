from ex0.creatures import Creature
from .capabilities import HealCapability, TransformCapability

class Sproutling(Creature, HealCapability):
    creature_name = "Sproutling"
    creature_type = "Grass"

    def attack(self) -> str:
        return (f"{self.creature_name} uses Vine Whip!")

    def heal(self) -> str:
        return (f"{self.creature_name} heals itself for a small amount")


class Bloomelle(Creature, HealCapability):
    creature_name = "Bloomelle"
    creature_type = "Grass/Fairy"

    def attack(self) -> str:
        return (f"{self.creature_name} uses Petal Dance!")

    def heal(self) -> str:
        return (f"{self.creature_name} heals itself and others for a large amount")


class Shiftling(Creature, TransformCapability):
    creature_name = "Shiftling"
    creature_type = "Normal"
    creature_morphed = 0

    def attack(self) -> str:
        if self.creature_morphed == 0:
            return (f"{self.creature_name} attacks normally")
        else:
            return (f"{self.creature_name} performs a boosted strike!")

    def transform(self) -> str:
        self.creature_morphed = 1
        return (f"{self.creature_name} shifts into a sharper form!")

    def revert(self) -> str:
        self.creature_morphed = 0
        return (f"{self.creature_name} returns to normal")


class Morphagon(Creature, TransformCapability):
    creature_name = "Morphagon"
    creature_type = "Normal/Dragon"
    creature_morphed = 0

    def attack(self) -> str:
        if self.creature_morphed == 0:
            return (f"{self.creature_name} attacks normally")
        else:
            return (f"{self.creature_name} unleashes a devastating morph strike!")

    def transform(self) -> str:
        self.creature_morphed = 1
        return (f"{self.creature_name} morphs into a dragonic battle form!")

    def revert(self) -> str:
        self.creature_morphed = 0
        return (f"{self.creature_name} stabilizes its form")