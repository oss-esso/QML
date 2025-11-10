# Comprehensive Quantitative Finance Technical Report

This directory contains a complete LaTeX technical report covering advanced probability theory, stochastic processes, stochastic calculus, machine learning, and portfolio optimization with applications to quantitative finance.

## Files Structure

```
technical_report.tex              # Main file with preamble and Chapter 1
chapter2_stochastic_processes.tex # Chapter 2: Stochastic Processes
chapter3_stochastic_calculus.tex  # Chapter 3: Stochastic Calculus & Options
chapter4_machine_learning.tex     # Chapter 4: Machine Learning & GARCH
chapter5_portfolio.tex            # Chapter 5: Portfolio Optimization (includes conclusion)
```

## Compilation Instructions

### Method 1: Combine All Files

Create a single complete document by combining all chapter files:

```bash
# On macOS/Linux
cat technical_report.tex > complete_report.tex
echo "\n% Chapter 2" >> complete_report.tex
sed '1d' chapter2_stochastic_processes.tex >> complete_report.tex
echo "\n% Chapter 3" >> complete_report.tex  
sed '1d' chapter3_stochastic_calculus.tex >> complete_report.tex
echo "\n% Chapter 4" >> complete_report.tex
sed '1d' chapter4_machine_learning.tex >> complete_report.tex
echo "\n% Chapter 5" >> complete_report.tex
sed '1d' chapter5_portfolio.tex >> complete_report.tex
```

Then compile:
```bash
pdflatex complete_report.tex
pdflatex complete_report.tex  # Run twice for references
```

### Method 2: Manual Assembly

1. Open `technical_report.tex`
2. Before `\end{document}`, add:
   ```latex
   \input{chapter2_stochastic_processes}
   \input{chapter3_stochastic_calculus}
   \input{chapter4_machine_learning}
   \input{chapter5_portfolio}
   ```
3. Remove the `\end{document}` from chapter files 2-5
4. Compile with `pdflatex technical_report.tex`

### Method 3: Use Provided Script

```bash
chmod +x compile_report.sh
./compile_report.sh
```

## Content Overview

### Chapter 1: Advanced Probability Theory and Financial Risk Metrics (60+ pages)
- Probability spaces and axioms
- Random variables and distributions
- Moments, skewness, kurtosis
- Characteristic functions
- Law of Large Numbers and Central Limit Theorem
- Conditional expectation and martingales
- Value-at-Risk (VaR) calculation methods
- Conditional VaR (Expected Shortfall)
- Risk-adjusted performance metrics (Sharpe, Sortino)
- Maximum drawdown

### Chapter 2: Stochastic Processes and Mean Reversion (50+ pages)
- Markov chains and random walks
- Brownian motion properties
- Geometric Brownian Motion (GBM)
- Ornstein-Uhlenbeck (OU) process
- Mean reversion theory and half-life
- Parameter estimation for OU processes
- Cointegration testing
- Pairs trading strategies
- Process simulation methods

### Chapter 3: Stochastic Calculus and Option Pricing (60+ pages)
- Itô integral construction and properties
- Itô's lemma (1D and multidimensional)
- Stochastic differential equations (SDEs)
- Black-Scholes-Merton framework
- Derivation of Black-Scholes PDE
- Black-Scholes formula
- Put-call parity
- Option Greeks (Delta, Gamma, Vega, Theta, Rho)
- Implied volatility calculation
- Volatility smile and skew
- Path-dependent options
- Jump-diffusion models

### Chapter 4: Machine Learning for Financial Time Series (55+ pages)
- AR, MA, ARMA, ARIMA models
- Model selection with AIC/BIC
- ARCH and GARCH models
- GARCH(1,1) properties and estimation
- GJR-GARCH for asymmetric effects
- Volatility forecasting
- Neural networks and feedforward architectures
- Recurrent Neural Networks (RNN)
- Long Short-Term Memory (LSTM) networks
- LSTM architecture and training
- Financial time series considerations
- Hybrid GARCH-LSTM models
- Overfitting and regularization
- Performance evaluation

### Chapter 5: Portfolio Optimization and Risk Management (60+ pages)
- Modern Portfolio Theory (Markowitz)
- Mean-variance optimization
- Analytical solutions
- Efficient frontier
- Two-fund separation theorem
- Tangency portfolio and Capital Market Line
- Short-selling constraints
- Transaction costs
- Risk parity approach
- Estimation error and shrinkage methods
- Black-Litterman model
- Factor models (CAPM, Fama-French)
- Performance attribution
- Robust optimization
- Dynamic portfolio optimization
- Backtesting procedures

## Key Features

1. **Rigorous Mathematical Treatment**: All results proven or carefully derived
2. **Practical Implementation**: Python code examples throughout
3. **Real-World Applications**: Financial data and realistic examples
4. **Comprehensive Coverage**: 300+ pages of technical content
5. **Industry-Standard Methods**: GARCH, Black-Scholes, LSTM, Markowitz
6. **Modern Extensions**: Deep learning, robust optimization, factor models

## Prerequisites

- Calculus (single and multivariable)
- Linear algebra
- Probability and statistics
- Basic programming (Python)
- Familiarity with financial markets (helpful but not required)

## Target Audience

- Quantitative finance professionals
- Master's/PhD students in financial engineering
- Data scientists transitioning to finance
- Risk managers and portfolio managers
- Researchers in computational finance

## Required LaTeX Packages

All required packages are included in the preamble:
- amsmath, amssymb, amsthm (mathematics)
- graphicx (figures)
- hyperref (links and references)
- listings (code formatting)
- algorithm, algpseudocode (algorithms)
- booktabs (professional tables)
- tcolorbox (colored boxes)

## Compilation Requirements

- LaTeX distribution (TeX Live, MiKTeX, MacTeX)
- pdflatex compiler
- Standard LaTeX packages (usually included in distributions)

## Estimated Document Length

- Total pages: ~300-350 (with figures and spacing)
- Main content: ~280 pages
- Appendices: ~20 pages
- Bibliography: ~2 pages
- Table of contents, lists: ~5 pages

## Citations and References

The document includes 15 key references covering:
- Seminal papers (Markowitz, Black-Scholes, Merton)
- Econometric methods (Engle, Bollerslev)
- Modern textbooks (Hull, Shreve, Tsay)
- Machine learning (Goodfellow, López de Prado)

## License

This technical report is part of the QML (Quantitative Machine Learning) project.
See LICENSE file for details.

## Author

Edoardo Spigarolo
Transitioning from Quantum Physics to Quantitative Finance

## Acknowledgments

This report synthesizes theoretical foundations from classical texts with practical
implementations using modern Python libraries including NumPy, pandas, scipy,
statsmodels, yfinance, ARCH, and TensorFlow.

## Contact

For questions or corrections, please open an issue in the GitHub repository.

---

**Last Updated**: November 10, 2025
