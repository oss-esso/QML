"""Tests for risk metrics."""

import pytest
import numpy as np
import pandas as pd

from qf_utils.risk_metrics import RiskMetrics


def test_sharpe_ratio(sample_returns):
    """Test Sharpe ratio calculation."""
    sharpe = RiskMetrics.sharpe_ratio(sample_returns)
    assert isinstance(sharpe, float)
    assert -5 < sharpe < 5  # Reasonable range


def test_sortino_ratio(sample_returns):
    """Test Sortino ratio calculation."""
    sortino = RiskMetrics.sortino_ratio(sample_returns)
    assert isinstance(sortino, float)


def test_max_drawdown(sample_returns):
    """Test maximum drawdown calculation."""
    mdd = RiskMetrics.max_drawdown(sample_returns)
    assert isinstance(mdd, float)
    assert 0 <= mdd <= 1


def test_value_at_risk(sample_returns):
    """Test VaR calculation."""
    var_95 = RiskMetrics.value_at_risk(sample_returns, 0.95)
    assert isinstance(var_95, float)
    assert var_95 >= 0


def test_conditional_value_at_risk(sample_returns):
    """Test CVaR calculation."""
    cvar_95 = RiskMetrics.conditional_value_at_risk(sample_returns, 0.95)
    assert isinstance(cvar_95, float)
    assert cvar_95 >= 0


def test_volatility(sample_returns):
    """Test volatility calculation."""
    vol = RiskMetrics.volatility(sample_returns)
    assert isinstance(vol, float)
    assert vol > 0


def test_beta():
    """Test beta calculation."""
    np.random.seed(42)
    market_returns = pd.Series(np.random.normal(0.001, 0.02, 252))
    asset_returns = 0.8 * market_returns + pd.Series(np.random.normal(0, 0.01, 252))
    
    beta = RiskMetrics.beta(asset_returns, market_returns)
    assert isinstance(beta, float)
    assert 0.5 < beta < 1.5  # Should be close to 0.8
