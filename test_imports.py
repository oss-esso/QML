#!/usr/bin/env python3
"""Diagnostic script to test module imports and path setup."""

import sys
import os
import pathlib

print("=" * 80)
print("DIAGNOSTIC: Module Import Test")
print("=" * 80)

# Show current state
print(f"\n1. Current working directory: {os.getcwd()}")
print(f"   Python executable: {sys.executable}")
print(f"   Python version: {sys.version.split()[0]}")

# Find project root
p = pathlib.Path.cwd()
project_root = None
for _ in range(10):
    if (p / 'setup.py').exists() or (p / 'README.md').exists():
        project_root = str(p)
        break
    if p.parent == p:
        break
    p = p.parent

print(f"\n2. Project root: {project_root}")

# Add to path if needed
if project_root and project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"   Added to sys.path ✓")
else:
    print(f"   Already in sys.path ✓")

# Show sys.path
print(f"\n3. sys.path (first 5 entries):")
for i, p in enumerate(sys.path[:5]):
    print(f"   [{i}] {p}")

# Check file existence
print(f"\n4. Checking file existence:")
cython_file = pathlib.Path(project_root) / 'src' / 'cython_modules' / 'black_scholes_cy.cpython-313-darwin.so'
cpp_file = pathlib.Path(project_root) / 'black_scholes_cpp.cpython-313-darwin.so'

print(f"   Cython: {cython_file}")
print(f"   - Exists: {cython_file.exists()}")
if cython_file.exists():
    print(f"   - Size: {cython_file.stat().st_size} bytes")

print(f"   C++: {cpp_file}")
print(f"   - Exists: {cpp_file.exists()}")
if cpp_file.exists():
    print(f"   - Size: {cpp_file.stat().st_size} bytes")

# Check if __init__.py files exist
print(f"\n5. Checking __init__.py files:")
init_src = pathlib.Path(project_root) / 'src' / '__init__.py'
init_cython = pathlib.Path(project_root) / 'src' / 'cython_modules' / '__init__.py'

print(f"   src/__init__.py: {init_src.exists()}")
print(f"   src/cython_modules/__init__.py: {init_cython.exists()}")

# Try imports
print(f"\n6. Attempting imports:")
print("-" * 80)

print("\n   A) Testing Cython import (from src.cython_modules.black_scholes_cy):")
try:
    from src.cython_modules.black_scholes_cy import call_price as cy_call
    result = cy_call(100, 100, 1.0, 0.05, 0.2)
    print(f"      ✅ SUCCESS! call_price(100, 100, 1, 0.05, 0.2) = {result:.4f}")
except ModuleNotFoundError as e:
    print(f"      ❌ ModuleNotFoundError: {e}")
    print(f"      → Trying direct import from src.cython_modules...")
    try:
        import src.cython_modules.black_scholes_cy as cy_module
        result = cy_module.call_price(100, 100, 1.0, 0.05, 0.2)
        print(f"      ✅ Direct import worked! Result: {result:.4f}")
    except Exception as e2:
        print(f"      ❌ Also failed: {e2}")
except Exception as e:
    print(f"      ❌ {type(e).__name__}: {e}")

print("\n   B) Testing C++ import (import black_scholes_cpp):")
try:
    import black_scholes_cpp
    result = black_scholes_cpp.BlackScholes.call_price(100, 100, 1.0, 0.05, 0.2)
    print(f"      ✅ SUCCESS! call_price(100, 100, 1, 0.05, 0.2) = {result:.4f}")
except ModuleNotFoundError as e:
    print(f"      ❌ ModuleNotFoundError: {e}")
    print(f"      → Trying to import with importlib...")
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "black_scholes_cpp",
            str(cpp_file)
        )
        cpp_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cpp_module)
        result = cpp_module.BlackScholes.call_price(100, 100, 1.0, 0.05, 0.2)
        print(f"      ✅ importlib import worked! Result: {result:.4f}")
    except Exception as e2:
        print(f"      ❌ Also failed: {e2}")
except Exception as e:
    print(f"      ❌ {type(e).__name__}: {e}")

print("\n" + "=" * 80)
print("DIAGNOSIS COMPLETE")
print("=" * 80)
