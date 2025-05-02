#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""setup"""

from os.path import abspath, dirname
from os.path import join as pjoin

from setuptools import find_packages, setup


def main():
    """setuptools setup"""
    here = abspath(dirname(__file__))
    name = "storpool_tasks"
    with open(pjoin(here, name, "__init__.py"), "r", encoding="utf-8") as src:
        data = [i for i in src.readlines() if i.startswith("__")]
    meta = dict((i[0].strip(), i[1].strip().strip("'\"")) for i in (ln.split("=", 1) for ln in data))
    setup(
        name=name,
        version=meta["__version__"],
        author=meta["__author__"],  # Optional
        maintainer=meta["__maintainer__"],  # Optional
        packages=find_packages(include=[name, name + ".*"]),
    )


if __name__ == "__main__":
    main()
