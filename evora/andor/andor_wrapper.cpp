#include <atmcdLXd.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

PYBIND11_MODULE(andor_wrapper, m) {
    m.def("initialize", &Initialize, "Initialize the Andor Camera");
    m.def("set_read_mode", &SetReadMode, "Set Read Mode");
    m.def("shutdown", &ShutDown, "Shutdown the Andor Camera");
}
