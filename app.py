from flask import Flask, render_template, request, redirect, jsonify, make_response
from evora import dummy as andor #andor
# app = Flask(__name__)

#try:
#    from evora import andor
#except(ImportError):
#    print("COULD NOT GET DRIVERS/SDK, STARTING IN DUMMY MODE")
    # TODO: add dummy server if necessary

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

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
        if request.method == "POST":
            req = request.get_json(force=True)

            andor.setTemperature(req['temp'])
            #print(req)

            res = make_response(jsonify(req), 200)

            return res

    @app.route('/getStatusTEC')
    def route_getStatusTEC():
        return str(andor.getStatusTEC())

    return app

app = create_app()


if __name__ == '__main__':
    app.run(port=3000)
