from ex0 import CreatureFactory, FlameFactory, AquaFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import BattleStrategy, NormalStrategy, AggressiveStrategy, DefensiveStrategy


def battle(opponents: list[tuple[CreatureFactory, BattleStrategy]], label: str = "") -> None:

    roster = [(factory.create_base(), strategy) for factory, strategy in opponents]

    print("*** Tournament ***")
    print(f"{len(roster)} opponents involved")

    for i, (creature1, strategy1) in enumerate(roster):
        for j, (creature2, strategy2) in enumerate(roster):
            if j <= i:
                continue

            print("* Battle *")
            print(f"{creature1.describe()}")
            print("vs.")
            print(f"{creature2.describe()}")
            print("now fight!")

            result1 = strategy1.act(creature1)
            result2 = strategy2.act(creature2)

            if not strategy1.is_valid(creature1):
                print(result1)
                return
            if not strategy2.is_valid(creature2):
                print(result2)
                return

            print(result1)
            print(result2)
            print()


def main() -> None:
    print("Tournament 0 (basic)")
    t0 = [(FlameFactory(), NormalStrategy()), (HealingCreatureFactory(), DefensiveStrategy())]
    print("[ (Flameling+Normal), (Healing+Defensive) ]")
    battle(t0)
    print()

    # Tournament 1 - error
    print("Tournament 1 (error)")
    t1 = [(FlameFactory(), AggressiveStrategy()), (HealingCreatureFactory(), DefensiveStrategy())]
    print("[ (Flameling+Aggressive), (Healing+Defensive) ]")
    battle(t1)
    print()

    # Tournament 2 - multiple
    print("Tournament 2 (multiple)")
    t2 = [
        (AquaFactory(), NormalStrategy()),
        (HealingCreatureFactory(), DefensiveStrategy()),
        (TransformCreatureFactory(), AggressiveStrategy())
    ]
    print("[ (Aquabub+Normal), (Healing+Defensive), (Transform+Aggressive) ]")
    battle(t2)


if __name__ == "__main__":
    main()
