from typing import Callable, Any
from functools import reduce, partial, lru_cache, singledispatch
from operator import add, mul


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