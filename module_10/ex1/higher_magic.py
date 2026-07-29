import sys
import random
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data_generator import FuncMageDataGenerator


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    def combined(target: str, power: int) -> tuple:
        return (spell1(target, power), spell2(target, power))
    return combined


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    def amplified(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)
    return amplified


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    def cast(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        else:
            return "Spell fizzled"
    return cast


def spell_sequence(spells: list[Callable]) -> Callable:
    def ordered(target: str, power: int) -> list:
        return [spell(target, power) for spell in spells]
    return ordered


def main() -> None:
    def fireball(target: str, power: int) -> str:
        return f"{target} hit by fireball for {power} damage"
    
    def freeze(target: str, power: int) -> str:
        return f"{target} frozen with {power} power"
    
    def is_strong_enough(target: str, power: int) -> bool:
        return power >= 30
    
    test_powers = FuncMageDataGenerator.generate_spell_powers(3)
    test_targets = random.sample(FuncMageDataGenerator.MAGE_NAMES, 3)
    combined = spell_combiner(fireball, freeze)
    amplified = power_amplifier(fireball, 2)
    conditional = conditional_caster(is_strong_enough, fireball)
    sequence = spell_sequence([fireball, freeze])
    
    for target, power in zip(test_targets, test_powers):
        print(combined(target, power))
        print(amplified(target, power))
        print(conditional(target, power))
        print(sequence(target, power))
        print()


if __name__ == "__main__":
    main()
