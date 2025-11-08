"""
Cython-optimized modules for high-performance financial calculations.

This package contains Cython implementations of computationally intensive
algorithms used in quantitative finance.
"""

__version__ = "0.1.0"

# Import compiled Cython modules (will be available after compilation)
try:
    from .monte_carlo_cy import monte_carlo_option_price
    from .portfolio_opt_cy import efficient_frontier_cython
    from .greeks_cy import calculate_greeks_fast
    __all__ = [
        "monte_carlo_option_price",
        "efficient_frontier_cython", 
        "calculate_greeks_fast",
    ]
except ImportError:
    # Cython modules not compiled yet
    __all__ = []
    import warnings
    warnings.warn(
        "Cython modules not compiled. Run 'python setup.py build_ext --inplace' "
        "to compile for better performance.",
        ImportWarning
    )
