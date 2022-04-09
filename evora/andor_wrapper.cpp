#include <pybind11/pybind11.h>
#include <atmcdLXd.h>
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
		out.push_back(std::vector<at_32>(imageWidth));
	}
	for (auto row = 0; row < imageHeight; row++) {
		for (auto col = 0; col < imageWidth; col++) {
			out[row][col] = imageData[row * col];
		}
	}

	return out;
}

unsigned int InitializeWrapper(std::string andor_dir = "/usr/local/etc/andor") {
	char* casted = const_cast<char*>(andor_dir.c_str());
	return Initialize(casted);
}

PYBIND11_MODULE(andor_wrapper, m) {
    m.def("initialize",		&InitializeWrapper,         "Initialize the Andor Camera",
        py::arg("andor_dir") = "/usr/local/etc/andor"
    );

    m.def("setReadMode",	        &SetReadMode,           "Set Read Mode");
    m.def("shutdown",		        &ShutDown,              "Shutdown the Andor Camera");
    m.def("setAcquisitionMode",	    &SetAcquisitionMode,	"Set acquisition mode");
    m.def("setExposureTime",	    &SetExposureTime,	    "Set exposure time of shot");
    m.def("getAcquisitionTimings",  
                                    [](void) {
                                        float exposure, accumulate, kinetic;
                                        GetAcquisitionTimings(&exposure, &accumulate, &kinetic);
                                        py::dict out;
                                        out["exposure"] = exposure;
                                        out["accumulate"] = accumulate;
                                        out["kinetic"] = kinetic;

                                        return out;
                                    },                      "Get current camera timing settings");
    m.def("getStatus",		
                                [](void) {
                                    int status;
                                    GetStatus(&status);
                                    return status;
                                },	                    "Get camera status");

    m.def("getDetector",	
                                [](void) {
                                    int imageWidth, imageHeight;
                                    GetDetector(&imageWidth, &imageHeight);
                                    return py::make_tuple(imageWidth, imageHeight);
                                },                      "Get detector dimensions");	// converted into a tuple.

    m.def("setShutter", 		&SetShutter,		    "Initialize camera shutter");
    m.def("setImage",   		&SetImage,		        "Set image dimensions");
    m.def("startAcquisition",	&StartAcquisition,	    "Acquire CCD data");
    m.def("waitForAcquisition",	&WaitForAcquisition,	"Wait until an acquisition event occurs");
    m.def("abortAcquisition",	&AbortAcquisition,	    "Abort current acquisition if there is one");
    m.def("getAcquiredData",	
                                [](py::tuple& dim) {
                                    py::array out = py::cast(acquireDataMatrix(
                                                dim[0].cast<int>(),
                                                dim[1].cast<int>()
                                    ));
                                    return out;
                                },     					"Return CCD data");		// converted into a NumPy array.

    m.def("coolerOn",		    &CoolerON,	        	"Turn on Thermoelectric Cooler (TEC)");
    m.def("coolerOff",		    &CoolerOFF,	            "Turn off Thermoelectric Cooler (TEC)");
    m.def("setTargetTEC",	    &SetTemperature,    	"Set target TEC temperature");
    m.def("getStatusTEC",	
                                [](void) {
                                    float temperature;
                                    int status;
                                    status = GetTemperatureF(&temperature);
                                    py::dict out;
                                    out["temperature"]	= temperature;
                                    out["status"]	= status;
                                
                                    return out;
                                },	                    "Get TEC temperature and status");

    m.def("getRangeTEC",	    &GetTemperatureRange,	"Get valid range of temperatures (C) which TEC can cool to");
    m.def("setFanMode",		    &SetFanMode,		    "Set fan mode");
}
