from flask import Flask, render_template, request, redirect, jsonify, make_response
from evora import dummy as andor #andor
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

    print(f'Startup Status: {andor.initialize()}')

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
            req = request.get_json(force=True)

            change_temp = andor.setTemperature(req['temp'])
            app.logger.info(change_temp)

            res = req['temp']

            return res

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

            #refer to pg 41 - 45 of sdk for acquisition mode info
            if req['exp_type'] == 'Single':
                andor.setAcquisitionMode(1)
                
            elif req['exp_type'] == 'Real Time':
                andor.setAcquisitionMode(5)
                andor.setKineticCycleTime(0)

            elif req['exp_type'] == 'Series':
                andor.setAcquisitionMode(3)
                andor.setNumberKinetics(int(req['exp_num']))
                
            
            

            img = andor.getAcquiredData(
                req['file_name'],
                req['exp_time'],
                req['exp_num'],
                req['exp_type'],
                req['img_type'],
                req['fil_type']
                )
            
            if img['status'] == 20002:
                # use astropy here to return a fits file
                return img['data']
            else:
                raise Exception('Capture Unsuccessful')
            

    return app

app = create_app()


if __name__ == '__main__':
    app.run(port=3000)
