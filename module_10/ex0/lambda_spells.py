import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data_generator import FuncMageDataGenerator


def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(
        artifacts, key=lambda artifact: artifact["power"], reverse=True
        )


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
    artifacts = FuncMageDataGenerator.generate_artifacts(4)
    mages = FuncMageDataGenerator.generate_mages(5)
    spells = FuncMageDataGenerator.generate_spells(4)

    print(artifact_sorter(artifacts))
    print("\n")
    print(power_filter(mages, 92))
    print("\n")
    print(spell_transformer(spells))
    print("\n")
    print(mage_stats(mages))


if __name__ == "__main__":
    main()
