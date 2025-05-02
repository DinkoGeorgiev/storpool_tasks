from typing import Generator


def recursive_fizzbuzz(start: int, end: int) -> Generator[str | int, None, None]:  # Keep py < 3.13 happy
    """Recursive implementation of fizzbuzz-like logic.

    :param start: The first number to process
    :param end: The last number to process
    """
    output = ""
    output += start % 3 == 0 and "A" or ""
    output += start % 5 == 0 and "B" or ""
    output = output or start
    yield output
    yield from start < end and recursive_fizzbuzz(start + 1, end) or []


def map_fizzbuzz(start: int, end: int) -> map:
    """Map-based implementation of fizzbuzz-like logic.

    :param start: The first number to process
    :param end: The last number to process
    :credits: https://dev.to/nombrekeff/challenge-fizzbuzz-without-if-else-33c8#comment-126cf
    """
    return map(
        lambda x: {
            1: x,
            6: "A",
            10: "B",
            0: "AB",
        }[x**4 % 15],
        range(start, end + 1),
    )


if __name__ == "__main__":
    print(list(recursive_fizzbuzz(1, 100)))
