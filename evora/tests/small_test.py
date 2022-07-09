import pytest
import sys
  
# setting path
sys.path.append('../evora')
from dummy import *
from andor_error import ERROR_CODES, AndorCameraError

@pytest.fixture
def initialize_andor():
   return initialize()

def test_initialize(initialize_andor):
    assert initialize_andor == 20002