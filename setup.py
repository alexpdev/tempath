#! /usr/bin/python3
# -*- coding: utf-8 -*-

#############################################################################
# Copyright (C) 2021 alexpdev
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
############################################################################

from setuptools import setup, find_packages, find_namespace_packages
import json

INFO = json.load(open('./package.json'))

def readme():
    with open("README.md", encoding="UTF-8") as fd:
        long_description = fd.read()
    return long_description

setup(
    name=INFO['name'],
    version=INFO['version'],
    description=INFO['description'],
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
    ],
    keywords=INFO["keywords"],
    author=INFO["author"],
    author_email=INFO["email"],
    url=INFO["url"],
    project_urls={"Source Code": "https://github.com/alexpdev/autotestdir"},
    license=INFO["license"],
    packages=find_packages(),
    tests_require=['pytest'],
    test_suite='pytest',
    include_package_data=True,
    setup_requires=["setuptools"],
    zip_safe=False,
    python_requires='>=3.1',
)
