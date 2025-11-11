# Added TODO Exercises to Implementation Comparison Notebook

## Summary of New Cells

The notebook now includes **3 new TODO/Exercise sections** at the end (cells 18-23) that teach you how to implement Cython and C++ versions while keeping Python side-by-side for comparison.

---

## Cell 18: Markdown Introduction to Cython Exercise
**Location:** After "Part 8: Key Takeaways"

**Content:**
- Overview of the Cython implementation exercise
- Cython basics and advantages
- Background on type annotations
- Step-by-step guide to create `src/cython_modules/black_scholes_cy.pyx`

**Key Concepts Taught:**
- Cython type annotations (`cdef`, `double`, `int`)
- Helper functions for normal CDF and PDF
- Integration with existing codebase

---

## Cell 19: Cython Implementation TODO
**Type:** Python (Executable)

**What It Does:**
1. Displays a complete Cython template with TODOs
2. Shows the exact structure you need to implement
3. Tests the Python baseline with 10,000 options
4. Provides expected performance metrics
5. Includes troubleshooting guide

**Template Provided:**
```python
# Complete .pyx file template with:
# - Cython directives for optimization
# - norm_cdf implementation
# - norm_pdf implementation  
# - call_price function
# - put_price function
```

**Output:**
- Shows performance expectations (5-20x faster than Python)
- Displays the template code you can copy/paste
- Provides verification steps

---

## Cell 20: Markdown Introduction to C++ Exercise
**Location:** After Cython exercise

**Content:**
- Overview of C++ implementation with pybind11
- Advantages and challenges of C++
- Background on C++ financial math
- Step-by-step guide for two files:
  - `src/cpp_modules/black_scholes.hpp` (header)
  - `src/cpp_modules/black_scholes_wrapper.cpp` (pybind11 wrapper)

**Key Concepts Taught:**
- C++ namespaces and classes
- Math functions: `std::exp`, `std::log`, `std::sqrt`, `std::erf`
- pybind11 bindings for Python
- Compilation flags and requirements

---

## Cell 21: C++ Implementation TODO
**Type:** Python (Executable)

**What It Does:**
1. Explains the goals and advantages of C++
2. Details the implementation structure
3. Benchmarks Python with 100,000 options
4. Shows expected C++ performance (100-200x faster)
5. Provides file structure guide
6. Lists common mistakes to avoid
7. Testing checklist

**Performance Expectations:**
- Python baseline: ~6 seconds for 100k options
- C++ expected: ~0.03 seconds (200x speedup)
- Throughput gain: From ~16k to ~3M options/sec

**Common Mistakes Section:**
- Compilation issues
- Linker problems
- Type mismatches
- pybind11 binding errors

---

## Cell 22: Final Exercise Markdown
**Location:** Before the comprehensive benchmark

**Content:**
- Introduction to the final testing framework
- How to verify your implementations
- Comparison methodology

---

## Cell 23: Final Benchmark TODO
**Type:** Python (Executable)

**What It Does:**
1. **Comprehensive Benchmark:**
   - Tests Python (always available as reference)
   - Tests your Cython implementation (if compiled)
   - Tests your C++ implementation (if compiled)
   - Tests with 1,000 and 10,000 options

2. **Performance Metrics:**
   - Execution time in seconds
   - Throughput (options/sec)
   - Speedup factor vs Python

3. **Results Summary:**
   - Creates a comparison table
   - Shows all three implementations side-by-side
   - Provides verification checklist

4. **Learning Outcomes:**
   - Trade-offs recap
   - When to use each approach
   - Key concepts learned

---

## How to Use These Exercises

### Step 1: Review Python Baseline
Run cells 1-8 first to understand the existing implementations.

### Step 2: Learn Cython (Cell 19)
- Copy the template code provided
- Create `src/cython_modules/black_scholes_cy.pyx`
- Implement the functions with type annotations
- Compile: `python setup_cython.py build_ext --inplace`

### Step 3: Learn C++ (Cells 20-21)
- Create `src/cpp_modules/black_scholes.hpp`
- Create `src/cpp_modules/black_scholes_wrapper.cpp`
- Compile with the g++ command provided
- Test the import

### Step 4: Benchmark Everything (Cell 23)
- Run the comprehensive benchmark
- Compare your implementations with Python
- Verify speedup factors
- Review learning outcomes

---

## What You'll Learn

### Cython Exercise
✅ How to add type annotations to Python code
✅ How Cython compilation works
✅ Expected 5-20x performance improvement
✅ When Cython is worth the effort
✅ How to verify your implementation is correct

### C++ Exercise
✅ How to write high-performance C++ code
✅ How pybind11 creates Python bindings
✅ Expected 100-500x performance improvement
✅ When C++ optimization is justified
✅ How to compile and link C++ extensions

### Final Benchmark
✅ How to properly measure performance
✅ How to compare multiple implementations
✅ How to verify correctness across implementations
✅ Decision-making criteria for choosing implementations

---

## Expected Results

After completing the exercises:

| Implementation | Time (1000 opts) | Time (10k opts) | Speedup | Status |
|---|---|---|---|---|
| Python | ~0.004s | ~0.04s | 1.0x | Baseline |
| Your Cython | ~0.001s | ~0.008s | 5-20x | Should compile ✅ |
| Your C++ | ~0.0001s | ~0.0005s | 100-500x | Should compile ✅ |

---

## Troubleshooting

### Cython Issues
- **Compilation fails:** Check for typos in type annotations
- **Import fails:** Verify file path and namespace
- **No speedup:** Check that `cdef` types are declared

### C++ Issues
- **Compilation fails:** Missing `-fPIC` or compiler not found
- **Import fails:** Wrong module name or missing pybind11
- **Linking fails:** Wrong architecture flags
- **Results don't match:** Check math in d1, d2 calculations

---

## Next Steps After Exercises

1. **Optimize further:**
   - Add vectorized operations
   - Implement batch pricing
   - Add Greeks calculations

2. **Add more functions:**
   - American options
   - Exotic options
   - Volatility surface models

3. **Production deployment:**
   - Add error handling
   - Implement caching
   - Create configuration system

---

## File Organization

```
QML/
├── Proba/
│   └── Module3_Stochastic_Calculus/
│       ├── 04_Implementation_Comparison.ipynb  (This notebook)
│       └── IMPLEMENTATION_COMPARISON_GUIDE.md
├── src/
│   ├── cython_modules/
│   │   ├── __init__.py
│   │   ├── monte_carlo_cy.pyx (Existing)
│   │   └── black_scholes_cy.pyx (TODO: Your implementation)
│   └── cpp_modules/
│       ├── option_pricing.hpp (Existing reference)
│       ├── option_pricing_wrapper.cpp (Existing reference)
│       ├── black_scholes.hpp (TODO: Your implementation)
│       └── black_scholes_wrapper.cpp (TODO: Your implementation)
└── setup_cython.py (Update to include your new .pyx file)
```

---

## Quick Reference

### Cython Template Commands
```bash
# Create and edit
touch src/cython_modules/black_scholes_cy.pyx

# Compile
python setup_cython.py build_ext --inplace

# Test import
python -c "from src.cython_modules.black_scholes_cy import call_price"
```

### C++ Compilation Command
```bash
g++ -O3 -shared -std=c++17 -fPIC -undefined dynamic_lookup \
    `python3 -m pybind11 --includes` \
    src/cpp_modules/black_scholes_wrapper.cpp \
    -o black_scholes_cpp.so
```

### Testing in Python
```python
# Cython
from src.cython_modules.black_scholes_cy import call_price
result = call_price(100, 100, 1, 0.05, 0.2)

# C++
import black_scholes_cpp
result = black_scholes_cpp.BlackScholes.call_price(100, 100, 1, 0.05, 0.2)
```

---

## Additional Resources

- Cython Documentation: https://cython.readthedocs.io/
- pybind11 Documentation: https://pybind11.readthedocs.io/
- Black-Scholes Formula: https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model
- C++ Math Library: https://en.cppreference.com/w/cpp/numeric/math

---

**Estimated Time to Complete:**
- Review: 10 minutes
- Cython implementation: 30 minutes
- C++ implementation: 1-2 hours
- Testing and optimization: 30 minutes
- **Total: 2-3 hours of hands-on learning**

Happy coding! 🚀
