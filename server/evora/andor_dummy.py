from evora.andor_error import ERROR_CODES, AndorCameraError

# Insert code here

def initialize(): #input into function a path, and this will return an int status
    """This function will initialize the Andor SDK System. As part of the initialization procedure on 
some cameras (i.e. Classic, iStar and earlier iXion) the DLL will need access to a
DETECTOR.INI which contains information relating to the detector head, number pixels, 
readout speeds etc""" #boolean
    pass
def setReadMode(): #this will return an int status
    """This function will set the readout mode to be used on the subsequent acquisitions."""
    pass
def setAcquisitionMode(): #this will return an int status
    """This function will set the acquisition mode to be used on the function StartAcquisition."""
    pass
def setExposureTime(): #this will return an int status
    """This function will set the exposure time to the nearest valid value not less than the given 
value. The actual exposure time used is obtained by function GetAcquisitionTimings."""
    pass
def getAcquisitionTimings(): #this will return int status, float exposure, float accumulate, float kinetic
    """This function will return the current “valid” acquisition timing information. This function 
should be used after all the acquisitions settings have been set, e.g. SetExposureTime, 
SetKineticCycleTime and SetReadMode etc. The values returned are the actual times 
used in subsequent acquisitions. 
This function is required as it is possible to set the exposure time to 20ms, accumulate 
cycle time to 30ms and then set the readout mode to full image. As it can take 250ms to 
read out an image it is not possible to have a cycle time of 30ms."""
    pass
def getStatus(): #this will return int status, int camera status
    """This function will return the current status of the Andor SDK system. This function should 
be called before an acquisition is started to ensure that it is IDLE and during an acquisition 
to monitor the process."""
    pass
def getDetector(): #this will return int status, int xpixels, int ypixels
    """This function returns the size of the detector in pixels. The horizontal axis is taken to be 
the axis parallel to the readout register."""
    pass
def setShutter(): #this will return an int status
    """This function controls the behaviour of the shutter.
The typ parameter allows the user to control the TTL signal output to an external shutter. 
The mode parameter configures whether the shutter opens & closes automatically 
(controlled by the camera) or is permanently open or permanently closed. 
The opening and closing time specify the time required to open and close the shutter 
(this information is required for calculating acquisition timings)."""
    pass
def setImage(): #this will return an int status
    """This function will set the horizontal and vertical binning to be used when taking a full 
resolution image."""
    pass
def startAcquisition(): #this will return an int status
    """This function starts an acquisition. The status of the acquisition can be monitored
    via the function GetStatus()."""
    pass
def waitForAcquisition(): #this will return an int status
    """WaitForAcquisition can be called after an acquisition is started using StartAcquisition to 
put the calling thread to sleep until an Acquisition Event occurs. This can be used as a 
simple alternative to the functionality provided by the SetDriverEvent function, as all 
Event creation and handling is performed internally by the SDK library. 
Like the SetDriverEvent functionality it will use less processor resources than 
continuously polling with the GetStatus function. If you wish to restart the calling thread 
without waiting for an Acquisition event, call the function CancelWait.
An Acquisition Event occurs each time a new image is acquired during an Accumulation, 
Kinetic Series or Run-Till-Abort acquisition or at the end of a Single Scan Acquisition.
If a second event occurs before the first one has been acknowledged, the first one will be 
ignored. Care should be taken in this case, as you may have to use CancelWait to exit 
the function."""
    pass


def abortAcquisition(): #this will return an int status
    """This function aborts the current acquisition if one is active."""
    pass
def getAcquiredData(dim=(1024,1024)): 
    """This function will return the data from the last acquisition. The data are returned as long 
integers (32-bit signed integers). The “array” must be large enough to hold the complete 
data set."""
    return np.random.randint(0,256,size= dim)

def coolerOn(): #this will return an int status
    """Switches ON the cooling. On some systems the rate of temperature change is controlled 
until the temperature is within 3º of the set value. Control is returned immediately to the 
calling application."""
    pass
def coolerOff(): #this will return an int status
    """Switches OFF the cooling. The rate of temperature change is controlled in some models 
until the temperature reaches 0º. Control is returned immediately to the calling 
application."""
    pass
def setTargetTEC(): #this will return an int status
    """This function will set the desired temperature of the detector. To turn the cooling ON and 
OFF use the CoolerON and CoolerOFF function respectively."""
    pass
def getStatusTEC(): #this will return an int status
    """This function will return if the TEC has overheated."""
    pass
def getRangeTEC(): #this will return int status, int min, int max
    """This function returns the valid range of temperatures in centigrade to which the detector 
can be cooled."""
    pass
def setFanMode(): #this will return an int status
    """Allows the user to control the mode of the camera fan. If the system is cooled, the fan 
should only be turned off for short periods of time. During this time the body of the 
camera will warm up which could compromise cooling capabilities. 
If the camera body reaches too high a temperature, depends on camera, the buzzer will 
sound. If this happens, turn off the external power supply and allow the system to 
stabilize before continuing."""
    pass