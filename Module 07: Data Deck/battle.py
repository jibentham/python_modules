from ex0 import Creature, CreatureFactory, FlameFactory, AquaFactory


def verify_factory(factory: CreatureFactory) -> None:
    base = factory.create_base()
    evolved = factory.create_evolved()

    for creature in (base, evolved):
        print(creature.describe())
        print(creature.attack())
        print()


def creature_fight(factory1: CreatureFactory, factory2: CreatureFactory) -> None:
    creature1 = factory1.create_base()
    creature2 = factory2.create_base()

    print(f"--- Fight: {creature1.creature_name} vs {creature2.creature_name} ---")
    print(creature1.attack())
    print(creature2.attack())


def main() -> None: 
    flame_factory = FlameFactory()
    aqua_factory = AquaFactory()

    verify_factory(flame_factory)
    verify_factory(aqua_factory)

    creature_fight(flame_factory, aqua_factory)


if __name__ == "__main__":
    main()
