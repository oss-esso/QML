# Quick Start Guide - Implementation Exercises

## 🎯 Goal
Learn to implement Black-Scholes in Python, Cython, and C++ while comparing performance.

## ⏱️ Time Estimate
- Cython: 30 minutes
- C++: 1-2 hours  
- Testing: 10 minutes
- **Total: 2-3 hours**

---

## 📋 Quick Checklist

### Phase 1: Learn (20 minutes)
- [ ] Open `04_Implementation_Comparison.ipynb`
- [ ] Run Cells 1-8 to see Python implementation
- [ ] Read Cell 24 (Cython overview)
- [ ] Read Cell 26 (C++ overview)

### Phase 2: Cython (30 minutes)
- [ ] Read Cell 25 STEP 1-3 (understand concepts)
- [ ] Follow Cell 25 STEP 4 checklist:
  - [ ] Create `src/cython_modules/black_scholes_cy.pyx`
  - [ ] Add imports from libc.math
  - [ ] Implement norm_cdf and norm_pdf helpers
  - [ ] Implement call_price and put_price
- [ ] Compile: `python setup_cython.py build_ext --inplace`
- [ ] Test with Cell 25 STEP 5 code

### Phase 3: C++ (1-2 hours)
- [ ] Read Cell 27 STEP 1-3 (understand C++ syntax)
- [ ] Follow Cell 27 STEP 4 checklist - Part A:
  - [ ] Create `src/cpp_modules/black_scholes.hpp`
  - [ ] Add header guards and includes
  - [ ] Create namespace FinancialMath
  - [ ] Implement BlackScholes class with helpers
  - [ ] Implement call_price and put_price
- [ ] Follow Cell 27 STEP 4 checklist - Part B:
  - [ ] Create `src/cpp_modules/black_scholes_wrapper.cpp`
  - [ ] Add pybind11 includes
  - [ ] Create PYBIND11_MODULE binding
- [ ] Compile with g++ command from Cell 27 STEP 4
- [ ] Test with Cell 27 STEP 5 code

### Phase 4: Verify (10 minutes)
- [ ] Run Cell 29 (comprehensive benchmark)
- [ ] Check results table
- [ ] Verify speedups:
  - [ ] Cython: 5-20x faster
  - [ ] C++: 100-500x faster
- [ ] Review learning outcomes

---

## 🚀 Quick Commands

```bash
# After implementing Cython
cd /Users/edoardospigarolo/Documents/QML
python setup_cython.py build_ext --inplace

# After implementing C++
cd /Users/edoardospigarolo/Documents/QML
g++ -O3 -Wall -shared -std=c++17 -fPIC -undefined dynamic_lookup \
    `python3 -m pybind11 --includes` \
    src/cpp_modules/black_scholes_wrapper.cpp \
    -o black_scholes_cpp.so
```

---

## 📚 Where Everything Is

| Item | Location |
|------|----------|
| Main Notebook | `04_Implementation_Comparison.ipynb` |
| Python Intro | Cells 1-23 |
| **Cython Exercise** | **Cells 24-25** |
| **C++ Exercise** | **Cells 26-27** |
| **Final Test** | **Cells 28-29** |
| Full Guide | `EXERCISE_TODO_CELLS_GUIDE.md` |
| Summary | `EXERCISE_CELLS_SUMMARY.md` |
| This File | `QUICK_START.md` |

---

## 🔑 Key Concepts

### Python → Cython
```python
# Before: Python
def call_price(S, K, T, r, sigma):
    return S * norm.cdf(d1) - ...

# After: Cython with types
def call_price(double S, double K, double T, double r, double sigma):
    cdef double d1, d2
    return S * norm_cdf(d1) - ...
```

### Python → C++
```cpp
// Create header file: black_scholes.hpp
namespace FinancialMath {
    class BlackScholes {
        static double call_price(double S, double K, double T, double r, double sigma) {
            return S * norm_cdf(d1) - ...;
        }
    };
}

// Create wrapper: black_scholes_wrapper.cpp
PYBIND11_MODULE(black_scholes_cpp, m) {
    py::class_<BlackScholes>(m, "BlackScholes")
        .def_static("call_price", &BlackScholes::call_price, ...);
}
```

---

## ✅ Success Indicators

### Cython Working ✓
```
✅ File created: src/cython_modules/black_scholes_cy.pyx
✅ Compilation: No errors
✅ Import: from src.cython_modules.black_scholes_cy import call_price
✅ Speed: 5-20x faster than Python
```

### C++ Working ✓
```
✅ Files created: src/cpp_modules/black_scholes.hpp + wrapper.cpp
✅ Compilation: No errors
✅ Import: import black_scholes_cpp
✅ Speed: 100-500x faster than Python
```

### Both Working ✓
```
✅ Cell 29 runs without errors
✅ Results table shows all three implementations
✅ Speedup values match expectations
✅ All verification checks pass
```

---

## 🆘 Troubleshooting

### Cython Won't Compile
1. Check file is named `black_scholes_cy.pyx` (not `.py`)
2. Verify directives at top of file
3. Run: `python setup_cython.py build_ext --inplace`
4. Check for type annotation errors

### C++ Won't Compile
1. Check both files exist (.hpp and .cpp)
2. Verify `#ifndef` / `#define` guards in header
3. Check `std::` prefix on all math functions
4. Run from project root: `/Users/edoardospigarolo/Documents/QML`

### Slow Performance
- **Cython**: Add type annotations (check for any `cdef` missing)
- **C++**: Use `-O3` flag in compilation
- Both: Check you're using C math library, not NumPy

### Import Errors
- **Cython**: Run `python setup_cython.py build_ext --inplace`
- **C++**: Run the g++ command to create `.so` file
- Both: Verify files are in correct directories

---

## 📊 Expected Results

### Benchmark Results
```
Python:   ~5ms per 10,000 options (2,000 opts/sec)
Cython:   ~0.5ms per 10,000 options (20,000 opts/sec) → ~10x faster
C++:      ~0.01ms per 10,000 options (1,000,000 opts/sec) → ~500x faster
```

### Cell 29 Output
```
🔹 Benchmark with 1000 options:
  🐢 Python: ✅ Time: 0.0050s | Throughput: 200,000 opts/sec
  🚀 Cython: ✅ Time: 0.0005s | Throughput: 2,000,000 opts/sec | Speedup: 10.0x
  ⚡ C++:    ✅ Time: 0.0001s | Throughput: 10,000,000 opts/sec | Speedup: 50.0x
```

---

## 🎓 What You'll Learn

After completing:
1. ✅ How to add type annotations for speed
2. ✅ How to use C math libraries efficiently
3. ✅ How C++ outperforms Python
4. ✅ When to use each implementation
5. ✅ How to create Python bindings with pybind11

---

## 🚀 Next Level

Once you've mastered all three:
- [ ] Add Greeks calculations (Delta, Gamma, Vega)
- [ ] Implement American option pricing
- [ ] Create vectorized versions
- [ ] Try GPU implementations (CUDA)
- [ ] Profile with actual trading data

---

**Ready to start? Open the notebook and jump to Cell 25! 🚀**
