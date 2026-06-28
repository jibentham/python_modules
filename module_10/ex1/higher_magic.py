def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    def combined(target: str, power: int) -> tuple:
        return(spell1(target, power), spell2(target, power))
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
            return ("Spell fizzled")
    return cast


def spell_sequence(spells: list[Callable]) -> Callable:
    def ordered(target: str, power: int) -> list:
        return [spell(target, power) for spell in spells]
    return ordered


def main() -> None:
    


if __name__ == "__main__":
    main()

