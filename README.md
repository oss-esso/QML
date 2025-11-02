# 📊 Quantitative Finance Learning Repository

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **A comprehensive, production-ready quantitative finance learning environment for transitioning from physics to finance.**

---

## 🎯 Project Overview

This repository provides a complete learning path from fundamental probability theory to advanced quantitative finance applications. Designed specifically for professionals with physics/STEM backgrounds looking to transition into quantitative finance roles.

### What Makes This Different?

✅ **Production-Ready Code**: Industry-standard code quality with type hints, error handling, and comprehensive testing  
✅ **Real Market Data**: Integration with yfinance and other financial data sources  
✅ **Context7-Informed**: Built using up-to-date best practices from Context7 documentation  
✅ **Practical Focus**: Every concept includes real-world financial applications  
✅ **Complete Pipeline**: From data fetching to backtesting to performance analysis  

---

## 📚 Learning Modules

### Module 1: Advanced Probability
- Probability fundamentals recap
- Distributions and moments
- Monte Carlo simulations
- **Financial Applications**:
  - Value-at-Risk (VaR) calculations
  - Risk metrics (Sharpe, Sortino ratios)
  - Portfolio risk analysis

### Module 2: Stochastic Processes
- Random walks and Brownian motion
- Geometric Brownian Motion (GBM)
- Martingales
- Ornstein-Uhlenbeck processes
- **Financial Applications**:
  - Stock price modeling
  - Mean reversion strategies
  - Parameter calibration from market data

### Module 3: Stochastic Calculus
- Itô calculus and Itô's lemma
- Stochastic differential equations
- Black-Scholes-Merton model
- **Financial Applications**:
  - Option pricing (European, American, Exotic)
  - Greeks calculation (Delta, Gamma, Vega, Theta, Rho)
  - Implied volatility surfaces
  - Numerical methods (Monte Carlo, Finite Difference)

### Module 4: Machine Learning for Finance
- Time series analysis (ARIMA, GARCH)
- Feature engineering for finance
- Deep learning (LSTM, GRU)
- **Financial Applications**:
  - Volatility forecasting
  - Price prediction
  - Backtesting frameworks
  - Walk-forward optimization

### Module 5: Portfolio Optimization & Risk Management
- Markowitz mean-variance optimization
- Capital Asset Pricing Model (CAPM)
- Factor models (Fama-French)
- Risk parity and Black-Litterman
- **Financial Applications**:
  - Efficient frontier construction
  - Portfolio rebalancing
  - Risk budgeting
  - Kelly Criterion

### Module 6: Derivatives Pricing & Fixed Income
- Interest rate models (Vasicek, CIR, Hull-White)
- Term structure modeling
- Credit risk models
- **Financial Applications**:
  - Bond pricing and duration
  - Yield curve construction
  - Credit default swaps
  - Exotic derivatives

---

## 🚀 Quick Start

### Installation

#### Option 1: Using Conda (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/QML.git
cd QML

# Create conda environment
conda env create -f environment.yml

# Activate environment
conda activate quant-finance

# Install the package
pip install -e .
```

#### Option 2: Using pip
```bash
# Clone the repository
git clone https://github.com/yourusername/QML.git
cd QML

# Create virtual environment
python -m venv venv

# Activate environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Running Your First Notebook

```bash
# Start Jupyter Lab
jupyter lab

# Navigate to Proba/Module1_Advanced_Probability/01_Probability_Recap.ipynb
```

---

## 📖 Learning Path

### Phase 1: Foundations (Weeks 1-4)
**Objective**: Master probability theory and stochastic processes

1. Complete Module 1: Advanced Probability
   - Work through all notebooks
   - Complete exercises
   - Implement VaR calculator project

2. Complete Module 2: Stochastic Processes
   - Understand Brownian motion
   - Implement GBM simulator
   - Calibrate models to real data

**Skills Gained**: Python scientific computing, probability theory, stochastic modeling

### Phase 2: Derivatives & Quantitative Methods (Weeks 5-8)
**Objective**: Master derivatives pricing and stochastic calculus

3. Complete Module 3: Stochastic Calculus
   - Understand Itô calculus
   - Implement Black-Scholes pricer
   - Build Greeks calculator
   - Create option pricing engine

**Skills Gained**: Derivatives pricing, risk management, numerical methods

### Phase 3: Machine Learning & Time Series (Weeks 9-12)
**Objective**: Apply ML techniques to financial data

4. Complete Module 4: Machine Learning
   - Implement GARCH models
   - Build LSTM price predictor
   - Create backtesting framework
   - Develop trading strategy

**Skills Gained**: Time series forecasting, ML for finance, strategy development

### Phase 4: Portfolio Management (Weeks 13-16)
**Objective**: Master portfolio theory and risk management

5. Complete Module 5: Portfolio Optimization
   - Implement Markowitz optimization
   - Build factor models
   - Create portfolio backtester
   - Develop rebalancing strategies

**Skills Gained**: Portfolio construction, risk management, performance attribution

### Phase 5: Advanced Topics (Weeks 17-20)
**Objective**: Specialized knowledge in derivatives and fixed income

6. Complete Module 6: Derivatives & Fixed Income
   - Implement interest rate models
   - Build yield curve
   - Price exotic options
   - Model credit risk

**Skills Gained**: Advanced derivatives, fixed income, credit risk

---

## 🛠️ Project Structure

```
QML/
├── Proba/                          # Main learning modules
│   ├── Module1_Advanced_Probability/
│   ├── Module2_Stochastic_Processes/
│   ├── Module3_Stochastic_Calculus/
│   ├── Module4_Machine_Learning/
│   ├── Module5_Portfolio_Optimization/
│   └── Module6_Derivatives_Pricing/
├── src/
│   └── qf_utils/                   # Reusable utility modules
│       ├── __init__.py
│       ├── data_fetcher.py         # Financial data retrieval
│       ├── risk_metrics.py         # Risk calculations
│       ├── performance.py          # Performance analysis
│       └── backtester.py           # Backtesting framework
├── tests/                          # Unit tests
│   ├── conftest.py
│   └── test_risk_metrics.py
├── data/                           # Data storage
│   ├── raw/                        # Raw downloaded data
│   └── processed/                  # Processed datasets
├── models/                         # Trained models
│   └── trained/
├── notebooks/                      # Additional notebooks
│   ├── examples/                   # Example implementations
│   └── exercises/                  # Practice exercises
├── docs/                           # Documentation
├── requirements.txt                # Python dependencies
├── environment.yml                 # Conda environment
├── setup.py                        # Package installation
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
├── AUDIT_REPORT.md                 # Repository audit
├── INDUSTRY_STANDARDS_RESEARCH.md  # Industry best practices
└── .github/
    └── instructions/
        └── memory.instructions.md  # AI assistant memory
```

---

## 💼 Career Transition Guide: Physics → Quant Finance

### Your Advantages

As a physicist, you already have:
- ✅ Strong mathematical foundation
- ✅ Programming experience (Python, numerical methods)
- ✅ Problem-solving skills
- ✅ Experience with complex modeling

### Skills to Develop

1. **Financial Domain Knowledge** (2-3 months)
   - Learn financial markets and instruments
   - Understand trading mechanisms
   - Study regulatory environment

2. **Financial Programming** (2-3 months)
   - Master pandas for financial data
   - Learn yfinance and data sources
   - Build backtesting frameworks

3. **Quantitative Methods** (3-4 months)
   - Apply stochastic calculus to finance
   - Implement derivatives pricing models
   - Study portfolio theory

4. **Machine Learning for Finance** (2-3 months)
   - Time series forecasting
   - Feature engineering
   - Model validation

### Timeline to Job-Ready

**6-12 months** of focused learning with this repository

### Portfolio Projects

Build these 5 projects to showcase your skills:

1. **Options Pricing Engine** - Demonstrates derivatives knowledge
2. **Volatility Forecasting Model** - Shows time series expertise
3. **Algorithmic Trading Strategy** - End-to-end implementation
4. **Portfolio Optimizer** - Portfolio theory application
5. **ML Price Predictor** - Modern ML techniques

### Target Roles

- Quantitative Researcher ($150K-$500K+)
- Quantitative Developer ($120K-$350K+)
- Risk Analyst/Quant ($100K-$250K+)
- Data Scientist (Finance) ($120K-$300K+)

---

## 📊 Example Usage

### Fetch Stock Data
```python
from qf_utils.data_fetcher import DataFetcher

fetcher = DataFetcher()
data = fetcher.fetch_stock_data('AAPL', period='1y')
returns = fetcher.calculate_returns(data['Close'])
```

### Calculate Risk Metrics
```python
from qf_utils.risk_metrics import RiskMetrics

sharpe = RiskMetrics.sharpe_ratio(returns)
max_dd = RiskMetrics.max_drawdown(returns)
var_95 = RiskMetrics.value_at_risk(returns, 0.95)
```

### Run Backtest
```python
from qf_utils.backtester import Backtester

def my_strategy(data):
    # Your trading logic here
    signals = ...
    return signals

backtester = Backtester(data, initial_capital=100000)
results = backtester.run(my_strategy)
results['analyzer'].print_report()
```

---

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=qf_utils --cov-report=html

# Run specific test file
pytest tests/test_risk_metrics.py
```

---

## 📚 Recommended Resources

### Books
- "Options, Futures, and Other Derivatives" - John Hull
- "Stochastic Calculus for Finance II" - Steven Shreve
- "Advances in Financial Machine Learning" - Marcos López de Prado
- "Asset Pricing" - John Cochrane

### Online Courses
- Coursera: Machine Learning for Trading (Georgia Tech)
- edX: Computational Investing (MIT)

### Websites
- QuantStart
- QuantLib documentation
- Towards Data Science (Finance section)
- SSRN (q-fin papers)

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built using best practices from Context7 documentation
- Inspired by industry-standard quantitative finance curricula
- Thanks to the open-source financial Python community

---

## 📧 Contact

- **Author**: Your Name
- **Email**: your.email@example.com
- **LinkedIn**: [Your Profile](https://linkedin.com/in/yourprofile)
- **GitHub**: [@yourusername](https://github.com/yourusername)

---

## 🗺️ Roadmap

- [ ] Add more example notebooks
- [ ] Implement QuantLib integration
- [ ] Add high-frequency trading module
- [ ] Create video tutorial series
- [ ] Build interactive dashboards
- [ ] Add reinforcement learning for trading

---

**⭐ If you find this repository helpful, please consider giving it a star!**

---

*Last Updated: November 2, 2025*
