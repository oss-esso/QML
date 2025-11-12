#include <pybind11/pybind11.h>
#include "black_scholes.hpp"

namespace py = pybind11;
using namespace FinancialMath;


PYBIND11_MODULE(black_scholes_cpp, m) {
    m.doc() = "Black-Scholes option pricing model";

    py::class_<BlackScholes>(m, "BlackScholes")
        .def_static("call_price", &BlackScholes::call_price,
                    py::arg("S"), py::arg("K"), py::arg("T"), py::arg("r"), py::arg("sigma"),
                    "Calculate the Black-Scholes call option price.")
        .def_static("put_price", &BlackScholes::put_price,
                    py::arg("S"), py::arg("K"), py::arg("T"), py::arg("r"), py::arg("sigma"),
                    "Calculate the Black-Scholes put option price.");

}