"""
Quantitative Finance Utilities Package.

This package provides reusable utilities for quantitative finance applications.
"""

__version__ = "0.1.0"
__author__ = "QF Learning Team"

from .data_fetcher import DataFetcher
from .risk_metrics import RiskMetrics
from .performance import PerformanceAnalyzer
from .backtester import Backtester
from .exercise_validators import (
    ValidationError,
    validate_type,
    validate_not_none,
    validate_numeric_close,
    validate_array_close,
    validate_range,
    validate_portfolio_weights,
    validate_returns_series,
    validate_correlation_matrix,
    exercise_passed,
    print_interpretation,
    hide_traceback,
    ExerciseValidator,
)

__all__ = [
    "DataFetcher",
    "RiskMetrics",
    "PerformanceAnalyzer",
    "Backtester",
    # Exercise validation
    "ValidationError",
    "validate_type",
    "validate_not_none",
    "validate_numeric_close",
    "validate_array_close",
    "validate_range",
    "validate_portfolio_weights",
    "validate_returns_series",
    "validate_correlation_matrix",
    "exercise_passed",
    "print_interpretation",
    "hide_traceback",
    "ExerciseValidator",
]
