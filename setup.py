#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from setuptools import setup, find_namespace_packages

test_deps = []
setup(
    name="netdiag",
    version="0.2.1",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    install_requires=[
        "click==7.1.2",
        "pydantic==1.6.1",
        "python-dotenv==0.13.0",
    ],
    entry_points={
      "console_scripts": ["netdiag = netdiag.__main__:main"]
    },
    extras_require={
        "test": test_deps,
    }
)
