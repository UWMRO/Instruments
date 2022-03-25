#include <atmcdLXd.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

PYBIND11_MODULE (andorbind, m) {
    m.def("Initialize", &Initialize, "Initialize the Andor Camera");
}
