"""Risk metrics calculations for portfolios and strategies."""

import logging
from typing import Optional

import numpy as np
import pandas as pd
from scipy import stats

logger = logging.getLogger(__name__)


class RiskMetrics:
    """Calculate various risk metrics for financial returns."""

    @staticmethod
    def sharpe_ratio(
        returns: pd.Series,
        risk_free_rate: float = 0.0,
        periods_per_year: int = 252,
    ) -> float:
        """
        Calculate annualized Sharpe ratio.

        Parameters
        ----------
        returns : pd.Series
            Returns series
        risk_free_rate : float, default=0.0
            Annual risk-free rate
        periods_per_year : int, default=252
            Trading periods per year

        Returns
        -------
        float
            Sharpe ratio

        Examples
        --------
        >>> returns = pd.Series([0.01, 0.02, -0.01, 0.03, -0.02])
        >>> RiskMetrics.sharpe_ratio(returns, risk_free_rate=0.02)
        """
        excess_returns = returns - risk_free_rate / periods_per_year
        if excess_returns.std() == 0:
            return 0.0
        return np.sqrt(periods_per_year) * excess_returns.mean() / excess_returns.std()

    @staticmethod
    def sortino_ratio(
        returns: pd.Series,
        risk_free_rate: float = 0.0,
        periods_per_year: int = 252,
    ) -> float:
        """
        Calculate annualized Sortino ratio (downside risk-adjusted).

        Parameters
        ----------
        returns : pd.Series
            Returns series
        risk_free_rate : float, default=0.0
            Annual risk-free rate
        periods_per_year : int, default=252
            Trading periods per year

        Returns
        -------
        float
            Sortino ratio
        """
        excess_returns = returns - risk_free_rate / periods_per_year
        downside_returns = excess_returns[excess_returns < 0]
        
        if len(downside_returns) == 0 or downside_returns.std() == 0:
            return 0.0
        
        downside_std = np.sqrt(np.mean(downside_returns**2))
        return np.sqrt(periods_per_year) * excess_returns.mean() / downside_std

    @staticmethod
    def max_drawdown(returns: pd.Series) -> float:
        """
        Calculate maximum drawdown.

        Parameters
        ----------
        returns : pd.Series
            Returns series

        Returns
        -------
        float
            Maximum drawdown (positive value)

        Examples
        --------
        >>> returns = pd.Series([0.01, 0.02, -0.05, 0.03, -0.02])
        >>> RiskMetrics.max_drawdown(returns)
        """
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        return abs(drawdown.min())

    @staticmethod
    def calmar_ratio(
        returns: pd.Series,
        periods_per_year: int = 252,
    ) -> float:
        """
        Calculate Calmar ratio (return / max drawdown).

        Parameters
        ----------
        returns : pd.Series
            Returns series
        periods_per_year : int, default=252
            Trading periods per year

        Returns
        -------
        float
            Calmar ratio
        """
        annual_return = returns.mean() * periods_per_year
        mdd = RiskMetrics.max_drawdown(returns)
        
        if mdd == 0:
            return 0.0
        
        return annual_return / mdd

    @staticmethod
    def value_at_risk(
        returns: pd.Series,
        confidence_level: float = 0.95,
        method: str = "historical",
    ) -> float:
        """
        Calculate Value at Risk (VaR).

        Parameters
        ----------
        returns : pd.Series
            Returns series
        confidence_level : float, default=0.95
            Confidence level (e.g., 0.95 for 95% VaR)
        method : str, default='historical'
            Method: 'historical', 'parametric', or 'cornish-fisher'

        Returns
        -------
        float
            VaR (positive value represents potential loss)

        Examples
        --------
        >>> returns = pd.Series(np.random.normal(0, 0.02, 1000))
        >>> var_95 = RiskMetrics.value_at_risk(returns, 0.95)
        """
        if method == "historical":
            return -np.percentile(returns, (1 - confidence_level) * 100)
        
        elif method == "parametric":
            mu = returns.mean()
            sigma = returns.std()
            z_score = stats.norm.ppf(1 - confidence_level)
            return -(mu + sigma * z_score)
        
        elif method == "cornish-fisher":
            mu = returns.mean()
            sigma = returns.std()
            skew = returns.skew()
            kurt = returns.kurtosis()
            
            z = stats.norm.ppf(1 - confidence_level)
            z_cf = (z +
                    (z**2 - 1) * skew / 6 +
                    (z**3 - 3*z) * kurt / 24 -
                    (2*z**3 - 5*z) * skew**2 / 36)
            
            return -(mu + sigma * z_cf)
        
        else:
            raise ValueError("method must be 'historical', 'parametric', or 'cornish-fisher'")

    @staticmethod
    def conditional_value_at_risk(
        returns: pd.Series,
        confidence_level: float = 0.95,
    ) -> float:
        """
        Calculate Conditional Value at Risk (CVaR / Expected Shortfall).

        Parameters
        ----------
        returns : pd.Series
            Returns series
        confidence_level : float, default=0.95
            Confidence level

        Returns
        -------
        float
            CVaR (positive value represents expected loss in tail)

        Examples
        --------
        >>> returns = pd.Series(np.random.normal(0, 0.02, 1000))
        >>> cvar_95 = RiskMetrics.conditional_value_at_risk(returns, 0.95)
        """
        var = -np.percentile(returns, (1 - confidence_level) * 100)
        tail_losses = returns[returns <= -var]
        return -tail_losses.mean() if len(tail_losses) > 0 else 0.0

    @staticmethod
    def volatility(
        returns: pd.Series,
        periods_per_year: int = 252,
    ) -> float:
        """
        Calculate annualized volatility.

        Parameters
        ----------
        returns : pd.Series
            Returns series
        periods_per_year : int, default=252
            Trading periods per year

        Returns
        -------
        float
            Annualized volatility
        """
        return returns.std() * np.sqrt(periods_per_year)

    @staticmethod
    def beta(
        returns: pd.Series,
        market_returns: pd.Series,
    ) -> float:
        """
        Calculate beta relative to market.

        Parameters
        ----------
        returns : pd.Series
            Asset returns
        market_returns : pd.Series
            Market returns

        Returns
        -------
        float
            Beta coefficient
        """
        covariance = returns.cov(market_returns)
        market_variance = market_returns.var()
        
        if market_variance == 0:
            return 0.0
        
        return covariance / market_variance


def main():
    """Example usage of RiskMetrics."""
    # Generate sample returns
    np.random.seed(42)
    returns = pd.Series(np.random.normal(0.001, 0.02, 252))
    
    print("Risk Metrics Example")
    print("=" * 50)
    print(f"Sharpe Ratio: {RiskMetrics.sharpe_ratio(returns):.4f}")
    print(f"Sortino Ratio: {RiskMetrics.sortino_ratio(returns):.4f}")
    print(f"Max Drawdown: {RiskMetrics.max_drawdown(returns):.4%}")
    print(f"Calmar Ratio: {RiskMetrics.calmar_ratio(returns):.4f}")
    print(f"VaR (95%): {RiskMetrics.value_at_risk(returns, 0.95):.4%}")
    print(f"CVaR (95%): {RiskMetrics.conditional_value_at_risk(returns, 0.95):.4%}")
    print(f"Volatility: {RiskMetrics.volatility(returns):.4%}")


if __name__ == "__main__":
    main()
