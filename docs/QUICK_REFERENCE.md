# Cython & C++ Quick Reference Card

## 🚀 Compilation Commands

```bash
# Compile everything
make all

# Cython only
python setup_cython.py build_ext --inplace

# C++ only
g++ -O3 -Wall -shared -std=c++17 -fPIC \
    `python3 -m pybind11 --includes` \
    src/cpp_modules/option_pricing_wrapper.cpp \
    -o option_pricing_cpp.so

# Clean build files
make clean
```

---

## 📝 Cython Syntax Cheat Sheet

### Type Declarations
```cython
cdef int i                    # C integer
cdef double x                 # C double  
cdef double[::1] arr          # 1D memoryview
cdef double[:, ::1] matrix    # 2D memoryview
cdef list py_list             # Python list
```

### Function Types
```cython
def py_func():     # Python-callable
    pass

cdef c_func():     # C-only (fastest)
    pass

cpdef both():      # Both Python & C
    pass
```

### Compiler Directives
```cython
@cython.boundscheck(False)   # Disable bounds checking
@cython.wraparound(False)    # Disable negative indexing
@cython.cdivision(True)      # C division semantics
```

### Import C Libraries
```cython
from libc.math cimport exp, sqrt, log, sin, cos, erf
from libc.stdlib cimport rand, RAND_MAX, malloc, free
from libc.time cimport time
```

### Release GIL
```cython
with nogil:
    # Code here can run in parallel
    for i in range(n):
        result += compute(i)
```

---

## ⚡ C++ Syntax Cheat Sheet

### pybind11 Module
```cpp
#include <pybind11/pybind11.h>
namespace py = pybind11;

PYBIND11_MODULE(module_name, m) {
    m.doc() = "Description";
    m.def("function", &cpp_function);
}
```

### Expose Class
```cpp
py::class_<MyClass>(m, "MyClass")
    .def(py::init<int>())
    .def("method", &MyClass::method)
    .def_readonly("value", &MyClass::value);
```

### NumPy Arrays
```cpp
#include <pybind11/numpy.h>

py::array_t<double> process(py::array_t<double> input) {
    auto buf = input.request();
    double *ptr = static_cast<double*>(buf.ptr);
    // Process ptr[i]
}
```

---

## 📊 Performance Comparison

| Feature | Python | NumPy | Cython | C++ |
|---------|--------|-------|--------|-----|
| Dev Speed | ⚡⚡⚡ | ⚡⚡⚡ | ⚡⚡ | ⚡ |
| Run Speed | 1x | 10x | 30x | 80x |
| Syntax | Easy | Easy | Medium | Hard |
| Debugging | Easy | Easy | Medium | Hard |

---

## 🎯 When to Use What

**Pure Python:**
- Prototyping
- Glue code
- I/O operations

**NumPy:**
- Vectorizable operations
- Matrix math
- First optimization

**Cython:**
- Loops (can't vectorize)
- Need 10-50x speedup
- Call C libraries

**C++:**
- Maximum performance
- 50-100x+ speedup
- Complex algorithms

---

## 💡 Common Patterns

### Monte Carlo (Cython)
```cython
%%cython
from libc.math cimport exp, sqrt, log
from libc.stdlib cimport rand, RAND_MAX

cdef double randn() nogil:
    # Box-Muller transform
    cdef double u1 = rand() / RAND_MAX
    cdef double u2 = rand() / RAND_MAX
    return sqrt(-2*log(u1)) * cos(2*3.14159*u2)

def monte_carlo(double S0, double K, double T, 
                double r, double sigma, int n):
    cdef int i
    cdef double drift = (r - 0.5*sigma*sigma)*T
    cdef double vol = sigma*sqrt(T)
    cdef double ST, payoff, total = 0.0
    
    with nogil:
        for i in range(n):
            ST = S0 * exp(drift + vol*randn())
            payoff = max(ST - K, 0.0)
            total += payoff
    
    return exp(-r*T) * total / n
```

### Black-Scholes (C++)
```cpp
double call_price(double S, double K, double T, 
                  double r, double sigma) {
    double d1 = (log(S/K) + (r + 0.5*sigma*sigma)*T) / 
                (sigma*sqrt(T));
    double d2 = d1 - sigma*sqrt(T);
    return S*norm_cdf(d1) - K*exp(-r*T)*norm_cdf(d2);
}
```

---

## 🔧 Debugging Tips

### Cython Annotation
```bash
cython -a myfile.pyx
# Open myfile.html to see Python vs C interactions
# Yellow = slow (Python), White = fast (C)
```

### Profiling
```python
%load_ext cython
%%cython
# cython: profile=True
def my_func():
    pass

# Then use cProfile
import cProfile
cProfile.run('my_func()')
```

### Common Errors
```cython
# ❌ Don't: Use Python loops
for i in range(n):
    result += arr[i]

# ✅ Do: Use cdef
cdef int i
for i in range(n):
    result += arr[i]

# ❌ Don't: Python objects in nogil
with nogil:
    py_list.append(x)  # Error!

# ✅ Do: Use C types only
with nogil:
    c_array[i] = x
```

---

## 📚 Import in Python

### After Compilation
```python
# Cython modules
from src.cython_modules import monte_carlo_option_price

price = monte_carlo_option_price(100, 100, 1.0, 0.05, 0.2, 100000)

# C++ modules
import option_pricing_cpp

bs = option_pricing_cpp.BlackScholes
price = bs.call_price(100, 100, 1.0, 0.05, 0.2)

mc = option_pricing_cpp.MonteCarlo(seed=42)
price = mc.european_option(100, 100, 1.0, 0.05, 0.2, 100000, True)
```

---

## ⚙️ Optimization Flags

### Cython (setup.py)
```python
extra_compile_args=[
    '-O3',           # Maximum optimization
    '-march=native', # Use CPU-specific instructions
    '-ffast-math',   # Aggressive math optimizations
]
```

### C++ (g++)
```bash
-O3                # Maximum optimization
-std=c++17         # C++17 standard
-march=native      # CPU-specific
-fPIC              # Position-independent code
-Wall              # All warnings
```

---

## 🎓 Learning Resources

- **Cython:** https://cython.readthedocs.io/
- **pybind11:** https://pybind11.readthedocs.io/
- **Guide:** `docs/CYTHON_CPP_GUIDE.md` (in this repo)

---

**Quick Start:** `make all` → Happy optimizing! 🚀
