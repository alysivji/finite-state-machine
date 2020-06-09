import codecs
import os
import re
from setuptools import setup, find_packages


############
# Supporting
############
with open("README.md") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    dependencies = f.read().splitlines()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *parts), "r") as fp:
        return fp.read()


#######
# Build
#######
setup(
    name="finite-state-machine",
    version=find_version("finite_state_machine", "__version__.py"),
    author="Aly Sivji",
    author_email="alysivji@gmail.com",
    description="Lightweight, decorator-based implementation of a Finite State Machine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alysivji/finite-state-machine",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="finite-state-machine finite-automata state-machine",
    install_requires=dependencies,
    packages=find_packages(exclude=["tests"]),
    test_suite="tests",
    zip_safe=False,
)
