#!/usr/bin/env python
#
#                      __   .__                    .___
# __  _  _____________|  | _|  |   _________     __| _/___________
# \ \/ \/ /  _ \_  __ \  |/ /  |  /  _ \__  \   / __ |/ __ \_  __ \
#  \     (  <_> )  | \/    <|  |_(  <_> ) __ \_/ /_/ \  ___/|  | \/
#   \/\_/ \____/|__|  |__|_ \____/\____(____  /\____ |\___  >__|
#                          \/               \/      \/    \/
#
# Copyright (c) 2018 Stephen Shao <Stephen.Shao@emc.com>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.  See http://www.gnu.org/copyleft/gpl.html for
# the full text of the license.

"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

setup(
    name = 'workloader',
    version = '1.1.3',
    keywords='WorkloadWisdom workloader LDX',
    description = 'A library to control Workload Wisdom through REST API',
    license = 'GPL License',
    url = 'https://eos2git.cec.lab.emc.com/shaos2/workloader',
    author = 'Stephen Shao',
    author_email = 'Stephen.Shao@emc.com',
    packages = find_packages(exclude=['docs', 'ext']),
    include_package_data = True,
    platforms = 'any',
    install_requires = ['requests'],
)
