try:
    import alchemy.grimoire.dark_spellbook
    print(alchemy.grimoire.dark_spellbook.dark_spell_record("Tenebris", "bats and arsenic"))
except Exception as e:
    print(f"💥 Laboratory explosion: {type(e).__name__}: {e}")