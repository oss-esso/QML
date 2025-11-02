"""Test configuration and fixtures."""

import pytest
import numpy as np
import pandas as pd


@pytest.fixture
def sample_returns():
    """Generate sample return series for testing."""
    np.random.seed(42)
    dates = pd.date_range("2020-01-01", periods=252, freq="D")
    returns = pd.Series(np.random.normal(0.001, 0.02, 252), index=dates)
    return returns


@pytest.fixture
def sample_prices():
    """Generate sample price series for testing."""
    np.random.seed(42)
    dates = pd.date_range("2020-01-01", periods=252, freq="D")
    price = 100
    prices = [price]
    
    for _ in range(251):
        price *= 1 + np.random.normal(0.001, 0.02)
        prices.append(price)
    
    return pd.Series(prices, index=dates)
