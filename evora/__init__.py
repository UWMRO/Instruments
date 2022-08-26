try:
    from .andor import *
except ImportError:
    print('Dummy mode is ACTIVE (Pybind11 wrapper not found.)')
    from .andor_dummy import *
