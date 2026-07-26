from typing import Callable


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