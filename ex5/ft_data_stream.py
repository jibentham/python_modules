import random
from typing import Generator


def gen_event() -> Generator[tuple[str, str], None, None]:
    players: list = [
        "Alice", "Bob", "Dylan", "Charlie"
    ]
    actions: list = [
        "run", "climb", "swim", "move", "jump",
        "grab", "sleep", "eat"
    ]

    while True:
        yield (random.choice(players), random.choice(actions))


def consume_event(events: list[tuple[str, str]]) -> Generator[tuple[str, str], None, None]:
    while events:
        yield events.pop(random.randrange(len(events)))


def main() -> None:
    generator: Generator = gen_event()

    print("=== Game Data Stream Processor ===")
    for i in range(1, 1001):
        name: str
        action: str
        name, action = next(generator)
        print(f"Event {i:>4}: Player '{name}' did action '{action}'")

    n: int = 10
    events: list = [next(generator) for _ in range(n)]
    print(f"Built list of {n} events: {events}")

    consumed: Generator = consume_event(events)
    for event in consumed:
        print(f"Got event from list: {event}")
        print(f"Remains in list: {events}")


if __name__ == "__main__":
    main()
