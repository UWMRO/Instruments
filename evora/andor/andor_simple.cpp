#include <pybind11/pybind11.h>
#include <atmcdLXd.h>

namespace py = pybind11;

PYBIND11_MODULE(andor_simple, m) {
    m.def("initialize",		&Initialize,		"Initialize the Andor Camera");
    m.def("shutdown",		&ShutDown,		"Shutdown the Andor Camera");
}
