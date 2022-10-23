#print('__init__ ran')
try:
    from .andor import *
except: #(ImportError, AndorCameraError):
    from .dummy import *
#from .dummy import *