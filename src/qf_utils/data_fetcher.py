"""Data fetching utilities for financial data."""

import logging
from datetime import datetime, timedelta
from typing import List, Optional, Union

import pandas as pd
import yfinance as yf

logger = logging.getLogger(__name__)


class DataFetcher:
    """Fetch financial market data from various sources."""

    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize DataFetcher.

        Parameters
        ----------
        cache_dir : str, optional
            Directory to cache downloaded data
        """
        self.cache_dir = cache_dir
        logger.info("DataFetcher initialized")

    def fetch_stock_data(
        self,
        tickers: Union[str, List[str]],
        start_date: Optional[Union[str, datetime]] = None,
        end_date: Optional[Union[str, datetime]] = None,
        period: str = "1y",
    ) -> pd.DataFrame:
        """
        Fetch stock price data from Yahoo Finance.

        Parameters
        ----------
        tickers : str or list of str
            Stock ticker symbol(s)
        start_date : str or datetime, optional
            Start date for historical data
        end_date : str or datetime, optional
            End date for historical data
        period : str, default='1y'
            Period to download (e.g., '1d', '5d', '1mo', '1y', 'max')

        Returns
        -------
        pd.DataFrame
            DataFrame with OHLCV data

        Examples
        --------
        >>> fetcher = DataFetcher()
        >>> data = fetcher.fetch_stock_data('AAPL', period='1mo')
        >>> data.head()
        """
        try:
            if isinstance(tickers, str):
                tickers = [tickers]

            logger.info(f"Fetching data for {tickers}")

            if start_date and end_date:
                data = yf.download(
                    tickers,
                    start=start_date,
                    end=end_date,
                    auto_adjust=True,
                    progress=False,
                )
            else:
                data = yf.download(
                    tickers, period=period, auto_adjust=True, progress=False
                )

            logger.info(f"Successfully fetched {len(data)} rows")
            return data

        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            raise

    def calculate_returns(
        self, prices: pd.Series, method: str = "simple"
    ) -> pd.Series:
        """
        Calculate returns from price series.

        Parameters
        ----------
        prices : pd.Series
            Price series
        method : str, default='simple'
            'simple' or 'log' returns

        Returns
        -------
        pd.Series
            Returns series

        Examples
        --------
        >>> fetcher = DataFetcher()
        >>> returns = fetcher.calculate_returns(price_series)
        """
        if not isinstance(prices, pd.Series):
            raise TypeError("prices must be a pandas Series")

        if len(prices) < 2:
            raise ValueError("Need at least 2 price points")

        if (prices <= 0).any():
            raise ValueError("Prices must be positive")

        if method == "simple":
            returns = prices.pct_change()
        elif method == "log":
            returns = np.log(prices / prices.shift(1))
        else:
            raise ValueError("method must be 'simple' or 'log'")

        return returns.dropna()

    def get_multiple_assets(
        self, tickers: List[str], start_date: str, end_date: str
    ) -> pd.DataFrame:
        """
        Fetch multiple assets and return close prices.

        Parameters
        ----------
        tickers : list of str
            List of ticker symbols
        start_date : str
            Start date
        end_date : str
            End date

        Returns
        -------
        pd.DataFrame
            DataFrame with close prices for each ticker
        """
        data = self.fetch_stock_data(tickers, start_date, end_date)

        if len(tickers) == 1:
            return data[["Close"]].rename(columns={"Close": tickers[0]})
        else:
            return data["Close"]


def main():
    """Command-line interface for data fetching."""
    import argparse

    parser = argparse.ArgumentParser(description="Fetch financial data")
    parser.add_argument("ticker", help="Ticker symbol")
    parser.add_argument("--period", default="1y", help="Period to fetch")
    parser.add_argument("--output", help="Output CSV file")

    args = parser.parse_args()

    fetcher = DataFetcher()
    data = fetcher.fetch_stock_data(args.ticker, period=args.period)

    if args.output:
        data.to_csv(args.output)
        print(f"Data saved to {args.output}")
    else:
        print(data.head())
        print(f"\nFetched {len(data)} rows")


if __name__ == "__main__":
    main()
