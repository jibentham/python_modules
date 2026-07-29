import sys
import random
import time
from functools import wraps
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data_generator import FuncMageDataGenerator


def spell_timer(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Casting {func.__name__}...")
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"Spell completed in {elapsed} seconds")
        return result
    return wrapper


def power_validator(min_power: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, spell_name: str, power: int) -> str:
            if power >= min_power:
                return func(self, spell_name, power)
            return "Insufficient power for this spell"
        return wrapper
    return decorator


def retry_spell(max_attempts: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func) 
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt < max_attempts:
                        print(
                            f"Spell failed, retrying... "
                            f"(attempt {attempt}/{max_attempts})"
                        )
            return f"Spell casting failed after {max_attempts} attempts"
        return wrapper
    return decorator


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        return len(name) >= 3 and all(c.isalpha() or c == " " for c in name)

    @power_validator(min_power=10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


def main() -> None:
    @spell_timer
    def slow_spell():
        time.sleep(0.1)
        return "Meteor summoned!"
    
    attempt_count = {"n": 0}
    @retry_spell(max_attempts=3)
    def unstable_spell():
        attempt_count["n"] += 1
        if attempt_count["n"] < 2:
            raise RuntimeError("Spell backfired")
        return "Spell stabilized"

    test_powers = [random.randint(5, 30) for _ in range(4)]
    spell_names = random.sample(FuncMageDataGenerator.SPELL_NAMES, 4)
    mage_names = random.sample(FuncMageDataGenerator.MAGE_NAMES, 6)
    invalid_names = ["Jo", "A", "Alex123", "Test@Name"]
    guild = MageGuild()
    
    for spell_name, power in zip(spell_names, test_powers):
        print(guild.cast_spell(spell_name, power))
    print()
    for name in mage_names + invalid_names:
        print(f"{name}: {MageGuild.validate_mage_name(name)}")
    print()
    print(slow_spell())
    print()
    print(unstable_spell())


if __name__ == "__main__":
    main()
