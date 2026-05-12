from .dark_spellbook import dark_spell_allowed_ingredients

def dark_validate_ingredients(ingredients: str) -> str:
    for x in light_spell_allowed_ingredients():
        if x.lower() == ingredients.lower():
            return ("VALID")
    return ("INVALID")
