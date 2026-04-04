from setuptools import setup
from setuptools import find_packages

version = "1.0.1"

install_requires = [
    "requests",
]

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

setup(
    name="guntamatic",
    version=version,
    description="module to get data from a Guntamatic heater e.g. BMK 20",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitea.caret.be/jens/guntamatic",
    author="Jens Timmerman",
    author_email="guntamatic@caret.be",
    license="Apache License 2.0",
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "guntamatic = guntamatic.heater:main"
        ]
    },
)
