import array
import logging
import sys
from argparse import ArgumentParser

from bitarray import bitarray

UINT32_RANGE = 2**32


def process_input(filename, seen_once, seen_multiple, chunk_size=4 * 1024 * 1024):
    with open(filename, "rb") as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break

            numbers = array.array("I")
            numbers.frombytes(data)

            for num in numbers:
                if not seen_once[num]:
                    seen_once[num] = True
                else:
                    seen_multiple[num] = True


def get_counts(input_file):
    logging.debug("Allocating bitarrays (~1GB RAM) ...")

    seen_once = bitarray(UINT32_RANGE, endian="little")
    seen_multiple = bitarray(UINT32_RANGE, endian="little")
    seen_once.setall(False)
    seen_multiple.setall(False)

    logging.debug("Processing input file %r ...", input_file)
    process_input(input_file, seen_once, seen_multiple)

    logging.debug("Counting results ...")

    total_seen = seen_once.count()
    seen_multiple_count = (seen_once & seen_multiple).count()

    unique = (seen_once | seen_multiple).count()
    seen_once_only = total_seen - seen_multiple_count
    return unique, seen_once_only


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i, --input-file", dest="input_file", required=True, help="Input file")
    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", default=False, help="Log more information"
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(asctime)s %(message)s")
    try:
        unique_count, seen_once_count = get_counts(input_file=args.input_file)
    except EnvironmentError as exc:
        sys.exit(exc)

    print(f"Number of unique values: {unique_count}")
    print(f"Number of values seen only once: {seen_once_count}")
    print(f"Number of values found more than once: {unique_count - seen_once_count}")
