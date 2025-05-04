import sys
import tempfile

import pytest

from storpool_tasks.counting.countreader import get_counts

# pylint: disable=missing-function-docstring


def write_uint32(destination_file, values, bytes_per_value=4):
    with open(destination_file, "wb") as out_file:
        for val in values:
            out_file.write(val.to_bytes(length=bytes_per_value, byteorder=sys.byteorder, signed=False))


@pytest.mark.parametrize(
    "values,expected_unique,expected_seen_once",
    [
        # Mixed input
        ([127, 128, 255, 127, 127, 0], 4, 3),
        # Single repeated value
        ([123456] * 1_000, 1, 0),
        # All unique
        (list(range(2000)), 2000, 2000),
        # Empty file
        ([], 0, 0),
    ],
)
def test_get_counts(values, expected_unique, expected_seen_once):
    with tempfile.NamedTemporaryFile(delete_on_close=False) as fp:
        write_uint32(fp.name, values, bytes_per_value=4)
        fp.close()
        n_distinct, n_unique = get_counts(input_file=fp.name)
        assert n_distinct == expected_unique
        assert n_unique == expected_seen_once
