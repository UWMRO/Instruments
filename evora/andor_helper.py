import andor_wrapper as wrapper
import andor_errors as errors

# Ideally: the only functions exposed are here (for abstraction principles)
def startup(andor_dir='/usr/local/etc/andor'):
    error_code = wrapper.initialize(andor_dir=andor_dir)
    if error_code != 20002:
        raise errors.StartupError(error_code)
    else:
        return error_code

def acquireBias():
    pass

def acquireImage():
    pass

def enableTEC():
    pass

def statusTEC():
    pass

def disableTEC():
    pass


