"""Simple backtesting framework."""

import logging
from typing import Callable, Dict, Optional

import numpy as np
import pandas as pd

from .risk_metrics import RiskMetrics
from .performance import PerformanceAnalyzer

logger = logging.getLogger(__name__)


class Backtester:
    """Simple backtesting framework for trading strategies."""

    def __init__(
        self,
        data: pd.DataFrame,
        initial_capital: float = 100000.0,
        commission: float = 0.001,
    ):
        """
        Initialize Backtester.

        Parameters
        ----------
        data : pd.DataFrame
            Price data with columns: Open, High, Low, Close, Volume
        initial_capital : float, default=100000.0
            Starting capital
        commission : float, default=0.001
            Commission rate (0.001 = 0.1%)
        """
        self.data = data
        self.initial_capital = initial_capital
        self.commission = commission
        self.positions = pd.Series(index=data.index, dtype=float).fillna(0)
        self.cash = pd.Series(index=data.index, dtype=float).fillna(initial_capital)
        self.portfolio_value = pd.Series(index=data.index, dtype=float)

    def run(self, signal_func: Callable) -> Dict:
        """
        Run backtest with given signal function.

        Parameters
        ----------
        signal_func : callable
            Function that takes data and returns trading signals
            Signals: 1 (buy), 0 (hold), -1 (sell)

        Returns
        -------
        dict
            Backtest results including returns, metrics, and trades
        """
        logger.info("Starting backtest...")

        # Generate signals
        signals = signal_func(self.data)

        # Initialize
        position = 0
        cash = self.initial_capital
        trades = []

        for i, (date, signal) in enumerate(signals.items()):
            price = self.data.loc[date, "Close"]

            # Execute trades based on signal
            if signal == 1 and position == 0:  # Buy
                shares = int(cash / price * (1 - self.commission))
                cost = shares * price * (1 + self.commission)
                if cost <= cash:
                    cash -= cost
                    position = shares
                    trades.append({"date": date, "action": "BUY", "shares": shares, "price": price})
                    logger.debug(f"BUY {shares} @ {price:.2f}")

            elif signal == -1 and position > 0:  # Sell
                proceeds = position * price * (1 - self.commission)
                cash += proceeds
                trades.append({"date": date, "action": "SELL", "shares": position, "price": price})
                logger.debug(f"SELL {position} @ {price:.2f}")
                position = 0

            # Track portfolio value
            portfolio_value = cash + position * price
            self.positions.loc[date] = position
            self.cash.loc[date] = cash
            self.portfolio_value.loc[date] = portfolio_value

        logger.info(f"Backtest complete. Total trades: {len(trades)}")

        # Calculate returns
        returns = self.portfolio_value.pct_change().dropna()

        # Generate performance report
        analyzer = PerformanceAnalyzer(returns)
        metrics = analyzer.generate_report()

        return {
            "returns": returns,
            "portfolio_value": self.portfolio_value,
            "positions": self.positions,
            "cash": self.cash,
            "trades": pd.DataFrame(trades),
            "metrics": metrics,
            "analyzer": analyzer,
        }


def main():
    """Example backtest."""
    from .data_fetcher import DataFetcher

    # Fetch data
    fetcher = DataFetcher()
    data = fetcher.fetch_stock_data("AAPL", period="1y")

    # Simple moving average crossover strategy
    def sma_crossover_signal(data, short_window=20, long_window=50):
        """Simple moving average crossover strategy."""
        signals = pd.Series(index=data.index, dtype=int).fillna(0)
        
        short_ma = data["Close"].rolling(window=short_window).mean()
        long_ma = data["Close"].rolling(window=long_window).mean()

        # Buy when short MA crosses above long MA
        signals[short_ma > long_ma] = 1
        # Sell when short MA crosses below long MA
        signals[short_ma < long_ma] = -1

        return signals

    # Run backtest
    backtester = Backtester(data, initial_capital=100000, commission=0.001)
    results = backtester.run(sma_crossover_signal)

    # Print results
    print("\nBacktest Results:")
    results["analyzer"].print_report()
    print(f"\nTotal Trades: {len(results['trades'])}")
    print(f"Final Portfolio Value: ${results['portfolio_value'].iloc[-1]:,.2f}")


if __name__ == "__main__":
    main()
