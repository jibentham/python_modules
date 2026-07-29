import sys
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data_generator import FuncMageDataGenerator


def mage_counter() -> Callable:
    count = 0

    def countmg() -> int:
        nonlocal count
        count += 1
        return count

    return countmg


def spell_accumulator(initial_power: int) -> Callable:
    total = initial_power

    def curr_power(amount: int) -> int:
        nonlocal total
        total += amount
        return total

    return curr_power


def enchantment_factory(enchantment_type: str) -> Callable:
    def apply(item: str) -> str:
        return enchantment_type + item

    return apply


def memory_vault() -> dict[str, Callable]:
    mem: dict[str, object] = {}

    def store(key: str, value: object) -> None:
        mem[key] = value

    def recall(key: str) -> object:
        if key in mem:
            return mem[key]
        return "ERROR: key not found"

    return {"store": store, "recall": recall}


def main() -> None:
    counter = mage_counter()
    initial_power = FuncMageDataGenerator.generate_spell_powers(1)[0]
    power_additions = FuncMageDataGenerator.generate_spell_powers(5)
    accumulate = spell_accumulator(initial_power)
    enchantment_types = FuncMageDataGenerator.ENCHANTMENT_TYPES
    items_to_enchant = FuncMageDataGenerator.generate_enchantment_items(4)
    vault = memory_vault()
    mages = FuncMageDataGenerator.generate_mages(3)

    for _ in range(4):
        print(f"Mage count: {counter()}")
    print()
    print(f"Starting power: {initial_power}")
    for amount in power_additions:
        print(f"Adding {amount} -> total: {accumulate(amount)}")
    print()
    for enchantment_type in enchantment_types[:3]:
        enchanter = enchantment_factory(enchantment_type)
        for item in items_to_enchant:
            print(enchanter(item))
    print()
    for i, mage in enumerate(mages):
        vault["store"](f"mage_{i}", mage)
    for i in range(len(mages)):
        print(f"Recalled mage_{i}: {vault['recall'](f"mage_{i}")}")
    print(f"Recalled missing key: {vault['recall']('nonexistent')}")


if __name__ == "__main__":
    main()
