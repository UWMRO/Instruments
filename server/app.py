from flask import Flask, render_template, request, redirect, jsonify, make_response, send_from_directory, current_app
from evora import dummy as andor #andor
# import evora.andor as andor
from andor_routines import startup, activateCooling, deactivateCooling, acquisition
from astropy.io import fits
import logging
import socket
import os
import numpy as np
from datetime import datetime

# app = Flask(__name__)

#try:
#    from evora import andor
#except(ImportError):
#    print("COULD NOT GET DRIVERS/SDK, STARTING IN DUMMY MODE")
    # TODO: add dummy server if necessary

#filter server
#try:
#    connection = socket.create_connection(('localhost', 3002))
#except Exception:
#    connection = socket.create_connection(('localhost', 5503))


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    logging.basicConfig(level=logging.DEBUG)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    start = startup()

    app.logger.info(f"Startup Status: {start['status']}")

    # a simple page that says hello
    @app.route('/getStatus')
    def getStatus():
        return str(andor.getStatus())

    @app.route('/')
    def index():
        tempData = andor.getStatusTEC()['temperature']
        return render_template('index.html', tempData=tempData)


    # REMEMBER: localhost:5000/temperature
    @app.route('/getTemperature')
    def route_getTemperature():
        return str(andor.getStatusTEC()['temperature'])


    @app.route('/setTemperature', methods=['POST'])
    def route_setTemperature():
        """
        Sets the temperature of the camera in Celsius. Uses the 'POST' method
        to take in form requests from the front end.

        Returns the set temperature for display on the front end.
        """
        if request.method == "POST":
            app.logger.info('setting temperature')
            req = request.get_json(force=True)

            #change_temp = andor.setTemperature(req['temp'])
            activateCooling(req['temp'])

            curr_temp = andor.getStatusTEC()['temperature']
            while curr_temp != req['temp']:
                curr_temp = andor.getStatusTEC()['temperature']
            deactivateCooling()

            app.logger.info(andor.getStatusTEC()['temperature'])

            res = req['temp']

            return res

    @app.route('/getStatusTEC')
    def route_getStatusTEC():
        return str(andor.getStatusTEC())

    @app.route('/get_filter_position')
    def route_get_filter():
        pass

    @app.route('/setFilterPosition')
    def route_set_filter():
        pass

    def get_filter():
        pass
    
    @app.route('/testReturnFITS', methods=['GET'])
    def route_testReturnFITS():
        acq = acquisition((1024, 1024), exposure_time=0.1)
        

        hdu = fits.PrimaryHDU(data=acq['data'])
        filename = f'{datetime.now().strftime("%m-%d-%Y_T%H%M%S")}.fits'
        hdu.writeto('./fits_files/' + filename)
        
        # np.savetxt('./uploads/' + filename, acq['data'], delimiter=',')
        uploads = os.path.join(current_app.root_path, './fits_files/')
        return send_from_directory(uploads, filename, as_attachment=True)

    @app.route('/testLongExposure')
    def route_testLongExposure():
        acquisition((1024, 1024), exposure_time=10)
        return str('Finished Acquiring after 10s')

    @app.route('/capture', methods=["POST"])
    def route_capture():
        """
        Attempts to take a picture with the camera. Uses the 'POST' method
        to take in form requests from the front end.

        TBD: What to return - the fits file or the np array.
        Throws an error if status code is not 20002 (success).
        """
        if request.method == "POST":
            req = request.get_json(force=True)

            dim = andor.getDetector()['dimensions']

            # check if acquisition is already in progress
            status = andor.getStatus()
            if status == 20072:
                return str('Acquisition already in progress.')

            # handle img type
            if req['img_type'] == 'bias':
                andor.setShutter(1, 2, 50, 50)
                andor.setImage(1, 1, 1, dim[0], 1, dim[1])
            else:
                andor.setShutter(1, 0, 50, 50)
                andor.setImage(1, 1, 1, dim[0], 1, dim[1])

            # handle exposure type
            # refer to pg 41 - 45 of sdk for acquisition mode info
            if req['exp_type'] == 'Single':
                andor.setAcquisitionMode(1)
                andor.setExposureTime(float(req['exp_time']))
                
            elif req['exp_type'] == 'Real Time':
                # this uses "run till abort" mode - how do we abort it?
                andor.setAcquisitionMode(5)
                andor.setExposureTime(0.3)
                andor.setKineticCycleTime(0)

            elif req['exp_type'] == 'Series':
                andor.setAcquisitionMode(3)
                andor.setNumberKinetics(int(req['exp_num']))
                andor.setExposureTime(float(req['exp_time']))
                
            andor.startAcquisition()
            status = andor.getStatus()
            while (status == 20072):
                status = andor.getStatus()
                app.logger.info('Acquisition in progress')

            #if status == 20073:
            #    andor.startAcquisition()
            #else:
            #    return 'Acquisition already in progress'

            img = andor.getAcquiredData(dim)
            
            if img['status'] == 20002:
                # use astropy here to write a fits file
                andor.setShutter(1, 0, 50, 50)
                hdu = fits.PrimaryHDU(img['data'])
                hdu.header['EXP_TIME'] = (float(req['exp_time']), "Exposure Time (Seconds)")
                hdu.header['EXP_TYPE'] = (str(req['exp_type']), "Exposure Type (Single, Real Time, or Series)")
                hdu.header['IMG_TYPE'] = (str(req['img_type']), "Image Type (Bias, Flat, Dark, or Object)")
                hdu.header['FILTER'] = (str(req['fil_type']), "Filter (Ha, B, V, g, r)")
                #hdu.writeto(f"server/fits_files/{req['file_name']}.fits", overwrite=True)
                hdu.writeto(f"fits_files/{req['file_name']}.fits", overwrite=True)
                return str('Capture Successful')
                # next thing to do - utilize js9
            else:
                andor.setShutter(1, 0, 50, 50)
                return str('Capture Unsuccessful')
            

    return app

app = create_app()


if __name__ == '__main__':
    app.run(host= 'localhost', port=3000)
