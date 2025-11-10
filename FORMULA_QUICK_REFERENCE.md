# Quick Reference Guide - Key Formulas

## Chapter 1: Probability and Risk Metrics

### Expected Value and Variance
- **Expected Value**: $E[X] = \int x f(x) dx$ (continuous), $E[X] = \sum x p(x)$ (discrete)
- **Variance**: $\text{Var}(X) = E[X^2] - (E[X])^2$
- **Standard Deviation**: $\sigma = \sqrt{\text{Var}(X)}$

### Distribution Parameters
- **Normal Distribution**: $X \sim N(\mu, \sigma^2)$, PDF: $f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-(x-\mu)^2/(2\sigma^2)}$
- **Skewness**: $\text{Skew} = E[(X-\mu)^3]/\sigma^3$
- **Kurtosis**: $\text{Kurt} = E[(X-\mu)^4]/\sigma^4 - 3$ (excess)

### Value-at-Risk (VaR)
- **Historical VaR**: $\text{VaR}_\alpha = -Q_\alpha(\text{returns})$ where $Q_\alpha$ is the $\alpha$-quantile
- **Parametric VaR**: $\text{VaR}_\alpha = -(\mu + \sigma z_\alpha)$ where $z_\alpha = \Phi^{-1}(1-\alpha)$
- **CVaR**: $\text{CVaR}_\alpha = E[L | L > \text{VaR}_\alpha]$

### Performance Metrics
- **Sharpe Ratio**: $\text{SR} = \frac{E[R - R_f]}{\sigma_R}$
- **Sortino Ratio**: $\text{Sortino} = \frac{E[R - R_f]}{\sigma_{\text{downside}}}$
- **Information Ratio**: $\text{IR} = \frac{E[R_p - R_b]}{\text{TE}}$

## Chapter 2: Stochastic Processes

### Brownian Motion
- **Basic Properties**: $W_0 = 0$, $W_t - W_s \sim N(0, t-s)$, $E[W_t] = 0$, $\text{Var}(W_t) = t$
- **Covariance**: $\text{Cov}(W_s, W_t) = \min(s,t)$
- **Scaling**: $W_{ct} \stackrel{d}{=} \sqrt{c} W_t$

### Geometric Brownian Motion (GBM)
- **SDE**: $dS_t = \mu S_t dt + \sigma S_t dW_t$
- **Solution**: $S_t = S_0 \exp((\mu - \sigma^2/2)t + \sigma W_t)$
- **Moments**: $E[S_t] = S_0 e^{\mu t}$, $\text{Var}(S_t) = S_0^2 e^{2\mu t}(e^{\sigma^2 t} - 1)$

### Ornstein-Uhlenbeck Process
- **SDE**: $dX_t = \theta(\mu - X_t) dt + \sigma dW_t$
- **Mean**: $E[X_t] = \mu + (X_0 - \mu)e^{-\theta t}$
- **Variance**: $\text{Var}(X_t) = \frac{\sigma^2}{2\theta}(1 - e^{-2\theta t})$
- **Half-Life**: $t_{1/2} = \ln(2)/\theta$
- **Stationary Distribution**: $X_\infty \sim N(\mu, \sigma^2/(2\theta))$

## Chapter 3: Stochastic Calculus and Options

### Itô's Lemma
For $dX_t = \mu dt + \sigma dW_t$ and $Y_t = f(t, X_t)$:
$$dY_t = \left(\frac{\partial f}{\partial t} + \mu \frac{\partial f}{\partial x} + \frac{1}{2}\sigma^2 \frac{\partial^2 f}{\partial x^2}\right) dt + \sigma \frac{\partial f}{\partial x} dW_t$$

### Black-Scholes Formula
**Call Option**:
$$C = S N(d_1) - K e^{-rT} N(d_2)$$

**Put Option**:
$$P = K e^{-rT} N(-d_2) - S N(-d_1)$$

Where:
$$d_1 = \frac{\ln(S/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}}, \quad d_2 = d_1 - \sigma\sqrt{T}$$

### Option Greeks
- **Delta**: $\Delta_{\text{call}} = N(d_1)$, $\Delta_{\text{put}} = N(d_1) - 1$
- **Gamma**: $\Gamma = \frac{N'(d_1)}{S \sigma \sqrt{T}}$ (same for call/put)
- **Vega**: $\mathcal{V} = S N'(d_1) \sqrt{T}$ (same for call/put)
- **Theta (call)**: $\Theta = -\frac{S N'(d_1) \sigma}{2\sqrt{T}} - rKe^{-rT}N(d_2)$
- **Rho (call)**: $\rho = KT e^{-rT} N(d_2)$

### Put-Call Parity
$$C - P = S - Ke^{-rT}$$

## Chapter 4: Machine Learning

### AR(1) Process
- **Model**: $X_t = \phi X_{t-1} + \epsilon_t$
- **Stationarity**: $|\phi| < 1$
- **Variance**: $\text{Var}(X_t) = \sigma^2/(1-\phi^2)$
- **Autocorrelation**: $\text{Corr}(X_t, X_{t-k}) = \phi^k$

### GARCH(1,1)
- **Model**: $\sigma_t^2 = \omega + \alpha \epsilon_{t-1}^2 + \beta \sigma_{t-1}^2$
- **Unconditional Variance**: $E[\sigma_t^2] = \omega/(1-\alpha-\beta)$
- **Persistence**: $\alpha + \beta$
- **Half-Life**: $t_{1/2} = \ln(0.5)/\ln(\alpha+\beta)$

### GJR-GARCH(1,1)
$$\sigma_t^2 = \omega + (\alpha + \gamma I_{t-1})\epsilon_{t-1}^2 + \beta \sigma_{t-1}^2$$
where $I_{t-1} = 1$ if $\epsilon_{t-1} < 0$, else 0

### Model Selection
- **AIC**: $-2\log L + 2k$
- **BIC**: $-2\log L + k\log n$
(Lower is better)

## Chapter 5: Portfolio Optimization

### Mean-Variance Optimization
- **Portfolio Return**: $\mu_p = w^T \mu$
- **Portfolio Variance**: $\sigma_p^2 = w^T \Sigma w$
- **Sharpe Ratio**: $\text{SR}_p = \frac{w^T\mu - r_f}{\sqrt{w^T\Sigma w}}$

### Minimum Variance Portfolio
$$w_{\text{mv}} = \frac{\Sigma^{-1} \mathbf{1}}{\mathbf{1}^T \Sigma^{-1} \mathbf{1}}$$

### Tangency Portfolio (Maximum Sharpe)
$$w_{\text{tan}} = \frac{\Sigma^{-1}(\mu - r_f\mathbf{1})}{\mathbf{1}^T\Sigma^{-1}(\mu - r_f\mathbf{1})}$$

### Risk Parity
- **Marginal Risk Contribution**: $\text{MRC}_i = \frac{(\Sigma w)_i}{\sigma_p}$
- **Risk Contribution**: $\text{RC}_i = w_i \cdot \text{MRC}_i = \frac{w_i (\Sigma w)_i}{\sigma_p}$
- **Constraint**: $\text{RC}_1 = \text{RC}_2 = \cdots = \text{RC}_n$

### CAPM
$$E[R_i] - R_f = \beta_i (E[R_m] - R_f)$$
where $\beta_i = \text{Cov}(R_i, R_m)/\text{Var}(R_m)$

### Black-Litterman
**Posterior Returns**:
$$E[\mu | \text{views}] = [(\tau\Sigma)^{-1} + P^T\Omega^{-1}P]^{-1}[(\tau\Sigma)^{-1}\Pi + P^T\Omega^{-1}Q]$$

### Performance Metrics
- **Maximum Drawdown**: $\text{MDD} = \max_{t} \frac{\max_{s \leq t} V(s) - V(t)}{\max_{s \leq t} V(s)}$
- **Calmar Ratio**: $\text{Calmar} = \frac{E[R_p]}{\text{MDD}}$

## Common Distributions

### Standard Normal
- PDF: $\phi(x) = \frac{1}{\sqrt{2\pi}} e^{-x^2/2}$
- CDF: $\Phi(x) = \int_{-\infty}^x \phi(t) dt$
- Quantiles: $\Phi^{-1}(0.95) \approx 1.645$, $\Phi^{-1}(0.975) \approx 1.96$, $\Phi^{-1}(0.99) \approx 2.326$

### Lognormal
If $\log X \sim N(\mu, \sigma^2)$:
- $E[X] = e^{\mu + \sigma^2/2}$
- $\text{Var}(X) = e^{2\mu + \sigma^2}(e^{\sigma^2} - 1)$

## Useful Approximations

### Volatility Scaling
- **Daily to Annual**: $\sigma_{\text{annual}} \approx \sigma_{\text{daily}} \times \sqrt{252}$
- **Weekly to Annual**: $\sigma_{\text{annual}} \approx \sigma_{\text{weekly}} \times \sqrt{52}$
- **Monthly to Annual**: $\sigma_{\text{annual}} \approx \sigma_{\text{monthly}} \times \sqrt{12}$

### Return Approximations
- **Log Return**: $r_t = \log(P_t/P_{t-1}) \approx (P_t - P_{t-1})/P_{t-1}$ for small returns
- **Annualization**: $r_{\text{annual}} = 252 \times \bar{r}_{\text{daily}}$

## Python Quick Reference

```python
# VaR (95%)
var_95 = -np.percentile(returns, 5)

# CVaR
cvar_95 = -returns[returns <= -var_95].mean()

# Sharpe Ratio (annualized)
sharpe = np.sqrt(252) * returns.mean() / returns.std()

# GARCH(1,1)
from arch import arch_model
model = arch_model(returns*100, vol='Garch', p=1, q=1)
result = model.fit(disp='off')

# Portfolio Optimization
from scipy.optimize import minimize
def portfolio_var(w, cov):
    return w.T @ cov @ w
result = minimize(portfolio_var, x0, args=(cov,), constraints=cons, bounds=bnds)
```

---

This quick reference covers the most essential formulas from all 5 chapters. For complete derivations and context, refer to the full technical report.
