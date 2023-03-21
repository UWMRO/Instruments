from PIL import Image
from numpy import asarray
import base64
from io import BytesIO
from random import randint
import threading
import time

# Replacement constants, taken from atmcdLXd.h
DRV_SUCCESS = 20002
DRV_TEMPERATURE_OFF = 20034
DRV_TEMPERATURE_STABILIZED = 20036
DRV_NOT_INITIALIZED = 20075
DRV_ACQUIRING = 20072
DRV_IDLE = 20073

min_temp = -80.0
max_temp = 50.0
current_temp = 20.0

initialized = False
acquiring = False
acquisition_mode = 1
exp_time = 0.1

"""
SWIG notes
SWIG seems to change the API from the docs in two major ways
1. Unsigned int functions actually return [status, return_val] e.g. [DRV_SUCCESS, 35]
2. Pointer arguments are simply omitted e.g. int SomeFunction(long* input) -> def SomeFunction()...
"""

# todo: execute this in a separate thread to emulate locking during acquisition?
def __emulate_acquisition(exp_time=exp_time):
    acquiring = True
    time.sleep(exp_time)
    acquiring = False

# Andor SDK replacement functions with return values
def getStatus():
    if initialized:
        if not acquiring:
            return {
                'status' : DRV_IDLE,
                'funcstatus' : DRV_SUCCESS
            }
        else:
            return {
                'status' : DRV_ACQUIRING,
                'funcstatus' : DRV_SUCCESS
            }
    else:
        return {
            'status' : DRV_NOT_INITIALIZED,
            'funcstatus' : DRV_NOT_INITIALIZED
        }
    #return DRV_NOT_INITIALIZED


def getStatusTEC():
    if initialized:
        if not acquiring:
            return {
                'status' : DRV_SUCCESS, 
                'temperature': current_temp
            }
        else:
            return {
                'status' : DRV_ACQUIRING, 
                'temperature': -999.0
            }
    else:
        return {
            'status' : DRV_NOT_INITIALIZED, 
            'temperature': -999.0
        }
    


def setTemperature(value):
    global current_temp 
    current_temp = float(value) 
    return current_temp

def setTargetTEC(temperature):
    if initialized:
        if not acquiring:
            current_temp = temperature
            return DRV_SUCCESS
        else:
            return DRV_ACQUIRING
    else:
        return DRV_NOT_INITIALIZED

def getAvailableCameras():
    return 1


def getCameraHandle(cameraIndex):
    return DRV_SUCCESS


def initialize(directory=''):
    initialized = True
    return DRV_SUCCESS


# def getTemperatureF():
#     return -999

# def getTemperatureStatus():
#     return DRV_SUCCESS

def getTemperatureRange():
    if initialized:
        if not acquiring:
            return {
                'min' : min_temp,
                'max' : max_temp,
                'status' : DRV_SUCCESS
            }
        else:
            return {
            'min' : -999.0,
            'max' : -999.0,
            'status' : DRV_ACQUIRING
        }
    else:
        return {
            'min' : -999.0,
            'max' : -999.0,
            'status' : DRV_NOT_INITIALIZED
        }


# Acquisition
def startAcquisition():
    # todo: emulate the locking behavior when andor is taking a picture
    # add a boolean called 'acquiring'. if True, then lock the dummy module
    # this function will begin a thread where acquiring is set to True
    # for exp_time amount of time
    # other functions in the module will check if acquiring is False before proceeding
    if initialized:
        # acquiring = True
        if not acquiring:
            thread = threading.Thread(target=__emulate_acquisition)
            thread.start()
            return DRV_SUCCESS
        else:
            return DRV_ACQUIRING
    else:
        return DRV_NOT_INITIALIZED



def abortAcquisition():
    DRV_ACQUIRING = 0


def getAcquiredData(dim):
    if initialized:
        if not acquiring:
            img = 'space.txt'
            if randint(0, 1000) >= 999:
                img = 'server/evora/space0.txt'

            #time_sec = int(exp_time)

            #while time_sec:
            #    mins, secs = divmod(time_sec, 60)
            #    timer = '{:02d}:{:02d}'.format(mins, secs)
            #    print(timer, end="\r")
            #    time.sleep(1)
            #    time_sec -= 1
            
            #import os
            #list = os.listdir('.')

            with open(img) as f:
                data = asarray(Image.open(BytesIO(base64.b64decode(f.read()))))

            # This might not work, passing by reference is weird in Python
            
            return {
                'data' : data,
                'status' : DRV_SUCCESS
            }
        else:
            return {
                'data' : np.array([]),
                'status' : DRV_ACQUIRING
            }
    else:
        return {
                'data' : np.array([]),
                'status' : DRV_NOT_INITIALIZED
            }


# These functions do the same thing in this context
getMostRecentImage16 = getAcquiredData


def getAcquisitionTimings():
    if initialized:
        if not acquiring:
            return {
                'exposure' : exp_time,
                'accumulate' : -1.0,
                'kinetic' : -1.0,
                'status' : DRV_SUCCESS
            }
        else:
            return DRV_ACQUIRING
    else:
        return DRV_NOT_INITIALIZED


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


def getDetector():
    if initialized:
        if not acquiring:
            return {
                'dimensions' : (1024, 1024),
                'status' : DRV_SUCCESS
            }
        else:
            return {
                'dimensions' : (-1, -1),
                'status' : DRV_ACQUIRING
            }
    else:
        return {
            'dimensions' : (-1, -1),
            'status' : DRV_NOT_INITIALIZED
        }


def getAcquisitionProgress(acc, series):
    return 1


# Setter functions
def noop(*args):
    # Takes any number of arguments, does nothing
    pass


# Set to noop func instead of defining each to save space
setCurrentCamera = noop

def setAcquisitionMode(mode):
    if initialized:
        if not acquiring:
            acquisition_mode = mode
            return DRV_SUCCESS
        else:
            return DRV_ACQUIRING
    else:
        return DRV_NOT_INITIALIZED

#setTemperature = noop
# setShutter = noop
def setFanMode(mode):
    if initialized:
        if not acquiring:
            return DRV_SUCCESS
        else:
            return DRV_ACQUIRING
    else:
        return DRV_NOT_INITIALIZED

def coolerOn():
    if initialized:
        if not acquiring:
            return DRV_SUCCESS
        else:
            return DRV_ACQUIRING
    else:
        return DRV_NOT_INITIALIZED

def coolerOff():
    if initialized:
        if not acquiring:
            return DRV_SUCCESS
        else:
            return DRV_ACQUIRING
    else:
        return DRV_NOT_INITIALIZED


def shutdown():
    if not acquiring:
            initialized = False
            return DRV_SUCCESS
        else:
            return DRV_ACQUIRING
    

def setReadMode():
    if initialized:
        if not acquiring:
            return DRV_SUCCESS
        else:
            return DRV_ACQUIRING
    else:
        return DRV_NOT_INITIALIZED

def setImage(hbin, vbin, hstart, hend, vstart, vend):
    # determine the specifics of the behavior later lol
    if initialized:
        if not acquiring:
            return DRV_SUCCESS
        else:
            return DRV_ACQUIRING
    else:
        return DRV_NOT_INITIALIZED

def setShutter(typ, mode, closing_time, opening_time):
    # determine the specifics of the behavior later lol
    if initialized:
        return DRV_SUCCESS
    else:
        return DRV_NOT_INITIALIZED

def setExposureTime(exp_time):
    if initialized:
        if not acquiring:
            exp_time = exp_time
            return DRV_SUCCESS
        else:
            retrun DRV_ACQUIRING
    else:
        return DRV_NOT_INITIALIZED

setKineticCycleTime = noop
setNumberAccumulations = noop
setAccumulationCycleTime = noop
setNumberKinetics = noop
setTriggerMode = noop
