from ex1 import HealingCreatureFactory, TransformCreatureFactory


def heal_factory(factory: HealingCreatureFactory) -> None:
    base = factory.create_base()
    evolved = factory.create_evolved()

    for creature in (base, evolved):
        if creature == base:
            print("base:")
        if creature == evolved:
            print("evolved:")
        print(creature.describe())
        print(creature.attack())
        print(creature.heal())
        print()


def transform_factory(factory: TransformCreatureFactory) -> None:
    base = factory.create_base()
    evolved = factory.create_evolved()

    for creature in (base, evolved):
        if creature == base:
            print("base:")
        if creature == evolved:
            print("evolved:")
        print(creature.describe())
        print(creature.attack())
        print(creature.transform())
        print(creature.attack())
        print(creature.revert())
        print()


def main() -> None:

    healing_creature = HealingCreatureFactory()
    morphing_creature = TransformCreatureFactory()

    print("=== Testing creature with healing capability ===")
    heal_factory(healing_creature)
    print("=== Testing creature with transform capability ===")
    transform_factory(morphing_creature)


if __name__ == "__main__":
    main()
