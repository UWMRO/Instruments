from flask import Flask, render_template, request, redirect, jsonify, make_response
from evora.dummy import Dummy as andor #andor
from andor_routines import startup, activateCooling, deactivateCooling
from astropy.io import fits
import logging

# app = Flask(__name__)

#try:
#    from evora import andor
#except(ImportError):
#    print("COULD NOT GET DRIVERS/SDK, STARTING IN DUMMY MODE")
    # TODO: add dummy server if necessary

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
    
    andor.initialize()

    app.logger.info(f"Startup Status: {start['status']}")

    @app.route('/getStatus')
    def getStatus():
        return jsonify(andor.getStatus())

    @app.route('/')
    def index():
        tempData = andor.getStatusTEC()['temperature']
        return render_template('index.html', tempData=tempData)

    # REMEMBER: localhost:5000/temperature
    @app.route('/getTemperature')
    def route_getTemperature():
        # return str(andor.getStatusTEC()['temperature'])
        return jsonify(andor.getStatusTEC())
    

    @app.route('/setTemperature', methods=['POST'])
    def route_setTemperature():
        if request.method == 'POST':
            req = request.get_json(force=True)
            
            try:
                req_temperature = float(req['temperature'])
                app.logger.info(f'Setting temperature to: {req_temperature:.2f} [C]')
                andor.setTemperature(req_temperature)
            except ValueError:
                app.logger.info('Post request received a parameter of invalid type (must be float)')
        
        return str(req['temperature'])

    # def route_setTemperature():
    #     """
    #     Sets the temperature of the camera in Celsius. Uses the 'POST' method
    #     to take in form requests from the front end.

    #     Returns the set temperature for display on the front end.
    #     """
    #     if request.method == "POST":
    #         app.logger.info('setting temperature')
    #         req = request.get_json(force=True)

    #         #change_temp = andor.setTemperature(req['temp'])
    #         activateCooling(req['temp'])

    #         curr_temp = andor.getStatusTEC()['temperature']
    #         while curr_temp != req['temp']:
    #             curr_temp = andor.getStatusTEC()['temperature']
    #         deactivateCooling()

    #         app.logger.info(andor.getStatusTEC()['temperature'])

    #         res = req['temp']

    #         return res

    @app.route('/getStatusTEC')
    def route_getStatusTEC():
        return str(andor.getStatusTEC())

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
            # todo: review parallelism, threading behavior is what we want?
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
                hdu.writeto(f"server/fits_files/{req['file_name']}.fits", overwrite=True)
                return str('Capture Successful')
                # next thing to do - utilize js9
            else:
                andor.setShutter(1, 0, 50, 50)
                return str('Capture Unsuccessful')
            

    return app

app = create_app()


if __name__ == '__main__':
    app.run(host='localhost', port=3000)
