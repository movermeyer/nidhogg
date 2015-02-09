#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
from os.path import dirname, join


def read(*args):
    return io.open(join(dirname(__file__), *args)).read()

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open("README.rst").read()
history = open("HISTORY.rst").read().replace(".. :changelog:", "")

requirements = read("requirements.txt").splitlines(),
test_requirements = read("test_requirements.txt").splitlines(),

setup(
    name="nidhogg",
    version="2.0.0",
    description="Open-source Minecraft server bootstrapping platform",
    long_description=readme + "\n\n" + history,
    author="Andriy Kushnir (Orhideous)",
    author_email="orhideous@gmail.com",
    url="https://github.com/Orhideous/nidhogg",
    packages=["nidhogg"],
    package_dir={"nidhogg": "nidhogg"},
    include_package_data=True,
    install_requires=requirements,
    license="GPLv3",
    zip_safe=False,
    keywords=["Minecraft", "Yggdrasil", "Authentication"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: No Input/Output (Daemon)",
        "Framework :: Pyramid",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Utilities",
    ],
    test_suite="tests",
    tests_require=test_requirements,
    entry_points="""
        [paste.app_factory]
        main = nidhogg.app:main
    """,
    paster_plugins=["pyramid"],
)
