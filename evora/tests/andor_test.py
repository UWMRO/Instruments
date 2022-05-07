import unittest
import sys
  
# setting path
sys.path.append('../evora')
from andor import *


def test_initialize():
   assert initialize() == 20002


def test_setAcquisitionMode():
   assert setAcquisitionMode() == 20002


def test_setExposureTime():
   pass


def test_setShutter():
   pass


def test_setImage():
   pass


def test_setFanMode():
   pass


def test_coolerOn():
   pass


def test_coolerOff():
   pass


def test_setTargetTEC():
   pass


def test_startAcquisition():
   pass


def test_getStatus():
   pass


def main():
   test_initialize()


if __name__ == '__main__':
   main()
