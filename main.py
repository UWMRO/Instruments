from flask import Flask
app = Flask(__name__)

import glob # used only in Evora.getHeader
import os # used only in Evora.chooseLogFile
import time

from evora.common.utils.fits as fits_utils # TODO: edit path structure later
import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.time import Time
from evora.evora import Evora 

try:
    from evora.andor import andor
except(ImportError):
    print("COULD NOT GET DRIVERS/SDK, STARTING IN DUMMY MODE")
    # TODO: add dummy server if necessary

@app.route('/')
def index():
    return 'Server is running'


# REMEMBER: localhost:5000/temperature
@app.route('/temperature')
def route_temperature():
    e = Evora()
    andor_temp = 0  # add something here to output the actual temperature
    # limitation: does not update realtime
    return '{}°C'.format(andor_temp)


if __name__ == '__main__':
    app.run()
