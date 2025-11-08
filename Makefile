# Makefile for Compiling Cython and C++ Modules
#
# Usage:
#   make all       - Compile everything
#   make cython    - Compile Cython modules only
#   make cpp       - Compile C++ modules only
#   make clean     - Remove compiled files
#   make test      - Run performance tests

PYTHON := python3
CXX := g++
CXXFLAGS := -O3 -Wall -shared -std=c++17 -fPIC
PYTHON_INCLUDES := $(shell $(PYTHON) -m pybind11 --includes)
PYTHON_EXT_SUFFIX := $(shell $(PYTHON)-config --extension-suffix)

# Directories
SRC_CY := src/cython_modules
SRC_CPP := src/cpp_modules
BUILD := build

.PHONY: all cython cpp clean test help

all: cython cpp
	@echo "✅ All modules compiled successfully!"

help:
	@echo "Makefile for QML Cython/C++ modules"
	@echo ""
	@echo "Targets:"
	@echo "  all      - Compile all modules"
	@echo "  cython   - Compile Cython modules"
	@echo "  cpp      - Compile C++ modules"
	@echo "  clean    - Remove compiled files"
	@echo "  test     - Run performance tests"
	@echo "  help     - Show this message"

cython:
	@echo "🔨 Compiling Cython modules..."
	$(PYTHON) setup_cython.py build_ext --inplace
	@echo "✅ Cython compilation complete!"

cpp:
	@echo "🔨 Compiling C++ modules..."
	$(CXX) $(CXXFLAGS) $(PYTHON_INCLUDES) \
		$(SRC_CPP)/option_pricing_wrapper.cpp \
		-o option_pricing_cpp$(PYTHON_EXT_SUFFIX)
	@echo "✅ C++ compilation complete!"

clean:
	@echo "🧹 Cleaning up..."
	rm -rf build/
	rm -rf src/cython_modules/*.c
	rm -rf src/cython_modules/*.so
	rm -rf src/cython_modules/*.pyd
	rm -rf src/cython_modules/__pycache__
	rm -rf *.so *.pyd
	rm -rf *.html  # Cython annotation files
	@echo "✅ Clean complete!"

test: all
	@echo "🧪 Running performance tests..."
	$(PYTHON) -c "from tests.test_performance import run_all_benchmarks; run_all_benchmarks()"

install-deps:
	@echo "📦 Installing dependencies..."
	pip install cython pybind11 numpy scipy
	@echo "✅ Dependencies installed!"
