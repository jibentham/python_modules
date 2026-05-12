from .light_spellbook import light_spell_allowed_ingredients

def validate_ingredients(ingredients: str) -> str:
    for x in light_spell_allowed_ingredients():
        if x.lower() == ingredients.lower():
            return ("VALID")
    return ("INVALID")
