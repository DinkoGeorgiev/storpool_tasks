# storpool_tasks
Results and solutions to 4 challenges provided by StorPool.


## 1. Counting

### Description

A python program that takes as input a binary file containing 32-bit integer numbers stored as uint32_t.
The implementation aims to strike a balance between memory usage, speed and simplicity of implementation.

For 1 billion items (file size is 4,000,000,000 bytes), the program takes about 3-4 minutes on laptop with average specs and uses around 1.5GB ram, 1GB of which are for the helper bitarrays.

Current bottlenecks are the many bitarrays get/set method calls, along with python's inherent slower loops.


### Usage

`python storpool_tasks/counting/countreader.py -i input_file`

There is a `-v` option to log some basic additional info. Please refer to the included usage information for more details.



## 2. Fizzbuzz

### Description

A python program that outputs the numbers from 1 to 100. If the number is divisible by 3, instead
of it prints “A”, if it’s divisible by 5 - “B”, if it’s divisible by 15 - “AB”.

Two implementations are supplied without using conditionals/ifs, including for/while loops.

### Usage

`python storpool_tasks/fizzbuzz/fizzbuzz.py`

_See also_ `tests/fizzbuzz/test_fizzbuzz.py`


## 3. Large compressed json analysis

### Description

At https://quiz.storpool.com/bigf.json.bz2 there is a compressed JSON fine. In it are described
disks with their model and serial number. A bash script is included to count how many models there are and how many
times each one is present. Results and statistics of one of the test runs are included in `scripts/analysis/number_disks_per_model.txt`

Based on preliminary analysis of the file contents, it was determined that the number of unique models present is low. This means that all models can be counted directly with command line tools without requiring optimizations for memory.

### Requirements

The script utilizes the following standard programs
* __bzcat__: for decompressing the .bz2 file
* __grep__: To extract the disk model from each record.
* __tr__: The file has no new lines and standard grep does not have a way to set an arbitrary line delimiter. We work around this by replacing `}` with '\n' using `tr`
* __awk__: For the actual counting. It was chosen for its decent performance and implementation simplicity.
* __cat__: As a place holder when `pv` is not available (see below)
* __which__: To discover optional dependencies

In addition, the following optional tools are also used if available

* __pbzcat__: The file seems to be compressed using it or similar tool, as decompression speed is greatly increased.
* __lbzcat__: If found will be used instead of missing `pbzcat`
* __pv__: If available will be used to display basic info about the rate at which the decompressed data flows through the pipeline.

### Usage

See included help for details: `./scripts/analysis/disk_models_counter.sh -h`

Examples:

* Process the file without storing it to disk (can be slow, depending on the download speed)
  * `wget -O - https://quiz.storpool.com/bigf.json.bz2 | ./scripts/analysis/disk_models_counter.sh -`
* Process file stored on disk
  * `./scripts/analysis/disk_models_counter.sh ./bigf.json.bz2`
* Process part of the file on disk
  * `head -c 2048000 ./bigf.json.bz2 | ./scripts/analysis/disk_models_counter.sh -`
  * __Note:__ _This will likely trigger a premature EOF error from the decompressor, but disk model counts for the successfully extracted part will be displayed)_

## 4. Reverse engineering

### Description

At https://quiz.storpool.com/binaries.tgz there’s an archive with two executable binary files that
crash in different ways.

Analysis of the two binaries can be found in `reverse_engineering/` directory.

## Unit tests

### Tox

The recommended way to run the included python unit tests is through tox. The code has been tested with python 3.13 and 3.12.

* In a virtual environment `pip install tox`
* `tox`

### pytest

Alternatively, tests can be run directly with `pytest`

* In a virtual environment `pip install pytest`
* `pytest`
