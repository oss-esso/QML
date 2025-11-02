"""Setup script for Quantitative Finance Learning Repository."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="quant-finance-learning",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive quantitative finance learning repository for transitioning from physics to finance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/QML",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "scipy>=1.10.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "statsmodels>=0.14.0",
        "arch>=6.2.0",
        "yfinance>=0.2.28",
        "scikit-learn>=1.3.0",
        "cvxpy>=1.3.0",
        "PyPortfolioOpt>=1.5.5",
        "plotly>=5.14.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "mypy>=1.4.0",
            "sphinx>=7.0.0",
        ],
        "ml": [
            "xgboost>=1.7.6",
            "lightgbm>=4.0.0",
            "torch>=2.0.0",
            "tensorflow>=2.13.0",
        ],
        "bayesian": [
            "pymc>=5.6.0",
            "arviz>=0.15.0",
        ],
        "backtest": [
            "backtrader>=1.9.78",
            "vectorbt>=0.25.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "qf-fetch-data=qf_utils.data_fetcher:main",
            "qf-backtest=qf_utils.backtester:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/QML/issues",
        "Source": "https://github.com/yourusername/QML",
        "Documentation": "https://qml.readthedocs.io/",
    },
)
