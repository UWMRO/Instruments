from PIL import Image
from numpy import asarray
import base64
from io import BytesIO
from random import randint
import time

# Replacement constants, taken from atmcdLXd.h
DRV_SUCCESS = 20002
DRV_TEMPERATURE_OFF = 20034
DRV_TEMPERATURE_STABILIZED = 20036
DRV_NOT_INITIALIZED = 20075
DRV_ACQUIRING = 20072
DRV_IDLE = 20073

current_temp = -999.

"""
SWIG notes
SWIG seems to change the API from the docs in two major ways
1. Unsigned int functions actually return [status, return_val] e.g. [DRV_SUCCESS, 35]
2. Pointer arguments are simply omitted e.g. int SomeFunction(long* input) -> def SomeFunction()...
"""


# Andor SDK replacement functions with return values
def getStatus():
    return DRV_IDLE
    #return DRV_NOT_INITIALIZED


def getStatusTEC():
    return {'status':DRV_NOT_INITIALIZED, 'temperature':current_temp}


def setTemperature(value):
    global current_temp 
    current_temp = float(value) 
    return current_temp


def getAvailableCameras():
    return 1


def getCameraHandle(cameraIndex):
    return DRV_SUCCESS


def initialize(directory=''):
    return 1


def getTemperatureF():
    return -999


def getTemperatureStatus():
    return DRV_SUCCESS


def getTemperatureRange(mintemp, maxtemp):
    return maxtemp - mintemp


# Acquisition
def startAcquisition():
    DRV_ACQUIRING = 1


def abortAcquisition():
    DRV_ACQUIRING = 0


def getAcquiredData():
    img = 'evora/space.txt'
    if randint(0, 1000) >= 999:
        img = 'evora/space0.txt'

    #time_sec = int(exp_time)

    #while time_sec:
    #    mins, secs = divmod(time_sec, 60)
    #    timer = '{:02d}:{:02d}'.format(mins, secs)
    #    print(timer, end="\r")
    #    time.sleep(1)
    #    time_sec -= 1

    with open(img) as f:
        data = asarray(Image.open(BytesIO(base64.b64decode(f.read()))))

    # This might not work, passing by reference is weird in Python
    
    return {'data':data, 'status':DRV_SUCCESS}


# These functions do the same thing in this context
getMostRecentImage16 = getAcquiredData


def getAcquisitionTimings(exposure, accumulate, kinetic):
    return 1


def getNumberVSSpeeds(speeds):
    return 1


def getNumberVSAmplitudes(number):
    return 1


def getVSSpeed(index, speed):
    return 1


def getFastestRecommendedVSSpeed(index, speeds):
    return 1


def getNumberHSSpeeds(channel, typ, speeds):
    return 1


def getHSSpeed(channel, typ, index, speed):
    return 1


def getDetector(xpixels, ypixels):
    return 1


def getAcquisitionProgress(acc, series):
    return 1


# Setter functions
def noop(*args):
    # Takes any number of arguments, does nothing
    pass


# Set to noop func instead of defining each to save space
setCurrentCamera = noop
setAcquisitionMode = noop
#setTemperature = noop
setShutter = noop
setFanMode = noop
coolerOFF = noop
coolerON = noop
shutdown = noop
setReadMode = noop
setImage = noop
setShutter = noop
setExposureTime = noop
setKineticCycleTime = noop
setNumberAccumulations = noop
setAccumulationCycleTime = noop
setNumberKinetics = noop
setTriggerMode = noop
