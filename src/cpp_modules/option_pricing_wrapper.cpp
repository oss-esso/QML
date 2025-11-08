/**
 * Python bindings for C++ option pricing library using pybind11
 * 
 * Compile with:
 * g++ -O3 -Wall -shared -std=c++17 -fPIC `python3 -m pybind11 --includes` \
 *     option_pricing_wrapper.cpp -o option_pricing_cpp`python3-config --extension-suffix`
 */

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "option_pricing.hpp"

namespace py = pybind11;
using namespace OptionPricing;

PYBIND11_MODULE(option_pricing_cpp, m) {
    m.doc() = "High-performance option pricing library (C++ backend)";
    
    // Black-Scholes class
    py::class_<BlackScholes>(m, "BlackScholes")
        .def_static("call_price", &BlackScholes::call_price,
                   "Price European call option using Black-Scholes formula",
                   py::arg("S"), py::arg("K"), py::arg("T"), 
                   py::arg("r"), py::arg("sigma"))
        .def_static("put_price", &BlackScholes::put_price,
                   "Price European put option using Black-Scholes formula",
                   py::arg("S"), py::arg("K"), py::arg("T"), 
                   py::arg("r"), py::arg("sigma"))
        .def_static("calculate_d1", &BlackScholes::calculate_d1,
                   "Calculate d1 parameter")
        .def_static("calculate_d2", &BlackScholes::calculate_d2,
                   "Calculate d2 parameter");
    
    // Greeks struct
    py::class_<BlackScholes::Greeks>(m, "Greeks")
        .def_readonly("delta", &BlackScholes::Greeks::delta)
        .def_readonly("gamma", &BlackScholes::Greeks::gamma)
        .def_readonly("vega", &BlackScholes::Greeks::vega)
        .def_readonly("theta", &BlackScholes::Greeks::theta)
        .def_readonly("rho", &BlackScholes::Greeks::rho);
    
    m.def("calculate_greeks", &BlackScholes::calculate_greeks,
          "Calculate all Greeks at once (optimized)",
          py::arg("S"), py::arg("K"), py::arg("T"), 
          py::arg("r"), py::arg("sigma"), py::arg("is_call"));
    
    // Monte Carlo class
    py::class_<MonteCarlo>(m, "MonteCarlo")
        .def(py::init<unsigned>(), py::arg("seed") = 42)
        .def("european_option", &MonteCarlo::european_option,
             "Price European option with Monte Carlo (antithetic variates)",
             py::arg("S0"), py::arg("K"), py::arg("T"), 
             py::arg("r"), py::arg("sigma"), 
             py::arg("n_simulations"), py::arg("is_call"))
        .def("asian_option", &MonteCarlo::asian_option,
             "Price Asian option with Monte Carlo",
             py::arg("S0"), py::arg("K"), py::arg("T"), 
             py::arg("r"), py::arg("sigma"), 
             py::arg("n_simulations"), py::arg("n_steps"), 
             py::arg("is_call"));
    
    // Binomial Tree
    py::class_<BinomialTree>(m, "BinomialTree")
        .def_static("american_option", &BinomialTree::american_option,
                   "Price American option using CRR binomial tree",
                   py::arg("S0"), py::arg("K"), py::arg("T"), 
                   py::arg("r"), py::arg("sigma"), 
                   py::arg("n_steps"), py::arg("is_call"));
}
