import sys
import random
from collections.abc import Callable
from typing import Any
from functools import reduce, partial, lru_cache, singledispatch
from operator import add, mul
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data_generator import FuncMageDataGenerator


def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        raise ValueError("spells list cannot be empty")
    if operation == "add":
        return reduce(add, spells)
    elif operation == "multiply":
        return reduce(mul, spells)
    elif operation == "max":
        return reduce(max, spells)
    elif operation == "min":
        return reduce(min, spells)
    else:
        raise ValueError(f"unknown operation:{operation}")


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    fire_enchant = partial(base_enchantment, power=50, element="fire")
    ice_enchant = partial(base_enchantment, power=50, element="ice")
    lightning_enchant = partial(
        base_enchantment, power=50, element="lightning"
    )
    return {
        "fire": fire_enchant,
        "ice": ice_enchant,
        "lightning": lightning_enchant,
    }


@lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:
    @singledispatch
    def process(data):
        return f"Unknown spell type: {data}\n"

    @process.register
    def _(data: int) -> str:
        return f"damage spell did {data} damage\n"

    @process.register
    def _(data: str) -> str:
        return f"spell enchanted with {data}\n"

    @process.register
    def _(data: list) -> str:
        return f"spell multi casted: {len(data)}\n"

    return process


def main() -> None:
    def base_enchantment(item: str = "Sword", power: int = 0, element: str = "") -> str:
        return f"{item} enchanted with {element} ({power} power)"

    spell_powers = FuncMageDataGenerator.generate_spell_powers(6)
    operations = ["add", "multiply", "max", "min"]
    fibonacci_tests = [random.randint(8, 20) for _ in range(3)]
    enchants = partial_enchanter(base_enchantment)
    process = spell_dispatcher()

    for op in operations:
        print(f"{op}: {spell_reducer(spell_powers, op)}")
    print()
    for name, enchant_fn in enchants.items():
        print(enchant_fn(item="Sword"))
    print()
    for n in fibonacci_tests:
        print(f"fibonacci({n}) = {memoized_fibonacci(n)}")
    print()
    print(process(42))
    print(process("fireball"))
    print(process([1, 2, 3]))


if __name__ == "__main__":
    main()
