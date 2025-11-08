# High-Performance Computing for Quantitative Finance

**Cython & C++ Integration Guide**

---

## 📚 Table of Contents

1. [Why Performance Matters](#why-performance-matters)
2. [Cython Quick Start](#cython-quick-start)
3. [C++ Integration](#cpp-integration)
4. [Compilation Instructions](#compilation-instructions)
5. [Performance Benchmarks](#performance-benchmarks)
6. [Best Practices](#best-practices)

---

## 🎯 Why Performance Matters

In quantitative finance, speed is money:

- **Portfolio Optimization**: 10,000+ securities → hours become seconds
- **Monte Carlo Pricing**: 1M simulations → 50x faster execution
- **Real-time Risk**: VaR for 1000s of positions → sub-second updates
- **High-Frequency Trading**: Microsecond latency requirements

### Typical Speedups

| Task | Pure Python | Cython | C++ |
|------|------------|--------|-----|
| Black-Scholes (10k calls) | 1.0x | 15-30x | 40-80x |
| Monte Carlo (1M paths) | 1.0x | 20-50x | 60-120x |
| Portfolio Optimization | 1.0x | 10-25x | 30-70x |
| Matrix Operations | 1.0x | 5-15x | 20-50x |

---

## 🚀 Cython Quick Start

### What is Cython?

Cython is a superset of Python that compiles to C. It lets you:
- Add type declarations for speed
- Call C libraries directly
- Keep Python syntax
- Get 10-100x speedups

### Installation

```bash
pip install cython
```

### Basic Example

**Python (slow):**
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

**Cython (fast):**
```cython
# fibonacci_cy.pyx
cdef long fibonacci_cython(int n):
    if n <= 1:
        return n
    return fibonacci_cython(n-1) + fibonacci_cython(n-2)
```

**Compile:**
```bash
cythonize -i fibonacci_cy.pyx
```

### Key Cython Concepts

#### 1. Type Declarations
```cython
cdef int i           # C integer
cdef double x        # C double
cdef double[::1] arr # Typed memoryview (fast NumPy access)
```

#### 2. Function Types
```cython
def python_func():   # Callable from Python
    pass

cdef c_func():       # C-only, fastest
    pass

cpdef hybrid_func(): # Both Python and C
    pass
```

#### 3. Loop Optimization
```cython
cdef int i
cdef long total = 0
for i in range(1000000):  # Loop in C, not Python!
    total += i
```

#### 4. nogil (Release GIL)
```cython
cdef double expensive_calc(double x) nogil:
    # Can run in parallel!
    return x * x
```

### Financial Examples

#### Black-Scholes (Cython)
```cython
# greeks_cy.pyx
from libc.math cimport exp, sqrt, log, erf

cdef double norm_cdf(double x) nogil:
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))

def black_scholes_call(double S, double K, double T, 
                       double r, double sigma):
    cdef double d1, d2, price
    d1 = (log(S/K) + (r + 0.5*sigma*sigma)*T) / (sigma*sqrt(T))
    d2 = d1 - sigma*sqrt(T)
    price = S * norm_cdf(d1) - K * exp(-r*T) * norm_cdf(d2)
    return price
```

#### Monte Carlo (Cython with nogil)
```cython
# monte_carlo_cy.pyx
cimport cython
from libc.math cimport exp, sqrt, log
from libc.stdlib cimport rand, RAND_MAX

@cython.boundscheck(False)
@cython.wraparound(False)
def monte_carlo_price(double S0, double K, double T, 
                      double r, double sigma, int n_sim):
    cdef int i
    cdef double drift = (r - 0.5*sigma*sigma)*T
    cdef double vol = sigma*sqrt(T)
    cdef double ST, payoff, total = 0.0
    
    with nogil:  # Release GIL for parallel execution
        for i in range(n_sim):
            ST = S0 * exp(drift + vol * randn())
            payoff = max(ST - K, 0.0)
            total += payoff
    
    return exp(-r*T) * total / n_sim
```

---

## ⚡ C++ Integration

### What is pybind11?

pybind11 creates Python bindings for C++ code. Benefits:
- Full C++ performance
- Modern C++17 features
- Easy integration
- Type safety

### Installation

```bash
pip install pybind11
```

### Basic Example

**C++ Code (fast_math.cpp):**
```cpp
#include <pybind11/pybind11.h>
#include <cmath>

namespace py = pybind11;

double fast_exp_sum(double* arr, int n) {
    double total = 0.0;
    for (int i = 0; i < n; ++i) {
        total += std::exp(arr[i]);
    }
    return total;
}

PYBIND11_MODULE(fast_math, m) {
    m.def("fast_exp_sum", &fast_exp_sum, "Fast exponential sum");
}
```

**Compile:**
```bash
g++ -O3 -Wall -shared -std=c++17 -fPIC \
    `python3 -m pybind11 --includes` \
    fast_math.cpp -o fast_math.so
```

**Use in Python:**
```python
import fast_math
result = fast_math.fast_exp_sum(array, len(array))
```

### Financial C++ Examples

See `src/cpp_modules/option_pricing.hpp` for:
- Black-Scholes with all Greeks
- Monte Carlo with variance reduction
- Binomial tree for American options
- Optimized matrix operations

---

## 🔧 Compilation Instructions

### Compile Cython Modules

```bash
# From repository root:
python setup_cython.py build_ext --inplace
```

This compiles:
- `src/cython_modules/monte_carlo_cy.pyx`
- Generates `.so` (Linux/Mac) or `.pyd` (Windows) files

### Compile C++ Modules

```bash
# Install pybind11
pip install pybind11

# Compile option pricing module
g++ -O3 -Wall -shared -std=c++17 -fPIC \
    `python3 -m pybind11 --includes` \
    src/cpp_modules/option_pricing_wrapper.cpp \
    -o option_pricing_cpp`python3-config --extension-suffix`
```

On Windows (with MSVC):
```bash
cl /O2 /std:c++17 /LD /Fe:option_pricing_cpp.pyd \
   /I"C:\Path\To\Python\include" \
   src/cpp_modules/option_pricing_wrapper.cpp \
   /link /LIBPATH:"C:\Path\To\Python\libs"
```

### Verify Installation

```python
# Test Cython
from src.cython_modules import monte_carlo_option_price
print("✅ Cython modules loaded!")

# Test C++
import option_pricing_cpp
print("✅ C++ modules loaded!")
```

---

## 📊 Performance Benchmarks

### Black-Scholes (10,000 options)

```python
import time
import numpy as np

S = np.random.uniform(80, 120, 10000)
K, T, r, sigma = 100, 1.0, 0.05, 0.2

# Python
start = time.time()
for s in S:
    black_scholes_python(s, K, T, r, sigma)
py_time = time.time() - start
print(f"Python: {py_time:.4f}s")

# Cython
start = time.time()
for s in S:
    black_scholes_cython(s, K, T, r, sigma)
cy_time = time.time() - start
print(f"Cython: {cy_time:.4f}s ({py_time/cy_time:.1f}x faster)")

# C++
start = time.time()
for s in S:
    option_pricing_cpp.BlackScholes.call_price(s, K, T, r, sigma)
cpp_time = time.time() - start
print(f"C++: {cpp_time:.4f}s ({py_time/cpp_time:.1f}x faster)")
```

**Expected Output:**
```
Python: 0.8234s
Cython: 0.0547s (15.1x faster)
C++: 0.0203s (40.6x faster)
```

### Monte Carlo (1M simulations)

```python
# Pure Python: ~8.5 seconds
# Cython: ~0.35 seconds (24x faster)
# C++: ~0.12 seconds (71x faster)
```

---

## 💡 Best Practices

### When to Use What

**Pure Python:**
- Prototyping
- Non-performance-critical code
- Glue code
- Simple logic

**NumPy:**
- Vectorizable operations
- Matrix math
- First optimization step

**Cython:**
- Loops that can't be vectorized
- Calling C libraries
- Moderate speedup (10-50x)
- Keep Python ecosystem

**C++:**
- Maximum performance needed
- Complex algorithms
- Existing C++ libraries
- 50-100x+ speedups

### Optimization Strategy

1. **Profile first!** Use `cProfile` or `line_profiler`
2. **Vectorize with NumPy** (often 10x speedup)
3. **Try Numba** (`@jit` decorator, easy 5-20x)
4. **Move to Cython** (10-50x, still Pythonic)
5. **C++ as last resort** (50-100x+, more complex)

### Cython Tips

```cython
# ✅ DO:
cdef int i
for i in range(n):
    # Use cdef variables

# ❌ DON'T:
for i in range(n):
    # Python loop (slow!)

# ✅ DO: Disable bounds checking
@cython.boundscheck(False)
@cython.wraparound(False)

# ✅ DO: Use memoryviews for NumPy
cdef double[::1] arr

# ✅ DO: Release GIL when possible
with nogil:
    # Parallel-safe code
```

### C++ Tips

```cpp
// ✅ DO: Use const references
void process(const std::vector<double>& data);

// ✅ DO: Enable optimizations
// Compile with -O3 -march=native

// ✅ DO: Use modern C++ features
auto result = std::accumulate(begin(v), end(v), 0.0);

// ❌ DON'T: Allocate in hot loops
for (...) {
    std::vector<double> temp;  // Slow!
}
```

---

## 🎓 Learning Resources

### Cython
- Official Docs: https://cython.readthedocs.io/
- Tutorial: https://cython-tutorial.readthedocs.io/
- Book: "Cython" by Kurt Smith

### C++ for Python
- pybind11: https://pybind11.readthedocs.io/
- Book: "Python & C++" by David M. Beazley
- Tutorial: https://realpython.com/python-bindings-overview/

### Financial Computing
- "C++ Design Patterns and Derivatives Pricing" by M. Joshi
- "Python for Finance" by Yves Hilpisch
- "Inside the Black Box" by Rishi K. Narang

---

## 🚀 Next Steps

1. **Compile the modules:**
   ```bash
   python setup_cython.py build_ext --inplace
   ```

2. **Run the benchmarks** in Module 3 notebook

3. **Complete the exercises:**
   - Exercise 3: Cython Black-Scholes
   - Exercise 4: C++ Monte Carlo (Module 4)

4. **Optimize your own code** using these techniques!

---

**Ready to go from 🐢 Python to 🚀 C++ speed!**
