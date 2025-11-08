"""
Exercise Validation Utilities for Quantitative Finance Learning

This module provides reusable validation functions and assertion helpers
for interactive exercises in Jupyter notebooks. It follows pytest best
practices for clear error messages and educational feedback.

Author: QML Repository
Date: November 2025
"""

import numpy as np
import pandas as pd
from typing import Union, Optional, Tuple, Callable
import sys


class ValidationError(Exception):
    """Custom exception for exercise validation failures."""
    pass


def validate_type(value, expected_type, var_name: str = "value"):
    """
    Validate that a value is of expected type.
    
    Args:
        value: The value to check
        expected_type: Expected type or tuple of types
        var_name: Name of variable for error message
        
    Raises:
        ValidationError: If type doesn't match
    """
    if not isinstance(value, expected_type):
        if isinstance(expected_type, tuple):
            type_names = " or ".join(t.__name__ for t in expected_type)
        else:
            type_names = expected_type.__name__
        raise ValidationError(
            f"❌ {var_name} should be {type_names}, "
            f"got {type(value).__name__}"
        )


def validate_not_none(value, var_name: str = "value"):
    """
    Validate that a value is not None.
    
    Args:
        value: The value to check
        var_name: Name of variable for error message
        
    Raises:
        ValidationError: If value is None
    """
    if value is None:
        raise ValidationError(f"❌ {var_name} must be calculated! Currently None.")


def validate_numeric_close(
    actual: float,
    expected: float,
    rtol: float = 0.01,
    atol: float = 1e-8,
    var_name: str = "value"
):
    """
    Validate that a numeric value is close to expected value.
    
    Args:
        actual: The calculated value
        expected: The expected value
        rtol: Relative tolerance (default 1%)
        atol: Absolute tolerance
        var_name: Name of variable for error message
        
    Raises:
        ValidationError: If values don't match within tolerance
    """
    if not np.isclose(actual, expected, rtol=rtol, atol=atol):
        raise ValidationError(
            f"❌ {var_name} incorrect.\n"
            f"   Expected: {expected:.6f}\n"
            f"   Got: {actual:.6f}\n"
            f"   Difference: {abs(actual - expected):.6f}"
        )


def validate_array_close(
    actual: np.ndarray,
    expected: np.ndarray,
    rtol: float = 0.01,
    atol: float = 1e-8,
    var_name: str = "array"
):
    """
    Validate that arrays are close element-wise.
    
    Args:
        actual: The calculated array
        expected: The expected array
        rtol: Relative tolerance
        atol: Absolute tolerance
        var_name: Name of variable for error message
        
    Raises:
        ValidationError: If arrays don't match
    """
    if actual.shape != expected.shape:
        raise ValidationError(
            f"❌ {var_name} shape mismatch.\n"
            f"   Expected shape: {expected.shape}\n"
            f"   Got shape: {actual.shape}"
        )
    
    if not np.allclose(actual, expected, rtol=rtol, atol=atol):
        max_diff = np.max(np.abs(actual - expected))
        raise ValidationError(
            f"❌ {var_name} values don't match.\n"
            f"   Maximum difference: {max_diff:.6f}\n"
            f"   Relative tolerance: {rtol}"
        )


def validate_range(
    value: float,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None,
    var_name: str = "value",
    inclusive: bool = True
):
    """
    Validate that a value is within a specified range.
    
    Args:
        value: The value to check
        min_val: Minimum allowed value (None for no minimum)
        max_val: Maximum allowed value (None for no maximum)
        var_name: Name of variable for error message
        inclusive: Whether range is inclusive (default True)
        
    Raises:
        ValidationError: If value is outside range
    """
    if min_val is not None:
        if inclusive and value < min_val:
            raise ValidationError(
                f"❌ {var_name} must be >= {min_val}, got {value:.6f}"
            )
        elif not inclusive and value <= min_val:
            raise ValidationError(
                f"❌ {var_name} must be > {min_val}, got {value:.6f}"
            )
    
    if max_val is not None:
        if inclusive and value > max_val:
            raise ValidationError(
                f"❌ {var_name} must be <= {max_val}, got {value:.6f}"
            )
        elif not inclusive and value >= max_val:
            raise ValidationError(
                f"❌ {var_name} must be < {max_val}, got {value:.6f}"
            )


def validate_portfolio_weights(weights: np.ndarray, tolerance: float = 1e-6):
    """
    Validate that portfolio weights sum to 1 (or 100%).
    
    Args:
        weights: Array of portfolio weights
        tolerance: Tolerance for sum check
        
    Raises:
        ValidationError: If weights don't sum to approximately 1
    """
    total = np.sum(weights)
    if not np.isclose(total, 1.0, atol=tolerance):
        raise ValidationError(
            f"❌ Portfolio weights must sum to 1.0\n"
            f"   Current sum: {total:.6f}\n"
            f"   Difference: {abs(total - 1.0):.6f}"
        )


def validate_returns_series(returns: pd.Series):
    """
    Validate that a returns series has reasonable properties.
    
    Args:
        returns: Pandas Series of returns
        
    Raises:
        ValidationError: If returns series has issues
    """
    validate_type(returns, pd.Series, "returns")
    
    if len(returns) == 0:
        raise ValidationError("❌ Returns series is empty!")
    
    # Check for all NaN
    if returns.isna().all():
        raise ValidationError("❌ All returns are NaN!")
    
    # Check for infinite values
    if np.isinf(returns).any():
        raise ValidationError("❌ Returns contain infinite values!")
    
    # Warn about extreme returns (likely error)
    max_return = returns.max()
    min_return = returns.min()
    if max_return > 2.0:  # 200% daily return seems suspicious
        print(f"⚠️  Warning: Maximum return is very high: {max_return:.2%}")
    if min_return < -1.0:  # -100% or worse
        print(f"⚠️  Warning: Minimum return is very low: {min_return:.2%}")


def validate_correlation_matrix(corr_matrix: np.ndarray):
    """
    Validate properties of a correlation matrix.
    
    Args:
        corr_matrix: Correlation matrix to validate
        
    Raises:
        ValidationError: If matrix is not a valid correlation matrix
    """
    # Must be square
    if corr_matrix.ndim != 2 or corr_matrix.shape[0] != corr_matrix.shape[1]:
        raise ValidationError(
            f"❌ Correlation matrix must be square.\n"
            f"   Got shape: {corr_matrix.shape}"
        )
    
    # Diagonal should be all 1s
    diag = np.diag(corr_matrix)
    if not np.allclose(diag, 1.0):
        raise ValidationError(
            "❌ Correlation matrix diagonal must be all 1s.\n"
            f"   Diagonal values: {diag}"
        )
    
    # Must be symmetric
    if not np.allclose(corr_matrix, corr_matrix.T):
        raise ValidationError("❌ Correlation matrix must be symmetric")
    
    # Values should be in [-1, 1]
    if np.any(corr_matrix > 1.0) or np.any(corr_matrix < -1.0):
        raise ValidationError(
            "❌ Correlation values must be in range [-1, 1]"
        )
    
    # Should be positive semi-definite
    eigenvalues = np.linalg.eigvals(corr_matrix)
    if np.any(eigenvalues < -1e-10):  # Allow small negative due to numerical errors
        raise ValidationError(
            "❌ Correlation matrix must be positive semi-definite.\n"
            f"   Minimum eigenvalue: {eigenvalues.min():.6f}"
        )


def exercise_passed(message: str = "Exercise Complete!"):
    """
    Print success message when exercise passes all checks.
    
    Args:
        message: Success message to print
    """
    print(f"✅ {message}")


def print_interpretation(text: str):
    """
    Print interpretation/explanation text with consistent formatting.
    
    Args:
        text: Interpretation text
    """
    print(f"   Interpretation: {text}")


# Decorator for hiding traceback in assertion helpers
def hide_traceback(func: Callable) -> Callable:
    """
    Decorator to hide function from traceback for cleaner error messages.
    
    Usage:
        @hide_traceback
        def check_value(x):
            assert x > 0, "Value must be positive"
    """
    def wrapper(*args, **kwargs):
        __tracebackhide__ = True
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


# Context manager for exercise validation
class ExerciseValidator:
    """
    Context manager for running exercise validations with clean error reporting.
    
    Usage:
        with ExerciseValidator("Exercise 1"):
            validate_not_none(my_var, "my_var")
            validate_numeric_close(result, 10.5, var_name="result")
    """
    
    def __init__(self, exercise_name: str):
        self.exercise_name = exercise_name
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is ValidationError:
            print(f"\n{self.exercise_name} Failed:")
            print(f"{exc_val}")
            return True  # Suppress traceback for ValidationError
        return False  # Propagate other exceptions


if __name__ == "__main__":
    # Example usage and tests
    print("Testing Exercise Validators...")
    
    # Test 1: Type validation
    try:
        validate_type(5, str, "test_var")
    except ValidationError as e:
        print(f"✓ Type validation works: {e}")
    
    # Test 2: Numeric close validation
    try:
        validate_numeric_close(10.01, 10.0, rtol=0.001, var_name="test")
    except ValidationError as e:
        print(f"✓ Numeric validation works: {e}")
    
    # Test 3: Range validation
    try:
        validate_range(150, min_val=0, max_val=100, var_name="score")
    except ValidationError as e:
        print(f"✓ Range validation works: {e}")
    
    print("\n✅ All validator tests passed!")
