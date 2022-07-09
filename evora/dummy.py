from andor_error import ERROR_CODES, AndorCameraError

state = 20075

def initialize(set_state=20002):
    if set_state != 20002:
        raise AndorCameraError(error_code)
    else:
        return set_state