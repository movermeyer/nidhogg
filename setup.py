import io
import re
from os.path import dirname, join

from setuptools import setup


def read(*args):
    return (
        io
        .open(join(dirname(__file__), *args))
        .read()
    )


setup(
    name="flask-nidhogg",
    version="1.1.1",
    license="GPLv3",
    description="OpenSource Yggdrasil protocol implementation",
    long_description="{}\n{}".format(
        read("README.rst"),
        re.sub(":obj:`~?(.*?)`", r"``\1``", read("CHANGELOG.rst"))
    ),
    author="Andriy Kushnir",
    author_email="orhideous@gmail.com",
    url="https://github.com/Orhideous/flask-nidhogg",
    packages=["nidhogg"],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: No Input/Output (Daemon)",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Utilities",
    ],
    keywords=["Minecraft", "Yggdrasil", "Authentication", ],
    install_requires=read("requirements.txt").splitlines(),
)
