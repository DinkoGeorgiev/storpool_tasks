#!/usr/bin/env bash

set -e
set -b

usage="""Usage:

\t$(basename "$0") input_file

Script to analyze a .bz2 json file like the one at https://quiz.storpool.com/bigf.json.bz2.
In the input file are described disks with their model and serial number.
The script counts and prints how many models there are and how many times each one is present.

Specify - as input_file to read from stdin

\tE.g.: wget -O - https://quiz.storpool.com/bigf.json.bz2 | "$0" -

Optional requirements:

\tpbzcat (preferred) or lbzcat will be used for decompression instead of bzcat if available.
\tpv will be used for basic decompression progress rate display if available.

"""

while :
do
    case "$1" in
      -h | --help)
          echo -e "$usage"
          exit 0
          ;;
      *)  # No more expected options
          break
          ;;
    esac
done

decompressor="bzcat"
# check if faster decompressor is available.
which lbzcat &> /dev/null && decompressor="lbzcat"
# The file seems to be compressed/benefit from pbzcat, so prefer it.
which pbzcat &> /dev/null && decompressor="pbzcat"
echo "Using ${decompressor} for decompression..." >&2


progress="cat"
# Use pv if found to display progress rate of decompressed data.
which pv &> /dev/null && progress='pv -tr'

input_file="${1:?Please specify input .bz2 file or - to read from stdin. Run with -h for more details.}"

if [ "${input_file}" != "-" ]; then
  # Only pbzcat will handle stdin with -- -, the others will treat it literary causing errors
  decompressor="${decompressor} --"
fi

echo
export LC_ALL=C  # Speed up grep, as the file does not appear to contain non-ascii characters.
${decompressor} "${input_file}" |${progress}|tr '}' '\n' |grep --color=never -o '"model":"[^"]\+"' |awk '{!seen[$0]++}END{for (i in seen) print i, seen[i]}'
