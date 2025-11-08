"""
Setup script for compiling Cython modules.

Usage:
    python setup_cython.py build_ext --inplace

This will compile all .pyx files in src/cython_modules/ to optimized C extensions.
"""

from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

extensions = [
    Extension(
        "src.cython_modules.monte_carlo_cy",
        ["src/cython_modules/monte_carlo_cy.pyx"],
        include_dirs=[np.get_include()],
        extra_compile_args=['-O3', '-march=native'],  # Maximum optimization
        extra_link_args=['-O3'],
    ),
]

setup(
    name="qf_cython_modules",
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            'language_level': "3",
            'boundscheck': False,
            'wraparound': False,
            'cdivision': True,
            'initializedcheck': False,
        },
        annotate=True,  # Generate HTML annotation files
    ),
    include_dirs=[np.get_include()],
)
