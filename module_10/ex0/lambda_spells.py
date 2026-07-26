def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts, key=lambda artifact: artifact["power"], reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda mage: mage["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda s: "* " + s + " *", spells))


def mage_stats(mages: list[dict]) -> dict:
    powers = list(map(lambda mage: mage["power"], mages))
    return {
        "max_power": max(mages, key=lambda mage: mage["power"]),
        "min_power": min(mages, key=lambda mage: mage["power"]),
        "average_power": sum(powers) / len(powers),
    }


def main() -> None:
    artifacts = [
        {"name": "Light Prism", "power": 74, "type": "weapon"},
        {"name": "Lightning Rod", "power": 114, "type": "relic"},
        {"name": "Light Prism", "power": 80, "type": "accessory"},
        {"name": "Earth Shield", "power": 114, "type": "accessory"},
    ]
    mages = [
        {"name": "Casey", "power": 97, "element": "lightning"},
        {"name": "Ember", "power": 90, "element": "ice"},
        {"name": "Nova", "power": 98, "element": "fire"},
        {"name": "Alex", "power": 74, "element": "water"},
        {"name": "Sage", "power": 69, "element": "earth"},
    ]
    spells = ["darkness", "fireball", "tornado", "earthquake"]

    print(artifact_sorter(artifacts))
    print("\n")
    print(power_filter(mages, 92))
    print("\n")
    print(spell_transformer(spells))
    print("\n")
    print(mage_stats(mages))


if __name__ == "__main__":
    main()