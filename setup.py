#!/usr/bin/env python3
from os import name, path
from sys import version
import setuptools

req_pkgs = [
    'bs4'
]

exec(open("fetch/__version__.py").read())

with open("README.md","r") as f:
    long_description = f.read()

setuptools.setup(
    name = "yashsinghcodes",
    version = "1.0.0",
    author = "Yash Singh",
    author_email = "yash9vardhan@gmail.com",
    description = "Fetch is use to get information about anything on the shell using Wikipedia",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/yashsinghcodes/fetch",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.*',
    install_requires = req_pkgs,
    setup_requires = req_pkgs
)