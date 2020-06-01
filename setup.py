#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from setuptools import find_packages, setup

import tcgplayer_api


with open('tcgplayer_api/VERSION') as version_file:
    version = version_file.read().strip()

with open("README.md") as readme_file:
    readme = readme_file.read()

# Requirements placed here for convenient viewing
install_requires = ["requests"]
tests_requires = ["pytest", "pytest-cov"]
docs_requires = [
    "m2r",
    "setuptools>=30.4",
    "Sphinx~=2.0",  # Use of v3.x.x requires m2r upgrade: https://github.com/miyakogi/m2r/pull/55
    "sphinxcontrib-apidoc~=0.3.0",
    "sphinx_rtd_theme"
]
dev_requires = tests_requires + docs_requires + ["pre-commit", "tox"]

# Avoid setuptools as an entrypoint unless it's the only way to do it.
# In other words, only use setuptools to build dists and wheels.
# E.g.: Run tests with pytest or tox; build sphinx directly; etc.
setup(
    name=tcgplayer_api.__name__,
    version=version,
    description='A Python client library for the TCGPlayer API.',
    long_description=readme,
    long_description_content_type='text/markdown',
    url="https://github.com/zaxr/tcgplayer-api-client-python",
    author=tcgplayer_api.__author__,
    author_email=tcgplayer_api.__email__,
    classifiers=["Development Status :: 2 - Pre-Alpha",
                 "Intended Audience :: Developers",
                 # "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                 "Natural Language :: English",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.6",
                 "Programming Language :: Python :: 3.7",
                 "Programming Language :: Python :: 3.8"],
    keywords='mtg magic the gathering tcg player api client',
    packages=find_packages(exclude=["docs", "tests"]),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=install_requires,
    extras_require={'docs': docs_requires,
                    'test': tests_requires,
                    'dev': dev_requires}
)
