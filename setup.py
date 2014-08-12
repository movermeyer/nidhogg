import io
import re
from os.path import dirname
from os.path import join

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()


requirements = [
    "Flask>=0.10.1",
    "Flask-SQLAlchemy==1.0",
    "SQLAlchemy==0.9.7",
    "PyMySQL==0.6.2"
]
setup(
    name="nidhogg",
    version="0.1.0",
    license="GPLv3",
    description="OpenSource Yggdrasil protocol implementation",
    long_description="%s\n%s" % (read("README.rst"), re.sub(":obj:`~?(.*?)`", r"``\1``", read("CHANGELOG.rst"))),
    author="Andriy Kushnir",
    author_email="orhideous@gmail.com",
    url="https://github.com/Orhideous/flask-nidhogg",
    packages=find_packages("nidhogg"),
    package_dir={"": "nidhogg"},
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
    keywords=[
        "Minecraft", "Yggdrasil", "Authentication",
    ],
    install_requires=requirements,
    test_suite='tests',
)