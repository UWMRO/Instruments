from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    return 'Server is running'


# REMEMBER: localhost:5000/temperature
@app.route('/temperature')
def route_temperature():
    andor_temp = 0  # add something here to output the actual temperature
    # limitation: does not update realtime
    return '{}°C'.format(andor_temp)


if __name__ == '__main__':
    app.run()
