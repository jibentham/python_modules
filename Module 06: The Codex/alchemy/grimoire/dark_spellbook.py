from alchemy.grimoire.dark_validator import dark_validate_ingredients

def dark_spell_allowed_ingredients() -> list[str]:
    return (["bats", "frogs", "arsenic", "eyeball"])


def dark_spell_record(spell_name: str, ingredients: str) -> str:
    if dark_validate_ingredients(ingredients) is "VALID":
        return (f"{spell_name} has been recorded.")
    else:
        return(f"{spell_name} has been rejected.")