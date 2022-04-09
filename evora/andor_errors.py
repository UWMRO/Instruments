from error_codes import ERROR_CODES

class StartupError(Exception):
    def __init__(self, error_code):
        self.error_code = error_code
        super().__init__(ERROR_CODES[self.error_code])

    def __str__(self):
        return f'{self.error_code}: {ERROR_CODES[self.error_code]}. Related: Initialize'
    
class BusyError(Exception):
    pass

class AcquisitionError(Exception):
    pass
