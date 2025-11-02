"""Performance analysis utilities."""

import logging
from typing import Dict, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from .risk_metrics import RiskMetrics

logger = logging.getLogger(__name__)


class PerformanceAnalyzer:
    """Analyze and visualize trading strategy performance."""

    def __init__(self, returns: pd.Series, benchmark_returns: Optional[pd.Series] = None):
        """
        Initialize PerformanceAnalyzer.

        Parameters
        ----------
        returns : pd.Series
            Strategy returns
        benchmark_returns : pd.Series, optional
            Benchmark returns for comparison
        """
        self.returns = returns
        self.benchmark_returns = benchmark_returns
        self.risk_metrics = RiskMetrics()

    def generate_report(self) -> Dict[str, float]:
        """
        Generate comprehensive performance report.

        Returns
        -------
        dict
            Dictionary of performance metrics
        """
        report = {
            "Total Return": (1 + self.returns).prod() - 1,
            "Annualized Return": self.returns.mean() * 252,
            "Volatility": self.risk_metrics.volatility(self.returns),
            "Sharpe Ratio": self.risk_metrics.sharpe_ratio(self.returns),
            "Sortino Ratio": self.risk_metrics.sortino_ratio(self.returns),
            "Max Drawdown": self.risk_metrics.max_drawdown(self.returns),
            "Calmar Ratio": self.risk_metrics.calmar_ratio(self.returns),
            "VaR (95%)": self.risk_metrics.value_at_risk(self.returns, 0.95),
            "CVaR (95%)": self.risk_metrics.conditional_value_at_risk(self.returns, 0.95),
            "Win Rate": (self.returns > 0).mean(),
        }

        if self.benchmark_returns is not None:
            report["Beta"] = self.risk_metrics.beta(self.returns, self.benchmark_returns)
            excess_returns = self.returns - self.benchmark_returns
            report["Alpha"] = excess_returns.mean() * 252

        return report

    def plot_cumulative_returns(self, figsize=(12, 6)):
        """Plot cumulative returns."""
        plt.figure(figsize=figsize)
        cumulative = (1 + self.returns).cumprod()
        plt.plot(cumulative.index, cumulative.values, label="Strategy")

        if self.benchmark_returns is not None:
            benchmark_cumulative = (1 + self.benchmark_returns).cumprod()
            plt.plot(
                benchmark_cumulative.index,
                benchmark_cumulative.values,
                label="Benchmark",
                alpha=0.7,
            )

        plt.title("Cumulative Returns")
        plt.xlabel("Date")
        plt.ylabel("Cumulative Return")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        return plt.gcf()

    def plot_drawdown(self, figsize=(12, 6)):
        """Plot drawdown over time."""
        plt.figure(figsize=figsize)
        cumulative = (1 + self.returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max

        plt.fill_between(drawdown.index, drawdown.values, 0, alpha=0.3, color="red")
        plt.plot(drawdown.index, drawdown.values, color="red", linewidth=1)
        plt.title("Drawdown Over Time")
        plt.xlabel("Date")
        plt.ylabel("Drawdown")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        return plt.gcf()

    def plot_monthly_returns(self, figsize=(14, 6)):
        """Plot monthly returns heatmap."""
        monthly_returns = self.returns.resample("M").apply(lambda x: (1 + x).prod() - 1)
        monthly_returns.index = monthly_returns.index.to_period("M")

        # Create pivot table
        pivot = monthly_returns.groupby([monthly_returns.index.year, monthly_returns.index.month]).first().unstack()

        plt.figure(figsize=figsize)
        sns.heatmap(pivot, annot=True, fmt=".2%", cmap="RdYlGn", center=0, cbar_kws={"label": "Return"})
        plt.title("Monthly Returns Heatmap")
        plt.xlabel("Month")
        plt.ylabel("Year")
        plt.tight_layout()
        return plt.gcf()

    def print_report(self):
        """Print formatted performance report."""
        report = self.generate_report()

        print("\n" + "=" * 60)
        print("PERFORMANCE REPORT")
        print("=" * 60)

        for metric, value in report.items():
            if "Return" in metric or "Ratio" in metric or "Drawdown" in metric or "VaR" in metric or "CVaR" in metric or "Volatility" in metric:
                print(f"{metric:.<40} {value:>15.4f}")
            elif "Rate" in metric:
                print(f"{metric:.<40} {value:>14.2%}")
            else:
                print(f"{metric:.<40} {value:>15.4f}")

        print("=" * 60 + "\n")
