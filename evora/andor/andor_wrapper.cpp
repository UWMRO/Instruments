#include <atmcdLXd.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

// GetAcquiredData originally modifies an array of long (at_32) to acquire the imaging data.
// helper func. below to convert it into a returned value, in matrix form.
std::vector<std::vector<at_32>> acquireDataMatrix(int imageWidth, int imageHeight) {
	at_32* imageData = new at_32[imageWidth * imageHeight];
	GetAcquiredData(imageData, imageWidth * imageHeight);

	auto out = std::vector<std::vector<at_32>>();
	for (auto row = 0; row < imageHeight; row++) {
		for (auto col = 0; col < imageWidth; col++) {
			out[row][col] = imageData[row + col];
		}
	}

	return out;
}

PYBIND11_MODULE(andor_wrapper, m) {
    m.def("initialize",		&Initialize,		"Initialize the Andor Camera");
    m.def("setReadMode",	&SetReadMode,		"Set Read Mode");
    m.def("shutdown",		&ShutDown,		"Shutdown the Andor Camera");
    m.def("setAcquisitionMode",	&SetAcquisitionMode,	"Set acquisition mode");
    m.def("setExposureTime",	&SetExposureTime,	"Set exposure time of shot");
    m.def("getDetector",	[](void) {
		int imageWidth, imageHeight;
		GetDetector(&imageWidth, &imageHeight);
		return py::make_tuple(imageWidth, imageHeight);
	},						"Get detector dimensions");	// converted into a tuple.

    m.def("setShutter",		&SetShutter,		"Initialize camera shutter");
    m.def("setImage",		&SetImage,		"Set image dimensions");
    m.def("startAcquisition",	&StartAcquisition,	"Acquire CCD data");
    m.def("getAcquiredData",	[](const py::tuple& dimensions) {			// revisit this? a tuple is a list, but not all lists are tuples (with len. 2)
		py::array out = py::cast(acquireDataMatrix(
			dimensions[0].cast<int>(),
			dimensions[1].cast<int>()
		));
		return out;
	},						"Return CCD data");		// converted into a NumPy array.
}
