#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="webapppython",
    version="0.1.0",
    description="Application Python pour afficher un site web dans une fenêtre minimaliste",
    author="cyberax64",
    author_email="cyberax64@github.com",
    packages=find_packages(),
    install_requires=[
        "PyQt5>=5.15.0",
        "PyQtWebEngine>=5.15.0",
    ],
    entry_points={
        "console_scripts": [
            "webapppython=app:main",
        ],
    },
    python_requires=">=3.6",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)