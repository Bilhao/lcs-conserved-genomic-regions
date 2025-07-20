"""
Setup script for LCS Conserved Genomic Regions package.
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open(os.path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="lcs-conserved-genomic-regions",
    version="1.0.0",
    author="Bilhao",
    author_email="",
    description="A Python tool for identifying conserved genomic regions using Needleman-Wunsch alignment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bilhao/lcs-conserved-genomic-regions",
    py_modules=[
        "main",
        "sequence", 
        "lcs_finder",
        "lcs_finder_n_sequences",
        "sequence_alignment",
        "sequence_database",
        "visualize"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "lcs-genomic=main:main",
        ],
    },
    keywords="bioinformatics genomics sequence-alignment needleman-wunsch dna",
    project_urls={
        "Bug Reports": "https://github.com/Bilhao/lcs-conserved-genomic-regions/issues",
        "Source": "https://github.com/Bilhao/lcs-conserved-genomic-regions",
    },
)